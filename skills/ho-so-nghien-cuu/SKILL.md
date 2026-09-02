---
name: ho-so-nghien-cuu
description: Tạo, kiểm tra hoặc tiếp nhận dự án nghiên cứu đang dở thành Research Passport. Creates, validates, confirms, or adopts an existing medical-research project. Không viết bài hay xác nhận dữ kiện thay tác giả.
metadata:
  version: 2.0.0-alpha.1
  role: leaf
  locale: [vi, en]
  document_types: [protocol, thesis, dissertation, manuscript, evidence-synthesis]
---

# Hồ sơ nghiên cứu

Own the Research Passport lifecycle. Use `new`, `adopt-existing-project`, `validate`, `confirm`, or `summarize` mode.

## New project

Create a Passport from confirmed user inputs. Unknown fields remain `UNRESOLVED` with localized marker labels and language-neutral codes.

## Existing project

For a supplied DOCX, Markdown, or text draft, read [references/adopt-existing-project.md](references/adopt-existing-project.md). Extract candidates with artifact and location provenance. Mark every extracted value `DRAFT_INFERRED`, expose conflicts, and ask for confirmation. Never infer ethics approval or verified results.

## Validation and confirmation

Validate against `../../schemas/research-passport.schema.json`. Confirmation must name the field, value, author, and timestamp and append an audit event. Never overwrite the input Passport.

## Output

Return the new Passport path or conversation block, validation issues, inferred-field table, ordered author questions, source-freshness banners, and disclosure record.

