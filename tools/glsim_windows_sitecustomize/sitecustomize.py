"""Process-start compatibility patch for GLSim on Windows.

genlayer-test 0.29.2 injects GenLayer message data into fd 0 successfully,
then Windows refuses to unlink that still-open temporary file. The server would
otherwise report a rollback before contract code executes.
"""

try:
    from gltest.direct import loader

    _original_inject = loader._inject_message_to_fd0

    def _inject_message_windows_compatible(vm):
        try:
            _original_inject(vm)
        except PermissionError:
            return None

    loader._inject_message_to_fd0 = _inject_message_windows_compatible
    # GLSim needs the actual contract class for schema and class caching.
    # The direct-test proxy is useful in pytest but hides that class from
    # glsim 0.29.2, causing an empty ABI and an invalid cached proxy class.
    loader._make_contract_proxy = lambda instance: instance
except ImportError:
    pass
