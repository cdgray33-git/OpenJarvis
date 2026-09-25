import os, sys
p = os.path.join(os.getcwd(), "docs", "SDP", "02-SRS-RTM.md"); t = open(p, "rb").read().decode("utf-8"); nl = "\r\n" if "\r\n" in t else "\n"
E = [("| RQ-023, 027, 032, 033 | - | - | - | DEFERRED (Phase 2) |",
      "| RQ-032 | code_interpreter + python-docx/python-pptx/openpyxl (D-40..D-45); SOUL Office line (D-44) | dispatch.log, workspace files | W83 S3 re-run 3: 6/6 real .docx/.pptx/.xlsx from undirected family requests, 33/34 requested details machine-checked; open: G-3 delivery, G-10 self-verification (R2 false negative) | PARTIAL - owner ruling pending |" + nl +
      "| RQ-023, 027, 033 | - | - | - | Phase 2, pulled forward W83 (D-39), not yet assessed |"),
     ("PHASE 2 (supporting roles, deferred by owner): RQ-023, RQ-027, RQ-032, RQ-033.",
      "PHASE 2 (supporting roles, deferred by owner): RQ-023, RQ-027, RQ-032, RQ-033. W83: PULLED FORWARD by owner (D-39) to test and tune the persona with MS Office."),
     ("PROGRESS (W83 owner ruling, 2026-09-24): VERIFIED 4/28 - RQ-021, RQ-022, RQ-024, RQ-030.",
      "PROGRESS (W83 owner ruling, 2026-09-24): VERIFIED 4/28 - RQ-021, RQ-022, RQ-024, RQ-030." + nl + "PHASE 2 PROGRESS (W83): RQ-032 evidence 6/6 real documents (S3 re-run 3, 0507c8c), owner ruling pending; RQ-023/027/033 not assessed.")]
c = [t.count(a) for a, _ in E]; print("RTM ANCHORS", c, "(want [1, 1, 1])")
if c != [1, 1, 1]: print("ABORT - RTM not edited"); sys.exit(1)
for a, b in E: t = t.replace(a, b, 1)
open(p, "wb").write(t.encode("utf-8")); print("RTM edited")
