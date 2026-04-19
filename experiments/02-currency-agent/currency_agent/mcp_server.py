"""Minimal MCP server that exposes a currency exchange-rate tool."""

import asyncio
import os

import httpx
from fastmcp import FastMCP

mcp = FastMCP("Currency MCP Server")


@mcp.tool()
def get_exchange_rate(
    currency_from: str = "USD",
    currency_to: str = "EUR",
    currency_date: str = "latest",
) -> dict:
    """Return exchange-rate data from frankfurter.app."""
    response = httpx.get(
        f"https://api.frankfurter.app/{currency_date}",
        params={"from": currency_from, "to": currency_to},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=int(os.getenv("PORT", "8080")),
        )
    )
