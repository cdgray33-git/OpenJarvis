import httpx, json, sqlite3
from openjarvis.tools.storage.sqlite import SQLiteMemory
B = "http://127.0.0.1:8010"; TOK = "ZEPHYRQUILL8842"
s0 = httpx.get(B + "/v1/memory/stats").json()["total_documents"]
good = b"\xff\xfe" + ("W83 decode test %s remote host line\r\n" % TOK).encode("utf-16-le")
junk = ("W83 junk bomless utf16 line\r\n" * 3).encode("utf-16-le")
r = httpx.post(B + "/v1/connectors/upload/ingest/files", files=[("files", ("w83_utf16.txt", good, "text/plain")), ("files", ("w83_junk.txt", junk, "text/plain"))], timeout=60)
print("V2 route status=%d body=%s" % (r.status_code, r.text[:120]))
s1 = httpx.get(B + "/v1/memory/stats").json()["total_documents"]
print("V2 stats %d -> %d  PASS=%s" % (s0, s1, s1 == s0 + 1))
hits = httpx.post(B + "/v1/memory/search", json={"query": TOK, "top_k": 5}).json().get("results", [])
c = hits[0]["content"] if hits else ""
print("V3 hits=%d nul_in_top=%d top=%r  PASS=%s" % (len(hits), c.count("\x00"), c[:70], bool(hits) and "\x00" not in c and TOK in c))
con = sqlite3.connect("file:C:/Users/Admin/.openjarvis/memory.db?mode=ro", uri=True)
ids = [i for i, md in con.execute("select id, metadata from documents") if json.loads(md or "{}").get("title") in ("w83_utf16.txt", "w83_junk.txt")]
con.close(); m = SQLiteMemory()
print("V5 cleanup deleted=%d of %d" % (sum(1 for i in ids if m.delete(i)), len(ids)))
con = sqlite3.connect("file:C:/Users/Admin/.openjarvis/memory.db?mode=ro", uri=True)
n, nul = con.execute("select count(*), sum(instr(content, char(0)) > 0) from documents").fetchone()
print("V5 count=%d rows_with_NUL=%d  PASS=%s" % (n, nul or 0, n == 3 and not nul))
