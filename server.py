import asyncio  
from playwright.async_api import async_playwright  
  
async def main():  
    async with async_playwright() as p:  
        browser = await p.chromium.launch()  
        page = await browser.new_page()  
          
        # 发送请求  
        await page.get("https://example.com")  
          
        # 关闭浏览器  
        await browser.close()  
  
asyncio.run(main())
