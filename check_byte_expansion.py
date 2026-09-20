import sqlite3

conn = sqlite3.connect(r"C:\Users\Admin\.openjarvis\memory.db")
cur = conn.cursor()

cur.execute("SELECT id, content FROM documents")

total_char_len = 0
total_byte_len = 0
worst_offenders = []

for id_, content in cur:
    if content is None:
        continue
    clen = len(content)
    blen = len(content.encode("utf-8", errors="surrogatepass"))
    total_char_len += clen
    total_byte_len += blen
    if blen > clen * 1.5:
        worst_offenders.append((id_, clen, blen))

print(f"Total character length (what LENGTH() reports): {total_char_len:,}")
print(f"Total actual UTF-8 byte length: {total_byte_len:,} ({total_byte_len/1e9:.2f} GB)")
print(f"Expansion factor: {total_byte_len/total_char_len:.2f}x")
print(f"\nRows with >1.5x byte expansion: {len(worst_offenders):,}")

worst_offenders.sort(key=lambda x: x[2], reverse=True)
print("\nTop 10 worst expansion rows:")
for id_, clen, blen in worst_offenders[:10]:
    print(f"  id={id_}  chars={clen:,}  bytes={blen:,}  ratio={blen/clen:.2f}x")

conn.close()
