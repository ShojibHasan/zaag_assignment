import scrapy
from scrapy_splash import SplashRequest
import json


class CosmosidSpider(scrapy.Spider):
    name = "cosmosid"
    login_url = "https://app.cosmosid.com/sign-in"
    search_url = "https://app.cosmosid.com/search"
    start_urls = [login_url]

    lua_script = """
        function main(splash, args)
    splash:set_user_agent('...')
    assert(splash:go(args.url))
    assert(splash:wait(5))

    if not splash:select('[aria-label="close"]') then
        return {error = 'Close button not found', html = splash:html()}
    end

    assert(splash:select('[aria-label="close"]'):mouse_click())
    assert(splash:wait(1))
end
    """

    def start_requests(self):
        yield SplashRequest(
            url=self.login_url,
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.lua_script,
                'email': 'demo_estee2@cosmosid.com',
                'password': 'xyzfg321',
            }
        )

    def parse(self, response):
        if response.status == 200:
            self.log('Initial URL loaded successfully. Fetching search page...')
            # Use Lua script for the search page where JS content is dynamically loaded
            lua_script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(5))
                return {html = splash:html()}
            end
            """
            return SplashRequest(url='https://app.cosmosid.com/search',
                                 callback=self.parse_search,
                                 endpoint='execute',
                                 args={'lua_source': lua_script})

    def parse_search(self, response):
        self.log('Search page loaded successfully.')
        print(response.css('a'))
        for a in response.css('a'):
            yield {
                'url': a.css('::attr(href)').get(),
                'text': a.css('::text').get()
            }