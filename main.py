from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup

async def open_site():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) # ИЗМЕНИТЬ НА FALSE ЕСЛИ НУЖНО ВИДЕТЬ БРАУЗЕР
        page = await browser.new_page()
        await page.goto("https://xmr.solopool.org/blocks", wait_until="networkidle")
        blocks_content = await page.content()
        await pull_the_link(blocks_content, 0)
        await page.goto("https://xmr.solopool.org/miners", wait_until="networkidle")
        miners_content = await page.content()
        await pull_the_link(miners_content, 1)
        await browser.close()

async def pull_the_link(content, s):
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find_all("tr")
    links = set()

    for row in rows:
        link_tag = row.find("a", href=lambda href: href and "/account/" in href)
        if link_tag and "/account/" in link_tag['href']:
            adress = link_tag['href'].split("/")[-1]
            links.add(adress)
    
    if s == 0:
        with open("solopool_blocks.txt", 'a') as f:
            for item in links:
                f.write(item + "\n")
    elif s == 1:
        with open("solopool_miners.txt", 'a') as f:
            for item in links:
                f.write(item + "\n")


if __name__ == "__main__":
    asyncio.run(open_site())
