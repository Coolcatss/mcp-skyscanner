import asyncio

from fastmcp import Client

import mcp_server


def raise_missing_captcha_redirect(*args, **kwargs):
    """Match the KeyError raised by the bundled client for Skyscanner's new 403 body."""
    raise KeyError("redirect_to")


def test_search_airports_classifies_current_captcha_response(monkeypatch):
    monkeypatch.setattr(
        mcp_server,
        "search_airports_workaround",
        raise_missing_captcha_redirect,
    )

    result = mcp_server.search_airports("LHR")

    assert result == {
        "error": "BannedWithCaptcha",
        "message": "Skyscanner blocked the request with CAPTCHA",
        "suggestion": "Try again later or use a proxy",
    }


def test_search_flights_classifies_current_captcha_response(monkeypatch):
    monkeypatch.setattr(
        mcp_server,
        "search_airports_workaround",
        raise_missing_captcha_redirect,
    )

    result = mcp_server.search_flights("LHR", "JFK", "2026-12-22")

    assert result == {
        "error": "BannedWithCaptcha",
        "message": "Skyscanner blocked the request with CAPTCHA",
        "suggestion": "Try again later or use a proxy",
    }


def test_search_airports_error_matches_declared_mcp_schema(monkeypatch):
    monkeypatch.setattr(
        mcp_server,
        "search_airports_workaround",
        raise_missing_captcha_redirect,
    )

    async def call_tool():
        async with Client(mcp_server.mcp) as client:
            return await client.call_tool("search_airports", {"query": "LHR"})

    result = asyncio.run(call_tool())

    assert result.data["error"] == "BannedWithCaptcha"
