from app.scraper.kissmanga import KissMangaSC
from app.scraper.mangahere import MangaHereSC
from app.scraper.mangatown import MangaTownSC
# from scraper.mangareader import MangaReaderSC


_ALL_CLASSES = [
    klass
    for name, klass in globals().items()
    if name.endswith('SC')
]

_ALL_CLASSES.sort(key=lambda x: x._NAME)


def gen_scrapers():
    return [klass() for klass in _ALL_CLASSES]
