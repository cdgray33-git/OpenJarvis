import os, sys
R = os.getcwd()
def edit(rel, pairs):
    p = os.path.join(R, rel); t = open(p, "rb").read().decode("utf-8"); nl = "\r\n" if "\r\n" in t else "\n"
    pairs = [(a.replace("\n", nl), b.replace("\n", nl)) for a, b in pairs]
    cnt = [t.count(a) for a, _ in pairs]; print(rel, "ANCHORS", cnt)
    if cnt != [1] * len(pairs): print("ABORT - nothing written for", rel); return False
    for a, b in pairs: t = t.replace(a, b)
    open(p, "wb").write(t.encode("utf-8")); return True
ok1 = edit("docs/SDP/02-SRS-RTM.md", [
 ("EVIDENCE SUPPORTS VERIFIED; OWNER RULING PENDING | PARTIAL |", "OWNER RULED VERIFIED W83 2026-09-24 (framing caveat recorded) | VERIFIED |"),
 ("v0.7 (W83): R1 qualification ruling; RQ-024 and RQ-031 assessed.", "v0.7 (W83): R1 qualification ruling; RQ-024 and RQ-031 assessed. v0.8 (W83): RQ-024 VERIFIED by owner ruling, 4/28."),
 ("PROGRESS (W83, 2026-09-24): VERIFIED 3/28 unchanged. PARTIAL: RQ-001, RQ-002, RQ-024, RQ-031.",
  "PROGRESS (W83, 2026-09-24): VERIFIED 3/28 unchanged. PARTIAL: RQ-001, RQ-002, RQ-024, RQ-031.\nPROGRESS (W83 owner ruling, 2026-09-24): VERIFIED 4/28 - RQ-021, RQ-022, RQ-024, RQ-030. PARTIAL: RQ-001, RQ-002, RQ-031. OPEN: RQ-004. NOT VERIFIED: RQ-025. NOT ASSESSED: 20.")])
ok2 = edit("BRIEF-W86-2026-09-24.md", [
 ("- RQ-024 evidence supports VERIFIED (undirected take/get/list pass); OWNER RULING PENDING.", "- RQ-024 VERIFIED by owner ruling (W83): VERIFIED 4/28 - RQ-021, RQ-022, RQ-024, RQ-030."),
 ("1. OWNER RULING: RQ-024 VERIFIED now (framing caveat recorded) -> RTM one-line change, VERIFIED 4/28. Or hold.", "1. DONE W83: RQ-024 ruled VERIFIED by owner (4/28), framing caveat recorded in the RTM."),
 ("Recommend first: clean the test notes out of MEMORY.md (AMBERFINCH, SLATEHERON)\n   and memory.db (BLUEHERON) once the owner has real notes to replace them - delete nothing before the replacement exists.",
  "Owner chose to LEAVE the test notes (AMBERFINCH,\n   SLATEHERON in MEMORY.md; BLUEHERON in memory.db); they list alongside real notes until removed."),
 ('"we did not follow the installation guide"). VERIFIED 3/28.', '"we did not follow the installation guide"). VERIFIED 4/28.'),
 ("VERIFIED 3/28 (4/28 pending the RQ-024 ruling).", "VERIFIED 4/28 (RQ-024 ruled W83).")])
print("RESULT rtm=%s brief=%s" % (ok1, ok2))
