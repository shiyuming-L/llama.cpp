import pytest
import re
from utils import *

server: ServerProcess

@pytest.fixture(autouse=True)
def create_server():
    global server
    server = ServerPreset.tinyllama2()
    server.server_port = 8082
    server.n_slots = 1
    server.n_ctx = 8192
    server.n_batch = 2048


TOOL_CALL_PATTERN = re.compile(r'^[A-Za-z0-9]{32}$')


def test_tool_call_id_format():
    """Tool call IDs should be 32-character alphanumeric strings."""
    global server
    server.start()

    body = server.make_any_request("POST", "/v1/chat/completions", data={
        "max_tokens": 128,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Call the test tool with success=true"},
        ],
        "tool_choice": "required",
        "tools": [{
            "type": "function",
            "function": {
                "name": "test",
                "description": "A test function",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "const": True,
                        },
                    },
                    "required": ["success"],
                },
            },
        }],
        "parallel_tool_calls": False,
        "temperature": 0.0,
        "top_k": 1,
    })

    choice = body["choices"][0]
    tool_calls = choice["message"].get("tool_calls")
    assert tool_calls is not None and len(tool_calls) == 1, f"Expected 1 tool call, got {choice['message']}"

    tool_call = tool_calls[0]
    tool_call_id = tool_call.get("id", "")
    assert len(tool_call_id) > 0, f"Tool call ID should not be empty: {tool_call}"
    assert TOOL_CALL_PATTERN.match(tool_call_id), \
        f"Tool call ID should be 32 alphanumeric chars, got: {tool_call_id}"


def test_tool_call_id_unique():
    """Multiple tool calls should have unique IDs."""
    global server
    server.start()

    body = server.make_any_request("POST", "/v1/chat/completions", data={
        "max_tokens": 256,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Call multiple tools."},
            {"role": "user", "content": "Call both test tools"},
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "test_a",
                    "description": "Test function A",
                    "parameters": {
                        "type": "object",
                        "properties": {"input": {"type": "string"}},
                        "required": ["input"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "test_b",
                    "description": "Test function B",
                    "parameters": {
                        "type": "object",
                        "properties": {"input": {"type": "string"}},
                        "required": ["input"],
                    },
                },
            },
        ],
        "temperature": 0.0,
        "top_k": 1,
    })

    choice = body["choices"][0]
    tool_calls = choice["message"].get("tool_calls")

    if tool_calls and len(tool_calls) > 1:
        ids = [tc.get("id", "") for tc in tool_calls]
        assert len(ids) == len(set(ids)), f"Tool call IDs should be unique, got: {ids}"


def test_tool_call_id_in_streaming():
    """Tool call IDs should be present in streaming responses."""
    global server
    server.start()

    collected_id = None
    for chunk in server.make_stream_request("POST", "/v1/chat/completions", data={
        "max_tokens": 128,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Call the test tool"},
        ],
        "tool_choice": "required",
        "tools": [{
            "type": "function",
            "function": {
                "name": "test",
                "description": "A test function",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "const": True},
                    },
                    "required": ["success"],
                },
            },
        }],
        "stream": True,
        "temperature": 0.0,
        "top_k": 1,
    }):
        if chunk.get("choices"):
            choice = chunk["choices"][0]
            delta = choice.get("delta", {})
            tool_calls = delta.get("tool_calls", [])
            for tc in tool_calls:
                if tc.get("id"):
                    collected_id = tc["id"]

    assert collected_id is not None, "Should have received a tool call ID in stream"
    assert TOOL_CALL_PATTERN.match(collected_id), \
        f"Streamed tool call ID should be 32 alphanumeric chars, got: {collected_id}"
