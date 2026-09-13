import io, re, tokenize

p = r"src\openjarvis\tools\_stubs.py"
src = io.open(p, encoding="utf-8").read()
pat = re.compile(r"confirm_callback\s*[=:]\s*.{0,20}lambda[^\n]*True")
hits = sorted({src[:m.start()].count("\n") + 1 for m in pat.finditer(src)})
print("regex hits on lines:", hits)

noncode = set()
with io.open(p, encoding="utf-8") as f:
    for tok in tokenize.generate_tokens(f.readline):
        if tok.type in (tokenize.COMMENT, tokenize.STRING):
            for ln in range(tok.start[0], tok.end[0] + 1):
                noncode.add(ln)

body = src.splitlines()
verdict = "CLEAN"
for ln in hits:
    if ln in noncode:
        kind = "COMMENT_OR_DOCSTRING"
    else:
        kind = "*** EXECUTABLE CODE ***"
        verdict = "REAL SITE FOUND"
    print(ln, kind, "|", body[ln - 1].strip()[:100])
print("VERDICT:", verdict)
