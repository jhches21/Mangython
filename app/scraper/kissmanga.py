from app.scraper.common import MangaScraper


class KissMangaSC(MangaScraper):
    _NAME = 'KissManga'
    _SITE_LINK = 'http://kissmanga.com'
    _SEARCH_LINK = 'http://kissmanga.com/Search/Manga'
    _SEARCH_REST = 'post'
    _REL_LINK = True
    _ONE_PAGE = True

    def _get_search_result(self, search):
        values = {
          'keyword': search,
          'selectSearch': 'Manga'
        }

        return super()._get_search_result(
            values,
            r'<a class="bigChar" href="(?P<url>[^"]*)">(?P<title>[^<]*)</a>',
            ('class="listing"', '</table>'),
        )

    def _get_series_info(self, url):
        values = {
            'altname': r'<span class="info">Other name:</span>(.*?)</p>',
            'img': r'<div id="rightside">.+?<img.+?src="([^"]*)"',
            'genre': r'<span class="info">Genres:</span>(.*?)</p>',
            'authors': r'<span class="info">Author:</span>(.*?)</p>',
            # 'artists': r'<label>Artist\(s\):</label><a.*?>([^<]*)</a>',
            'status': r'<span class="info">Status:</span>(.*?)<span',
            'summary': r'<span class="info">Summary:.+?<p.*?>(.*?)</p>'
        }

        return super()._get_series_info(
            url,
            values,
            ('id="container"', 'id="footer"')
        )

    def _gen_chapter_list(self, link):
        super()._gen_chapter_list(
            link,
            r'<a.+?href="([^"]*)".*?>([^<]*)</a>',
            ('class="listing"', '</table>')
        )

    # This scarper doesn't need _get_image() due to
    # page_list acting as full page of pictures.
    def _get_page_list(self, page_source):
        return super()._get_page_list(
            page_source,
            r'lstImages.push\("([^"]*)"\);',
            ('lstImages', 'lstImagesLoaded')
        )
