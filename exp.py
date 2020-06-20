import asyncio
from pyppeteer import launch


async def main():
    browser = await launch()
    page = await browser.newPage()

    await page.goto('https://www.youtube.com/channel/UCMXHtrkazQjeCOteE4sof8gj/playlists')
    await page.screenshot({'path': 'youtube1.png'})

    await page.goto('https://www.youtube.com/playlist?list=PLyIFQr1wryPLLpctn9JLqZzUiDN1vnzYu00')
    await page.screenshot({'path': 'youtube2.png'})

    await page.goto('https://www.youtube.com/playlist?list=PLyIFQr1wryPLLpctn9JLqZzUiDN1vnzYu')
    await page.screenshot({'path': 'youtube3.png'})

    await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())