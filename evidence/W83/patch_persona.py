import os, sys, time, shutil, py_compile, hashlib, tempfile
from pathlib import Path
M = "openjarvis-w83-persona-v1"; R = os.getcwd()
P = {k: os.path.join(R, "src", "openjarvis", *v) for k, v in {"stubs": ("agents", "_stubs.py"), "noh": ("agents", "native_openhands.py"), "bld": ("prompt", "builder.py"), "srv": ("cli", "serve.py")}.items()}
T = {k: open(p, "rb").read().decode("utf-8") for k, p in P.items()}
if any(M in t for t in T.values()): print("ALREADY PATCHED - no change"); sys.exit(0)
NL = {k: ("\r\n" if "\r\n" in t else "\n") for k, t in T.items()}
def J(k, lines): return NL[k].join(lines)
E = [
 ("stubs", J("stubs", ["        skill_few_shot_examples: Optional[List[str]] = None,", "    ) -> None:", "        super().__init__(", "            engine,", "            model,", "            bus=bus,", "            temperature=temperature,", "            max_tokens=max_tokens,", "        )"]),
           J("stubs", ["        skill_few_shot_examples: Optional[List[str]] = None,", "        prompt_builder: Optional[Any] = None,  # " + M + " (D-35: author hook was not forwarded)", "    ) -> None:", "        super().__init__(", "            engine,", "            model,", "            bus=bus,", "            temperature=temperature,", "            max_tokens=max_tokens,", "            prompt_builder=prompt_builder,", "        )"])),
 ("noh", J("noh", ["        confirm_callback=None,", "    ) -> None:"]), J("noh", ["        confirm_callback=None,", "        prompt_builder=None,  # " + M, "    ) -> None:"])),
 ("noh", J("noh", ["            confirm_callback=confirm_callback,", "        )"]), J("noh", ["            confirm_callback=confirm_callback,", "            prompt_builder=prompt_builder,", "        )"])),
 ("bld", J("bld", ["        if self._frozen_prefix is None:", "            self._frozen_prefix = self._build_frozen_prefix()"]),
         J("bld", ["        # " + M + ": rebuild only when a persona file changes (author cache stability kept, notes stay live)", "        _sig = self._files_sig()", "        if self._frozen_prefix is None or _sig != getattr(self, \"_frozen_sig\", None):", "            self._frozen_prefix = self._build_frozen_prefix()", "            self._frozen_sig = _sig"])),
 ("bld", J("bld", ["    def _load_file(self, path_str: str, max_chars: int) -> str:"]),
         J("bld", ["    def _files_sig(self):", "        out = []", "        for p in (self._mf_config.soul_path, self._mf_config.memory_path, self._mf_config.user_path):", "            q = Path(p).expanduser()", "            try:", "                st = q.stat()", "                out.append((str(q), st.st_mtime_ns, st.st_size))", "            except OSError:", "                out.append((str(q), None, None))", "        return tuple(out)", "", "    def _load_file(self, path_str: str, max_chars: int) -> str:"])),
 ("srv", J("srv", ["                agent = agent_cls(engine, model_name, **agent_kwargs)"]),
         J("srv", ["                # " + M + " (P3/W3, owner): author SystemPromptBuilder through the author prompt_builder hook",
                   "                if agent_key == \"native_openhands\" and getattr(agent_cls, \"accepts_tools\", False):",
                   "                    try:",
                   "                        from openjarvis.prompt.builder import SystemPromptBuilder",
                   "                        from openjarvis.agents.native_openhands import OPENHANDS_SYSTEM_PROMPT",
                   "                        from openjarvis.agents.prompt_loader import load_system_prompt_override",
                   "                        from openjarvis.tools._stubs import build_tool_descriptions",
                   "                        _oj_tmpl = (load_system_prompt_override(\"native_openhands\") or OPENHANDS_SYSTEM_PROMPT).format(",
                   "                            tool_descriptions=build_tool_descriptions(agent_kwargs.get(\"tools\") or []))",
                   "                        agent_kwargs[\"prompt_builder\"] = SystemPromptBuilder(agent_template=_oj_tmpl, memory_files_config=config.memory_files, system_prompt_config=config.system_prompt)",
                   "                        logger.info(\"PERSONA prompt_builder wired agent=%s template_chars=%d\", agent_key, len(_oj_tmpl))",
                   "                    except Exception:",
                   "                        logger.warning(\"PERSONA prompt_builder not wired - agent runs without persona\", exc_info=True)",
                   "                agent = agent_cls(engine, model_name, **agent_kwargs)"]))]
cnt = [T[k].count(a) for k, a, _ in E]; print("ANCHORS", cnt, "(want all 1)")
if cnt != [1] * len(E): print("ABORT - nothing written"); sys.exit(1)
for k, a, b in E: T[k] = T[k].replace(a, b)
ts = time.strftime("%Y%m%d_%H%M%S"); bd = os.path.join(R, "evidence", "W83", "backup")
for k, p in P.items():
    shutil.copy2(p, os.path.join(bd, os.path.basename(p) + ".bak-W83-persona-" + ts)); compile(T[k], p, "exec")
for k, p in P.items():
    open(p, "wb").write(T[k].encode("utf-8")); py_compile.compile(p, doraise=True)
    print("PATCHED %-20s marker=%d sha=%s" % (os.path.basename(p), T[k].count(M), hashlib.sha256(T[k].encode()).hexdigest().upper()[:16]))
print("BACKUP suffix .bak-W83-persona-" + ts)
from openjarvis.prompt.builder import SystemPromptBuilder
from openjarvis.core.config import MemoryFilesConfig, load_config
d = Path(tempfile.mkdtemp()); (d / "S.md").write_text("soul"); (d / "M.md").write_text("mem-one"); (d / "U.md").write_text("user")
b = SystemPromptBuilder(agent_template="TPL", memory_files_config=MemoryFilesConfig(soul_path=str(d / "S.md"), memory_path=str(d / "M.md"), user_path=str(d / "U.md")))
x1 = b.build(); x2 = b.build(); time.sleep(0.05); (d / "M.md").write_text("mem-two-changed"); x3 = b.build()
print("T1 builder cache-stable=%s live-after-change=%s" % (x1 is x2 or x1 == x2, "mem-two-changed" in x3 and "mem-one" not in x3))
shutil.rmtree(d, ignore_errors=True)
from openjarvis.agents.native_openhands import NativeOpenHandsAgent, OPENHANDS_SYSTEM_PROMPT
cfg = load_config()
pb = SystemPromptBuilder(agent_template="TEMPLATE-MARK", memory_files_config=cfg.memory_files, system_prompt_config=cfg.system_prompt)
class _E: pass
ag = NativeOpenHandsAgent(_E(), "stub", tools=[], prompt_builder=pb)
msgs = ag._build_messages("hi", None, system_prompt="PER-TURN-IGNORED")
sysm = [m for m in msgs if m.role.value == "system"]; c = sysm[0].content if sysm else ""
print("T2 system_msgs=%d template=%s persona=%s memory_live=%s per_turn_ignored=%s" % (len(sysm), c.startswith("TEMPLATE-MARK"), "## Agent Persona" in c, "AMBERFINCH-5520" in c, "PER-TURN-IGNORED" not in c))
print("T3 serve.py compiled OK")
