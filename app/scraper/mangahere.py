from app.scraper.common import MangaScraper


class MangaHereSC(MangaScraper):
    _NAME = 'MangaHere'
    _SITE_LINK = 'http://www.mangahere.co'
    _SEARCH_LINK = 'http://www.mangahere.co/search.php'
    _SEARCH_REST = 'get'

    def _get_search_result(self, search):
        values = {
          'name': search,
        }

        return super()._get_search_result(
            values,
            r'<a href="(?P<url>[^"]*).+?class="manga_info.+?rel="(?P<title>[^"]*)".*?</a>',
            ('result_search', '</table>')
        )

    def _get_series_info(self, url):
        values = {
            'altname': r'<label>Alternative Name:</label>([^<]*)</li>',
            'img': r'<img.*?src="([^"]*)".*?class="img"',
            'genre': r'<label>Genre\(s\):</label>([^<]*)</li>',
            'authors': r'<label>Author\(s\):</label>(.*?)<li>',
            'artists': r'<label>Artist\(s\):</label>(.*?)<li>',
            'status': r'<label>Status:</label>(.*?)</li>',
            'summary': r'id="show".*?>(.*?)&nbsp'
        }

        return super()._get_series_info(
            url,
            values,
            ('mr316', 'detail_list')
        )

    def _gen_chapter_list(self, link):
        super()._gen_chapter_list(
            link,
            r'<span class="left">.*?<a.+?href="([^"]*)".*?>([^<]*)</a>',
            ('detail_list', 'all_commet')
        )

    def _get_page_list(self, page_source):
        return super()._get_page_list(
            page_source,
            r'<option.+?value="([^"]*)".+?</option>',
            ('wid60', 'read_img')
        )

    def _get_image(self, page_source):
        return super()._get_image(
            page_source,
            r'<img.+?src="([^"]*)".+?id="image".*?>'
        )
