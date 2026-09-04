# Migration from 1.3.0 to 2.0

Version 2.0 does not install compatibility alias skills. Ask `medrs` about an old skill name; it reads `skills/medrs/references/legacy-skill-map.yaml` and reports the canonical destination and availability.

For an existing project, attach the current DOCX, Markdown, or text draft and request `ho-so-nghien-cuu` in `intake-existing-project` mode. The plugin creates a draft Research Passport, preserves provenance, marks uncertain fields, and asks for confirmation instead of requiring manual re-entry.

Keep 1.3.0 as an uninstalled archival ZIP. To roll back, uninstall 2.0 before reinstalling 1.3.0 so only one set of skill descriptions participates in routing.

Version 2.0 exposes exactly 24 canonical skills. Word formatting now separates semantic restructuring from document mechanics, and any OOXML-only run leaves pagination/visual checks pending. Peer-review revisions use stable comment IDs, changed-artifact locators and hashes; responses from 1.3.0 should be imported as unverified commitments until linked to the current artifact.
