from megamarket.queries import parse_products
from playwright import async_api

import asyncio

async def test_market_parse(url, browser):
    async for product in parse_products(url, browser):
        print("OK")
        
        
async def test_megamarket():
    async with async_api.async_playwright() as playwright:
        browser = await playwright.firefox.launch()
        for i in range(4):
            print(f"Client #{i} started!")
            asyncio.ensure_future(test_market_parse("https://megamarket.ru/catalog/avtomobilnye-kolonki/", browser))
        else:
            await test_market_parse("https://megamarket.ru/catalog/avtomobilnye-kolonki/", browser)