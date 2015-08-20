from app.scraper.common import MangaScraper


class MangaTownSC(MangaScraper):
    _NAME = 'MangaTown'
    _SITE_LINK = 'http://www.mangatown.com'
    _SEARCH_LINK = 'http://www.mangatown.com/search.php'
    _SEARCH_REST = 'get'

    def _get_search_result(self, search):
        values = {
          'name': search,
        }

        return super()._get_search_result(
            values,
            r'<[P|p].+?class="title".+?href="(?P<url>[^"]*)".*?title="(?P<title>[^"]*)".*?</a>',
            ('search_result', 'wid300')
        )

    def _get_series_info(self, url):
        values = {
            'altname': r'<b>Alternative Name:</b>([^<]*)</li>',
            'img': r'<img.*?src="([^"]*)".*?<ul>',
            'genre': r'<b>Genre\(s\):</b>(.*?)</li>',
            'authors': r'<b>Author\(s\):</b>(.*?)</li>',
            'artists': r'<b>Artist\(s\):</b>(.*?)</li>',
            'status': r'<b>Status:</b>(.*?)</li>',
            'summary': r'id="show".*?>(.*?)&nbsp'
        }

        return super()._get_series_info(
            url,
            values,
            ('class="detail_info', 'class="chapter_content"')
        )

    def _gen_chapter_list(self, link):
        super()._gen_chapter_list(
            link,
            r'<a.+?href="([^"]*)".*?>([^<]*)</a>',
            ('chapter_list', 'comment_content')
        )

    def _get_page_list(self, page_source):
        return super()._get_page_list(
            page_source,
            r'<option.+?value="([^"]*)".+?</option>',
            ('page_select', 'id="viewer"')
        )

    def _get_image(self, page_source):
        return super()._get_image(
            page_source,
            r'<img.+?src="([^"]*)".+?id="image".*?>'
        )
