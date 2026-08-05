try:
    from openjarvis_rust import TraceStore as RustTraceStore
    class TraceStore:
        def __init__(self, *args, **kwargs):
            try:
                self._backend = RustTraceStore(*args, **kwargs)
            except:
                self._backend = None
        
        def save(self, trace):
            if self._backend and hasattr(self._backend, 'save'):
                return self._backend.save(trace)
            return None
            
except ImportError:
    class TraceStore:
        def __init__(self, *args, **kwargs): pass
        def save(self, trace): pass
