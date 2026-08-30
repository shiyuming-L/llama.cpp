import pytest
from utils import *

server = ServerPreset.tinyllama2()


@pytest.fixture(autouse=True)
def create_server():
    global server
    server = ServerPreset.tinyllama2()
    server.n_ctx = 512
    server.n_slots = 1
    server.n_predict = 128


def test_ctx_shift_discard_boundary():
    """Test that n_discard is properly bounded during context shift.

    Regression test for: https://github.com/ggml-org/llama.cpp/pull/24786
    The fix ensures n_discard is clamped to [0, n_left - 1].
    """
    global server
    server.enable_ctx_shift = True
    server.start()

    # Use a prompt that's close to the context size to trigger shifting
    # n_ctx = 512, n_slots = 1, so slot context = 512 tokens
    # We need a prompt that will fill the context and require shifting
    long_prompt = "Hello world " * 200  # ~600 tokens, exceeds 512

    res = server.make_request("POST", "/completion", data={
        "n_predict": 32,
        "prompt": long_prompt,
    })
    assert res.status_code == 200
    assert res.body["truncated"] is True


def test_ctx_shift_disabled_rejects_long_prompt():
    """When ctx_shift is disabled, prompts exceeding context should fail."""
    global server
    server.enable_ctx_shift = False
    server.start()

    long_prompt = "Hello world " * 200  # ~600 tokens, exceeds 512

    res = server.make_request("POST", "/completion", data={
        "n_predict": 32,
        "prompt": long_prompt,
    })
    assert res.status_code != 200
    assert "error" in res.body


def test_ctx_shift_with_n_discard_override():
    """Test that custom n_discard values are properly bounded."""
    global server
    server.enable_ctx_shift = True
    server.start()

    long_prompt = "Hello world " * 200

    # Test with a very large n_discard value - should be clamped
    res = server.make_request("POST", "/completion", data={
        "n_predict": 32,
        "prompt": long_prompt,
        "n_discard": 1000,  # intentionally larger than context
    })
    # Should not crash, server should handle gracefully
    assert res.status_code == 200


def test_ctx_shift_with_zero_n_discard():
    """Test that n_discard=0 falls back to default behavior (n_left / 2)."""
    global server
    server.enable_ctx_shift = True
    server.start()

    long_prompt = "Hello world " * 200

    res = server.make_request("POST", "/completion", data={
        "n_predict": 32,
        "prompt": long_prompt,
        "n_discard": 0,  # should use default: n_left / 2
    })
    assert res.status_code == 200
    assert res.body["truncated"] is True


def test_ctx_shift_preserves_coherence():
    """Test that context shifting produces valid output."""
    global server
    server.enable_ctx_shift = True
    server.n_predict = 64
    server.start()

    # Create a prompt that will require multiple shifts
    prompt = "The quick brown fox jumps over the lazy dog. " * 50

    res = server.make_request("POST", "/completion", data={
        "n_predict": 64,
        "prompt": prompt,
    })
    assert res.status_code == 200
    assert len(res.body["content"]) > 0
    assert res.body["truncated"] is True
