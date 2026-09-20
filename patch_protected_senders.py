# MARKER: openjarvis-protected-senders-v1
import ast, shutil, sys
from pathlib import Path
P = Path("src/openjarvis/tools/mailbox_tools.py")
src = P.read_text(encoding="utf-8")
if "openjarvis-protected-senders-v1" in src:
    print("ALREADY APPLIED"); sys.exit(0)
A1 = "        _resolved = 0\n"
A2 = "            if not _sel:\n"
A3 = '            result["selected_by"] = "from_addr"\n'
for n, a in (("A1", A1), ("A2", A2), ("A3", A3)):
    if src.count(a) != 1:
        print("ANCHOR %s matched %d times - aborting" % (n, src.count(a))); sys.exit(1)
B1 = A1 + "        _blocked_report = {}\n"
B2 = (
"            # openjarvis-protected-senders-v1\n"
"            import json as _json\n"
"            from pathlib import Path as _Path\n"
"            _defaults = ['stackcommerce.com', 'cdgray33@yahoo.com',\n"
"                'notify@r.groupon.com', 'orders@r.groupon.com',\n"
"                'verify@r.groupon.com', 'otp@r.groupon.com',\n"
"                'orders@sidedeal', 'account@', 'ratings@',\n"
"                'noreply@service.wayfair.com']\n"
"            _prot = _defaults\n"
"            try:\n"
"                _pf = _Path.cwd() / 'protected_senders.json'\n"
"                if _pf.is_file():\n"
"                    _ld = _json.loads(_pf.read_text(encoding='utf-8'))\n"
"                    if isinstance(_ld, list) and _ld:\n"
"                        _prot = [str(x).lower() for x in _ld if str(x).strip()]\n"
"            except Exception:\n"
"                logger.exception('protected_senders.json unreadable; using built-in list')\n"
"            _keep = []\n"
"            for _h in _hits or []:\n"
"                if not isinstance(_h, dict):\n"
"                    continue\n"
"                if str(_h.get('folder', '') or '') != folder:\n"
"                    continue\n"
"                _u2 = str(_h.get('uid', '') or '').strip()\n"
"                if not _u2.isdigit():\n"
"                    continue\n"
"                _a = str(_h.get('from_addr', '') or '').lower()\n"
"                _m = ''\n"
"                for _p in _prot:\n"
"                    if _p and _p in _a:\n"
"                        _m = _p\n"
"                        break\n"
"                if _m:\n"
"                    _blocked_report[_a] = _blocked_report.get(_a, 0) + 1\n"
"                else:\n"
"                    _keep.append(_u2)\n"
"            _sel = _keep\n"
"            if _blocked_report:\n"
"                logger.warning('protected senders blocked from move: %s', _blocked_report)\n"
"            if _blocked_report and not _sel:\n"
"                return ToolResult(\n"
"                    tool_name=self.tool_id,\n"
"                    content=_dump({\n"
"                        'error': 'all matched messages are from protected senders; nothing moved',\n"
"                        'protected_blocked': _blocked_report,\n"
"                        'from_addr': _from_addr,\n"
"                        'folder': folder,\n"
"                    }),\n"
"                    success=False,\n"
"                )\n"
) + A2
B3 = A3 + '            if _blocked_report:\n                result["protected_blocked"] = _blocked_report\n'
out = src.replace(A1, B1).replace(A2, B2).replace(A3, B3)
ast.parse(out)
shutil.copyfile(str(P), str(P) + ".bak_protect")
P.write_text(out, encoding="utf-8")
print("APPLIED %d -> %d bytes" % (len(src), len(out)))
