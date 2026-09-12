try:
    from openjarvis.core.credentials import TOOL_CREDENTIALS, get_credential_status
except Exception as e:
    print("IMPORT FAILED: %r" % (e,)); raise SystemExit(1)
parts = []
for t in sorted(TOOL_CREDENTIALS):
    st = get_credential_status(t)
    if isinstance(st, dict):
        total = len(st); s = sum(1 for v in st.values() if v)
        print("TOOL %-24s set=%d total=%d keys=%s" % (t, s, total, sorted(st.keys())))
        if s > 0: parts.append("%s: %d/%d keys" % (t, s, total))
    else:
        print("TOOL %-24s -> unexpected return type %s" % (t, type(st).__name__))
print("")
print("CRED_PARTS_COUNT=%d" % len(parts))
print("GUARD_AT_553_PASSES=%s" % bool(parts))
