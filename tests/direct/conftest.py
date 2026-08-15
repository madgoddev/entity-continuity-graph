"""Windows compatibility shim for genlayer-test 0.29.2 direct mode.

The upstream loader successfully replaces fd 0, then attempts to unlink the
still-open temporary file. Windows rejects that unlink. Swallowing only that
post-injection PermissionError preserves the intended message-context setup;
the VM fixture restores fd 0 during teardown.
"""

from gltest.direct import loader


_original_inject = loader._inject_message_to_fd0


def _inject_message_windows_compatible(vm):
    try:
        _original_inject(vm)
    except PermissionError:
        # The exception is raised after fd 0 has already been injected.
        # VMContext._cleanup_after_deactivate restores the original descriptor.
        return None


loader._inject_message_to_fd0 = _inject_message_windows_compatible
