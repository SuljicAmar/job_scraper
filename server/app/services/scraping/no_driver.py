import asyncio

# import zendriver as zd
import nodriver as zd
import numpy as np
from ..jobs import add_unparsed_job
from ...cfg import config


async def main():
    cfg = config()
    browser = await zd.start()
    page = await browser.get(cfg["scrape"])

    search_area = await page.find("textarea", best_match=True)
    await page.wait(np.random.uniform(0.25, 1.5))
    await search_area.send_keys(cfg["query"])
    await page.wait(np.random.uniform(0.25, 2.25))

    search_button = await page.select(selector="input[type=submit]")
    await search_button.click()

    for iPage in range(2, 7):
        await page.wait(np.random.uniform(1.2, 4.25))
        all_links = await page.get_all_urls()
        clean_links = [i for i in all_links if site in i.lower()]
        add_unparsed_job(clean_links)

        next_page = await page.find(f"Page {iPage}")
        await page.wait(np.random.uniform(0.85, 10.25))
        await next_page.click()

    await browser.stop()


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
