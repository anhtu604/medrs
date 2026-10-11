"""Run with UNO-capable Python; never overwrites input or certifies visual layout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
import uuid
from zipfile import ZipFile
from xml.etree import ElementTree as ET


def _load_uno():
    try:
        import uno
        return uno
    except ImportError:
        return None


def _hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _safe_source(source):
    from docx_integrity import audit_docx_integrity
    integrity = audit_docx_integrity(source)
    if integrity["status"] != "PASS":
        raise ValueError("|".join(item["code"] for item in integrity["issues"]))
    with ZipFile(source) as archive:
        if sum(i.file_size for i in archive.infolist()) > 64 * 1024 * 1024:
            raise ValueError("DOCX_TOO_LARGE")
        toc = False
        for name in archive.namelist():
            if name.endswith(".rels"):
                for rel in ET.fromstring(archive.read(name)):
                    if rel.get("TargetMode") == "External" and not rel.get("Type", "").endswith("/hyperlink"):
                        raise ValueError("EXTERNAL_UPDATE_REQUIRES_SEPARATE_REVIEW")
        for field in integrity["field_instructions"]:
            first = field["instruction"].strip().upper().split()
            if first and first[0] in {"DDE","DDEAUTO","INCLUDETEXT","INCLUDEPICTURE","LINK","DATABASE"}:
                raise ValueError("EXTERNAL_UPDATE_REQUIRES_SEPARATE_REVIEW")
            toc |= bool(first and first[0] == "TOC")
        return toc


def refresh_document(source, output, pdf, *, soffice=None, uno_loader=_load_uno):
    source, output, pdf = [Path(p).resolve() for p in (source, output, pdf)]
    if source in {output, pdf} or output == pdf:
        return {"status": "SOURCE_OVERWRITE_FORBIDDEN"}
    if output.exists() or pdf.exists():
        return {"status": "OUTPUT_ALREADY_EXISTS"}
    uno = uno_loader()
    if uno is None:
        return {"status": "HOST_CAPABILITY_UNAVAILABLE", "reason": "UNO_PYTHON_UNAVAILABLE"}
    executable = soffice or shutil.which("soffice") or shutil.which("soffice.exe")
    if not executable or not Path(executable).is_file():
        return {"status": "HOST_CAPABILITY_UNAVAILABLE", "reason": "SOFFICE_UNAVAILABLE"}
    process, document, reopened, desktop = None, None, None, None
    before = _hash(source)
    try:
        has_toc = _safe_source(source)
        output.parent.mkdir(parents=True, exist_ok=True)
        pdf.parent.mkdir(parents=True, exist_ok=True)
        # Keep this run's isolated profile/log and intermediate files for diagnosis.
        run_dir = output.parent / ("uno-run-" + uuid.uuid4().hex)
        run_dir.mkdir()
        # LibreOffice on Windows crashed with deeply nested profile/cache paths.
        # Retain a short native profile; its location is recorded, not silently deleted.
        profile_dir = Path(tempfile.mkdtemp(prefix="medrs-uno-"))
        staged_docx, staged_pdf = run_dir / "refreshed.docx", run_dir / "render.pdf"
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        command = [str(executable), "-env:UserInstallation=" + profile_dir.as_uri(),
                   "--headless", "--norestore", "--nodefault", "--nofirststartwizard",
                   "--accept=socket,host=127.0.0.1,port=" + str(port) + ";urp;StarOffice.ComponentContext"]
        startup = None
        if os.name == "nt":
            startup = subprocess.STARTUPINFO()
            startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        with (run_dir / "soffice.log").open("wb") as log:
            process = subprocess.Popen(command, stdout=log, stderr=log, startupinfo=startup)
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", local)
        context, connection_error = None, None
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            try:
                context = resolver.resolve(
                    "uno:socket,host=127.0.0.1,port=" + str(port) + ";urp;StarOffice.ComponentContext")
                break
            except Exception as connection_exc:
                connection_error = str(connection_exc)
                if process.poll() is not None:
                    break
                time.sleep(0.2)
        if context is None:
            raise RuntimeError("UNO_CONNECTION_FAILED: exit=" + str(process.poll())
                               + "; bridge=" + str(connection_error))
        desktop = context.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", context)

        def properties(**values):
            props = []
            for key, value in values.items():
                prop = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
                prop.Name, prop.Value = key, value
                props.append(prop)
            return tuple(props)

        # NEVER_EXECUTE=0, NO_UPDATE=0; external update fields rejected above.
        load_props = properties(Hidden=True, ReadOnly=False, MacroExecutionMode=0, UpdateDocMode=0)
        document = desktop.loadComponentFromURL(source.as_uri(), "_blank", 0, load_props)
        if document is None:
            raise RuntimeError("DOCUMENT_LOAD_FAILED")
        indexes = document.getDocumentIndexes()
        count = indexes.getCount()
        if has_toc and count == 0:
            raise RuntimeError("TOC_INDEX_NOT_IMPORTED")
        document.getTextFields().refresh()
        for i in range(count):
            indexes.getByIndex(i).update()
        document.storeAsURL(staged_docx.as_uri(),
                            properties(FilterName="Office Open XML Text", Overwrite=False))
        document.close(True)
        document = None
        reopened = desktop.loadComponentFromURL(staged_docx.as_uri(), "_blank", 0, load_props)
        persisted_indexes = reopened.getDocumentIndexes()
        persisted_count = persisted_indexes.getCount()
        index_text = [persisted_indexes.getByIndex(i).getAnchor().getString()
                      for i in range(persisted_count)]
        if has_toc and (persisted_count == 0 or not any(t.strip() for t in index_text)):
            raise RuntimeError("TOC_REFRESH_NOT_PERSISTED")
        reopened.storeToURL(staged_pdf.as_uri(), properties(FilterName="writer_pdf_Export", Overwrite=False))
        reopened.close(True)
        reopened = None
        if _hash(source) != before:
            raise RuntimeError("SOURCE_CHANGED")
        # Atomic no-replace publication on the same filesystem.
        os.link(staged_docx, output)
        os.link(staged_pdf, pdf)
        return {"status": "REFRESHED_REVIEW_REQUIRED", "backend": "libreoffice-uno",
                "source_sha256": before, "artifact_sha256": _hash(output),
                "pdf_sha256": _hash(pdf), "index_count": count,
                "persisted_index_count": persisted_count, "index_text": index_text,
                "run_dir": str(run_dir), "output": str(output), "pdf": str(pdf),
                "native_profile": str(profile_dir),
                "unperformed": ["post-refresh-integrity", "source-layout-comparison", "visual-inspection"]}
    except Exception as exc:
        return {"status": "REFRESH_FAILED", "reason": str(exc), "source_sha256": before,
                "output_exists": output.exists(), "pdf_exists": pdf.exists()}
    finally:
        for doc in (document, reopened):
            if doc is not None:
                try:
                    doc.close(True)
                except Exception:
                    pass
        if desktop is not None:
            try:
                desktop.terminate()
            except Exception:
                pass
        if process is not None:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.terminate()


def emit_receipt(report):
    print(json.dumps(report, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("pdf")
    parser.add_argument("--soffice")
    args = parser.parse_args()
    report = refresh_document(args.source, args.output, args.pdf, soffice=args.soffice)
    emit_receipt(report)
    raise SystemExit(0 if report["status"] == "REFRESHED_REVIEW_REQUIRED" else 2)
