import random
import time
import re
import os

from app.utils import (
    get_page_source,
    download_image
)


class MangaScraper(object):
    _CHAPTER_LIST = None
    _PREV_LINK = None

    _REL_LINK = False
    _ONE_PAGE = False

    _PROGRESS = {}

    def _get_abs_link(self, link):
        return '{}{}'.format(self._SITE_LINK, link)

    # TODO: Throw error if search_boundary failed
    # Return list of [aboslute link, name of series]
    def _get_re_match(self, page_source, re_compile, search_boundary=None):
        if search_boundary:
            u_b = page_source.find(search_boundary[0])
            l_b = page_source.find(search_boundary[1])
            results = re_compile.findall(page_source[u_b:l_b])
        else:
            results = re_compile.findall(page_source)

        return results

    def _get_re_match_dict(self, page_source, re_compile, search_boundary=None):
        if search_boundary:
            u_b = page_source.find(search_boundary[0])
            l_b = page_source.find(search_boundary[1])
            results = [m.groupdict() for m in re_compile.finditer(page_source[u_b:l_b])]
        else:
            results = [m.groupdict() for m in re_compile.finditer(page_source)]

        return results

    def _get_search_result(self, search_value, re_compile, search):
        url = self._SEARCH_LINK
        page_source = None

        if self._SEARCH_REST == 'get':
            page_source = get_page_source(url, get_values=search_value)

        if self._SEARCH_REST == 'post':
            page_source = get_page_source(url, post_values=search_value)

        re_compile = re.compile(re_compile, re.S)
        match_result = self._get_re_match_dict(page_source, re_compile, search)

        for match in match_result:
            match['title'] = match['title'].strip()

            if self._REL_LINK:
                match['url'] = self._get_abs_link(match['url'])

        return match_result

    def _get_series_info(self, url, values, search):
        page_source = get_page_source(url)
        upper_b = page_source.find(search[0])
        lower_b = page_source.find(search[1])
        page_source = page_source[upper_b:lower_b]

        for key in values:
            value = values[key]
            re_compile = re.compile(value, re.S)
            matches = self._get_re_match(page_source, re_compile)

            # What the hell is this?
            if len(matches) == 1:
                values[key] = re.sub(r'(<a.+?>|</a>|&nbsp;)', '', matches[0], 0, re.S)
            else:
                values[key] = ''

        return values

    def _gen_chapter_list(self, url, re_compile, search):
        # TODO: Necessary?
        # Test to see if it was the same url as last time
        # to prevent from generating chapter list again.
        if not self._PREV_LINK == url:
            self._PREV_LINK = url

            page_source = get_page_source(url)
            re_compile = re.compile(re_compile, re.S)
            match_result = self._get_re_match(page_source, re_compile, search)

            if self._REL_LINK:
                match_result = list(map(lambda x: list(x), match_result))

                for match in match_result:
                    match[0] = self._get_abs_link(match[0])

            self._CHAPTER_LIST = match_result

    def _get_all_chapters(self, link):
        self._gen_chapter_list(link)
        return self._CHAPTER_LIST

    # TODO: Might will need add re_compile
    def _find_chapter(self, link, chapter):
        self._gen_chapter_list(link)
        re_compile = re.compile(r'\b(?<!\.)(Ch\.)?0*{}(?!\.)\b'.format(chapter), re.S)
        chapter = list(filter(lambda x: re_compile.search(x[1]), self._CHAPTER_LIST))

        return chapter

    def _get_page_list(self, page_source, re_compile, search):
        re_compile = re.compile(re_compile, re.S)
        return self._get_re_match(page_source, re_compile, search)

    def _get_image(self, page_source, re_compile):
        re_compile = re.compile(re_compile, re.S)
        return self._get_re_match(page_source, re_compile)

    def _process_chapter(self, ch_num, ch_link, series_dir, series_name, pages=None):
        print('Downloading chapter #{} from {}'.format(ch_num, ch_link))

        ch_dir = '{}/{}'.format(series_dir, ch_num)

        if not os.path.exists(ch_dir):
            os.makedirs(ch_dir)

        page_source = get_page_source(ch_link)
        page_list = self._get_page_list(page_source)

        if series_name not in self._PROGRESS:
            self._PROGRESS[series_name] = {}

        if ch_num not in self._PROGRESS[series_name]:
            self._PROGRESS[series_name][ch_num] = {
                'progress': 0,
                'max': len(page_list)
            }

        for index, page in enumerate(page_list):
            # If index is not in pages, then skip.
            # For single page download
            if pages:
                if not index + 1 in pages:
                    continue

            if index != 0:
                time.sleep(random.uniform(1.5, 3.0))

                if not self._ONE_PAGE:
                    page_source = get_page_source(page)

            if self._ONE_PAGE:
                img_link = page
            else:
                img_link = self._get_image(page_source)[0]

            jpg = '{:02d}.jpg'.format(index + 1)
            file_dir = '{}/{}'.format(ch_dir, jpg)

            # print('  Chapter #{} - Started downloading page #{}.'.format(ch_num, i))

            download_image(img_link, file_dir)
            self._PROGRESS[series_name][ch_num]['progress'] = index + 1

            print('  Chapter #{} - Downloaded page #{}'.format(ch_num, index + 1))

        print('Done with chapter {}!'.format(ch_num))

        self._PROGRESS[series_name][ch_num]['progress'] = 'completed'

        return len(page_list)

    def _get_progress(self, ch_num, series_name):
        if series_name in self._PROGRESS:
            if ch_num in self._PROGRESS[series_name]:
                return self._PROGRESS[series_name][ch_num]

        return {'progress': 0, 'max': 0}

    def _del_progress(self, ch_num, series_name):
        del self._PROGRESS[series_name][ch_num]
