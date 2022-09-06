"""Webhook file."""
import asyncio
import aiohttp
import xmltodict


class Config(object):
    """Config class."""

    def __init__(self):
        # Discord related stuff below
        self.name = 'Example webhook'
        self.channel_id = '123456789012345678'
        self.token = '2944923849238372913921849758973128973218957893210749802315214-123456'
        self.avatar = '4929394048fd93944929394048fd9394'
        self.guild_id = '482939203815724551'
        self._id = '489205812349512432'
        self.webhook_url = ''
        # RSS related stuff below
        self.feed_url = 'https://www.archlinux.org/feeds/packages/'


async def get_feed_from_rss(session, url):
    async with session.get(url) as rss_response:
        feed = await rss_response.text()
        return xmltodict.parse(feed, process_namespaces=True)


async def send_news_via_discord(session, url, data):
    await session.post(url, json=data)


async def main():
    last_package = open('last_package.txt', 'r+')
    config = Config()
    async with aiohttp.ClientSession() as session:
        feed = await get_feed_from_rss(session, config.feed_url)
        feed = feed['rss']['channel']
        for news in feed['item']:
            last_package.seek(0)
            if news['title'] in last_package.readline():
                last_package.seek(0)
                last_package.truncate()
                last_package.write(feed['item'][0]['title'])
                last_package.close()
                break
            else:
                data = {
                    'content': f'New update: {news["title"]}',
                    'name': config.name,
                    'avatar': config.avatar,
                    'channel_id': config.channel_id,
                    'guild_id': config.guild_id,
                    'id': config._id,
                    'token': config.token,
                }
                await send_news_via_discord(session, config.webhook_url, data)
                

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
