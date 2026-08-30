import pytest
from utils import *

server = ServerPreset.tinyllama2()


@pytest.fixture(autouse=True)
def create_server():
    global server
    server = ServerPreset.tinyllama2()


def test_tools_endpoint_disabled_by_default():
    """When --tools is not set, /tools endpoints should return 403."""
    global server
    server.start()

    res = server.make_request("GET", "/tools")
    assert res.status_code == 403
    assert "error" in res.body
    assert res.body["error"]["type"] == "feature_disabled"
    assert res.body["error"]["message"] == "this feature is disabled"

    res = server.make_request("POST", "/tools", data={})
    assert res.status_code == 403
    assert "error" in res.body
    assert res.body["error"]["type"] == "feature_disabled"


def test_cors_proxy_disabled_by_default():
    """When --ui-mcp-proxy is not set, /cors-proxy should return 403."""
    global server
    server.start()

    res = server.make_request("GET", "/cors-proxy")
    assert res.status_code == 403
    assert "error" in res.body
    assert res.body["error"]["type"] == "feature_disabled"

    res = server.make_request("POST", "/cors-proxy", data={})
    assert res.status_code == 403
    assert "error" in res.body
    assert res.body["error"]["type"] == "feature_disabled"


def test_slots_disabled_returns_501():
    """When --no-slots is set, /slots should return 501."""
    global server
    server.server_slots = False
    server.start()

    res = server.make_request("GET", "/slots")
    assert res.status_code == 501
    assert "error" in res.body


def test_slots_enabled_returns_200():
    """When --slots is set, /slots should return 200 with slot info."""
    global server
    server.server_slots = True
    server.n_slots = 2
    server.start()

    res = server.make_request("GET", "/slots")
    assert res.status_code == 200
    assert len(res.body) == 2


def test_disabled_features_error_format():
    """Verify the error response format matches the expected schema."""
    global server
    server.start()

    res = server.make_request("GET", "/tools")
    assert res.status_code == 403

    error = res.body["error"]
    assert "message" in error
    assert "type" in error
    assert isinstance(error["message"], str)
    assert isinstance(error["type"], str)


@pytest.mark.parametrize("endpoint,method", [
    ("/tools", "GET"),
    ("/tools", "POST"),
    ("/cors-proxy", "GET"),
    ("/cors-proxy", "POST"),
])
def test_disabled_endpoints_consistent_error(endpoint: str, method: str):
    """All disabled feature endpoints should return consistent 403 errors."""
    global server
    server.start()

    if method == "GET":
        res = server.make_request("GET", endpoint)
    else:
        res = server.make_request("POST", endpoint, data={})

    assert res.status_code == 403
    assert res.body["error"]["type"] == "feature_disabled"
    assert res.body["error"]["message"] == "this feature is disabled"
