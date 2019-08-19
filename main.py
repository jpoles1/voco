"""Voco adapter and notifier for Mozilla WebThings Gateway."""

from os import path
import functools
import gateway_addon
import signal
import sys
import time

import threading
import queue

sys.path.append(path.join(path.dirname(path.abspath(__file__)), 'lib'))

from pkg.voco_adapter import VocoAdapter  # noqa

_API_VERSION = {
    'min': 2,
    'max': 2,
}
_ADAPTER = None



print = functools.partial(print, flush=True)


def cleanup(signum, frame):
    """Clean up any resources before exiting."""
    if _ADAPTER is not None:
        _ADAPTER.close_proxy()
    sys.exit(0)


if __name__ == '__main__':
    if gateway_addon.API_VERSION < _API_VERSION['min'] or \
            gateway_addon.API_VERSION > _API_VERSION['max']:
        print('Unsupported API version.')
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    print("starting adapter")
    _ADAPTER = VocoAdapter(verbose=True)
    print("Adapter started, beyond init.")
    # Wait until the proxy stops running, indicating that the gateway shut us
    # down.
    while _ADAPTER.proxy_running(): # and _ADAPTER2.proxy_running()
        time.sleep(2)
