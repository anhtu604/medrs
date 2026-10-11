"""Inspect inherited Word run formatting and explicitly controlled table borders."""
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from xml.etree import ElementTree as ET


def story_paragraphs(document):
    # Existing body (including nested tables), headers and footers only. Do not
    # materialize new linked headers or rewrite protected note/comment definitions.
    for part in document.part.package.parts:
        root = getattr(part, "element", None)
        if root is not None and root.tag in {qn("w:document"), qn("w:hdr"), qn("w:ftr")}:
            for node in root.iter(qn("w:p")):
                yield Paragraph(node, document)


def style_chain(style):
    seen = set()
    while style is not None and style.style_id not in seen:
        seen.add(style.style_id)
        yield style
        style = style.base_style


def clear_font_properties(rpr):
    if rpr is None:
        return
    for tag in ("w:rFonts", "w:sz", "w:szCs"):
        for child in list(rpr.findall(qn(tag))):
            rpr.remove(child)


def effective_run_format(run, paragraph, document):
    layers = [run._r.rPr]
    layers += [s.element.rPr for s in style_chain(run.style)]
    layers += [s.element.rPr for s in style_chain(paragraph.style)]
    defaults = document.styles.element.find(qn("w:docDefaults"))
    if defaults is not None:
        default = defaults.find(qn("w:rPrDefault"))
        if default is not None:
            layers.append(default.find(qn("w:rPr")))
    layers = [layer for layer in layers if layer is not None]
    fonts = {}
    theme = None
    for part in document.part.package.parts:
        if str(part.partname) == "/word/theme/theme1.xml":
            theme = ET.fromstring(part.blob)
    for slot in ("ascii", "hAnsi", "eastAsia", "cs"):
        for layer in layers:
            rf = layer.find(qn("w:rFonts"))
            if rf is None:
                continue
            selector = rf.get(qn("w:" + ("cstheme" if slot == "cs" else slot + "Theme")))
            selector = selector or (rf.get(qn("w:csTheme")) if slot == "cs" else None)
            if selector:
                # Theme selectors override a literal face in the same layer.
                ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
                scheme = "majorFont" if selector.startswith("major") else "minorFont"
                face_kind = "ea" if selector.endswith("EastAsia") else "cs" if selector.endswith("Bidi") else "latin"
                face = theme.find(f".//a:fontScheme/a:{scheme}/a:{face_kind}", ns) if theme is not None else None
                # Blank ea/cs faces rely on script-specific fallback. Without an
                # exact script resolution we report unresolved, never assume Latin.
                fonts[slot] = (face.get("typeface") if face is not None else None) or "UNRESOLVED_THEME"
                break
            if rf.get(qn("w:" + slot)):
                fonts[slot] = rf.get(qn("w:" + slot))
                break
    sizes = {}
    for tag in ("sz", "szCs"):
        for layer in layers:
            node = layer.find(qn("w:" + tag))
            if node is not None:
                try:
                    sizes[tag] = float(node.get(qn("w:val"))) / 2
                except (TypeError, ValueError):
                    sizes[tag] = None
                break
    return fonts, sizes


def border_values(policy, *, row=None, rows=None):
    values = {side: "nil" for side in ("top", "bottom", "left", "right", "insideH", "insideV", "start", "end", "tl2br", "tr2bl")}
    if policy == "grid":
        for side in ("top", "bottom", "left", "right", "insideH", "insideV", "start", "end"):
            values[side] = "single"
    elif policy == "no-vertical":
        for side in ("top", "bottom", "insideH"):
            values[side] = "single"
    elif policy == "minimal":
        if row is None or row == 0:
            values["top"] = "single"
        if row is None or row == rows - 1:
            values["bottom"] = "single"
    return values


def borders_match(node, expected):
    # Explicit cell/table overrides are required: inherited grid/conditional
    # style borders cannot masquerade as a no-vertical policy.
    return node is not None and all(
        (child := node.find(qn("w:" + side))) is not None
        and child.get(qn("w:val")) == value for side, value in expected.items())
