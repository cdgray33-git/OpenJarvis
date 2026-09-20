import logging
lg = logging.getLogger("openjarvis.cli.serve")
print("LOGGER:", lg.name, "level:", lg.level, "effective:", lg.getEffectiveLevel(), "propagate:", lg.propagate, "disabled:", lg.disabled)
print("OWN HANDLERS:", lg.handlers)
r = logging.getLogger()
print("ROOT level:", r.level, "handlers:", r.handlers)
for h in r.handlers:
    print("  HANDLER", h, "level:", h.level, "filters:", h.filters)
print("MANAGER DISABLE:", logging.root.manager.disable)
