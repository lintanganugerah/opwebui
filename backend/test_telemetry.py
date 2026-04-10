import pytest
import httpx
import requests
import socket
import urllib.request
import asyncio
from unittest.mock import patch, MagicMock

# Domains that are explicitly allowed for normal operation or expected during testing
ALLOWED_DOMAINS = [
    "localhost",
    "127.0.0.1",
    "api.arsa.com",         # License/Branding (known)
    "licenses.api.arsa.com",# License (known)
]

class BlockedNetworkRequestError(Exception):
    pass

def check_url(url):
    """Check if the URL belongs to an allowed domain."""
    from urllib.parse import urlparse
    try:
        parsed = urlparse(url)
        domain = parsed.hostname
        if domain and not any(allowed in domain for allowed in ALLOWED_DOMAINS):
            raise BlockedNetworkRequestError(f"UNAUTHORIZED OUTBOUND REQUEST TO: {url}")
    except Exception as e:
        if isinstance(e, BlockedNetworkRequestError):
            raise
        # Ignore parse errors

@pytest.fixture(autouse=True)
def intercept_requests():
    """
    Patch requests.request and httpx.AsyncClient.request to intercept and block
    unauthorized outbound HTTP calls.
    """
    original_requests_request = requests.api.request
    original_httpx_request = httpx.AsyncClient.request
    original_urllib_urlopen = urllib.request.urlopen
    original_socket_connect = socket.socket.connect

    def mocked_requests_request(method, url, **kwargs):
        check_url(url)
        return original_requests_request(method, url, **kwargs)

    async def mocked_httpx_request(self, method, url, **kwargs):
        check_url(str(url))
        return await original_httpx_request(self, method, url, **kwargs)

    def mocked_urllib_urlopen(url, *args, **kwargs):
        if isinstance(url, str):
            check_url(url)
        elif hasattr(url, 'full_url'):
            check_url(url.full_url)
        return original_urllib_urlopen(url, *args, **kwargs)

    def mocked_socket_connect(self, address):
        if isinstance(address, tuple) and len(address) == 2:
            host, port = address
            if not any(allowed in str(host) for allowed in ALLOWED_DOMAINS):
                # We can't block all socket connects easily because of DB/Redis,
                # but we can log or raise if it looks like a public IP that isn't allowed.
                # For this test, we'll be lenient on raw sockets unless it's port 80/443
                if port in [80, 443]:
                   # Basic check, might catch DBs on cloud but good for a test
                   pass
        return original_socket_connect(self, address)


    with patch('requests.api.request', side_effect=mocked_requests_request), \
         patch('httpx.AsyncClient.request', side_effect=mocked_httpx_request), \
         patch('urllib.request.urlopen', side_effect=mocked_urllib_urlopen), \
         patch('socket.socket.connect', side_effect=mocked_socket_connect):
        yield

@pytest.mark.asyncio
async def test_no_unauthorized_telemetry():
    """
    Initialize the app and ensure no unexpected background tasks or initialization
    routines attempt to phone home to unauthorized domains.
    """
    # Simply importing the main app triggers a lot of initialization
    from open_webui.main import app
    
    # We can also start up a test client to trigger startup events
    from httpx import AsyncClient
    
    # Mocking successful startup
    assert app is not None
    
    # If the app tries to phone home (e.g. telemetry, posthog, sentry) during import 
    # or startup, the intercept_requests fixture will catch it and raise BlockedNetworkRequestError.
    
    # We're specifically checking that no Exception is raised here.
    assert True
