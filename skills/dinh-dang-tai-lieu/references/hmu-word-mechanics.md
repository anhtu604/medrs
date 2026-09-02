# HMU Word mechanics

The HMU profile encodes the official DOCX paragraph 44 requirements: Unicode, Times New Roman 13 or 14 pt, ordinary character density, 1.5-line spacing, A4 page, top and left margins 3.5 cm, bottom 3.0 cm and right 2.0 cm. Arabic page numbering begins at Đặt vấn đề, centered in the header. Paragraph 46 limits numeric heading depth to four levels. Paragraph 48 places table titles above tables and figure/diagram/chart titles below, with chapter-linked numbering.

The deterministic default uses 13 pt, one of the two officially allowed sizes. Changing to 14 pt is an author-approved profile choice and requires rerendering because pagination changes. The formatter may create TOC and PAGE field codes, but the output remains pending until an appropriate backend updates fields and rendered pages are inspected.

Do not infer a compliant document from Normal style alone: paragraphs can carry direct formatting or custom styles. Audit exceptions and report them. Do not place page numbers on preliminary pages merely because a PAGE field exists. Verify the section boundary and restart declaration at Đặt vấn đề in the actual package, then visually confirm the rendered transition.
