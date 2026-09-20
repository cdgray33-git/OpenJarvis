# MARKER: openjarvis-openapi-isolate-v1
"""Isolate the route responsible for the GET /openapi.json 500.

Read-only. Builds an in-process FastAPI app via create_app(None, "") and then
generates the OpenAPI schema one route at a time, reporting every route that
fails along with its source location and any unresolved string annotations.

Usage:
    uv run --no-sync python .\\tools\\diagnostics\\isolate_openapi.py
"""

import hashlib
import inspect
import sys
import traceback

NAME = "openjarvis-openapi-isolate-v1"


def _self_sha256():
    try:
        with open(__file__, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest().upper()
    except Exception as exc:  # pragma: no cover
        return "unavailable ({0})".format(exc)


def _banner():
    print("=" * 78)
    print(NAME)
    print("=" * 78)
    print("  python                       {0}".format(sys.executable))
    print("  script sha256                {0}".format(_self_sha256()))
    print("  mode                         read-only")
    print("=" * 78)


def _describe(route, exc):
    endpoint = route.endpoint
    print("-" * 78)
    print("  path                         {0}".format(route.path))
    try:
        methods = ",".join(sorted(route.methods or []))
    except Exception:
        methods = "?"
    print("  methods                      {0}".format(methods))
    print("  endpoint                     {0}.{1}".format(
        getattr(endpoint, "__module__", "?"),
        getattr(endpoint, "__qualname__", "?"),
    ))
    try:
        print("  defined                      {0}:{1}".format(
            inspect.getsourcefile(endpoint),
            inspect.getsourcelines(endpoint)[1],
        ))
    except Exception:
        print("  defined                      <unavailable>")
    print("  response_model               {0!r}".format(
        getattr(route, "response_model", None)))

    raw = getattr(endpoint, "__annotations__", {}) or {}
    strings = [(k, v) for k, v in raw.items() if isinstance(v, str)]
    if strings:
        print("  UNRESOLVED STRING ANNOTATIONS:")
        for key, value in strings:
            print("    {0} : {1!r}".format(key, value))
    else:
        print("  string annotations           none on this endpoint")
        print("  all annotations:")
        for key, value in raw.items():
            print("    {0} : {1!r}".format(key, value))

    first = str(exc).splitlines()
    first = first[0] if first else ""
    print("  error                        {0}: {1}".format(
        type(exc).__name__, first[:400]))


def main():
    _banner()

    try:
        from fastapi.openapi.utils import get_openapi
        from fastapi.routing import APIRoute
        from openjarvis.server.app import create_app
    except Exception:
        print("VERDICT: FAIL - could not import FastAPI or create_app")
        traceback.print_exc()
        return 2

    print("[*] constructing app via create_app(None, '')")
    print("    NOTE: create_app calls _restore_sendblue_bindings() inline at")
    print("          app.py:298, which reads channel bindings from the database.")
    print("          That read is the only DB access this script causes.")
    try:
        app = create_app(None, "")
    except Exception:
        print("VERDICT: FAIL - create_app() raised before any schema work")
        traceback.print_exc()
        return 2

    api_routes = [r for r in app.routes if isinstance(r, APIRoute)]
    print("[*] routes                     {0} total, {1} APIRoute".format(
        len(app.routes), len(api_routes)))

    try:
        get_openapi(title="probe", version="0", routes=app.routes)
        whole_app_error = None
    except Exception as exc:
        whole_app_error = exc

    if whole_app_error is None:
        print("[*] whole-app schema           OK")
        print("")
        print("VERDICT: PASS - schema generates cleanly in-process.")
        print("         The live 500 is therefore state-dependent, not static.")
        print("         Next step: pull the traceback from backend.log.")
        return 0

    print("[*] whole-app schema           FAILS ({0})".format(
        type(whole_app_error).__name__))
    print("[*] bisecting route by route")
    print("")

    failures = []
    for route in api_routes:
        try:
            get_openapi(title="probe", version="0", routes=[route])
        except Exception as exc:
            failures.append((route, exc))

    for route, exc in failures:
        _describe(route, exc)
    print("-" * 78)
    print("")

    if failures:
        print("VERDICT: FAIL - {0} of {1} routes fail individually.".format(
            len(failures), len(api_routes)))
        return 1

    print("VERDICT: INCONCLUSIVE - whole-app generation fails but no single")
    print("         route does. The cause is cross-route: a shared model, or a")
    print("         duplicate component name colliding in the schema registry.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
