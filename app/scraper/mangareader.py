import re

from app.scraper.common import MangaScraper


class MangaReaderSC(MangaScraper):
    _NAME = 'MangaReader'
    _SITE_LINK = 'http://www.mangareader.net'
    _SEARCH_LINK = 'http://www.mangareader.net/search/'
    _CHAPTER_LIST = None
    _PREV_LINK = None

    def _get_search_result(self, search):
        values = {
          'w': search,
        }
        re_compile = re.compile(r'<a href="(.+?[^"])">(.+?[^<])</a>', re.S)
        search_boundary = ('mangaresults', 'authorresults')

        page_source = self._request_page_get(self._SEARCH_LINK, values)
        match_result = self._get_re_match(page_source, re_compile, search_boundary)

        # Since match_result is a list of tuples, we need to change it to
        # list of list due to immutable tuples
        # Necessary?!
        match_result = list(map(lambda x: list(x), match_result))

        # Due to relative link
        for match in match_result:
            match[0] = self._get_abs_link(match[0])

        return match_result

    def _gen_chapter_list(self, link):
        re_compile = re.compile(r'<a.+?href="([^"]*)".*?>([^<]*)</a>', re.S)
        search_boundary = ('listing', 'adfooter')

        page_source = self._request_page(link)
        match_result = self._get_re_match(page_source, re_compile, search_boundary)

        self._CHAPTER_LIST = match_result

    def _find_chapter(self, link, chapter):
        super()._find_chapter(link, chapter)

        re_compile = re.compile(r'\b(?<!\.)0*{}(?!\.)\b'.format(chapter), re.S)
        chapter = list(filter(lambda x: re_compile.search(x[1]), self._CHAPTER_LIST))

        return chapter
