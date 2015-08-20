from flask import (
    send_from_directory,
    make_response,
    request
)
from sqlalchemy.sql.expression import ClauseElement
from config import MANGA_DIR

import json
import os

from app.scraper import gen_scrapers
from app.utils import download_image
from app import app, db, models

sites = gen_scrapers()


def valid_post_data(request, values):
    if not request.json:
        return False

    for value in values:
        if value not in request.json:
            return False

    return True


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


@app.route('/cdn/<path:filename>')
def custom_static(filename):
    return send_from_directory(MANGA_DIR, filename)


@app.route('/')
@app.route('/<path:p>')
def index(p=""):
    return make_response(open('app/static/index.html').read())


@app.route('/search')
@app.route('/search/<query>')
def search(query=""):
    # search_results = {"MangaHere": [{"url": "http://www.mangahere.co/manga/11_eyes/", "title": "11 eyes"}, {"url": "http://www.mangahere.co/manga/3x3_eyes/", "title": "3x3 Eyes"}, {"url": "http://www.mangahere.co/manga/b_eyes/", "title": "B-Eyes"}, {"url": "http://www.mangahere.co/manga/black_eyed_witch/", "title": "Black Eyed Witch"}, {"url": "http://www.mangahere.co/manga/blue_eyes_hoshino_lily/", "title": "Blue Eyes (HOSHINO Lily)"}, {"url": "http://www.mangahere.co/manga/cat_eyed_boy/", "title": "Cat Eyed Boy"}, {"url": "http://www.mangahere.co/manga/cat_s_eye/", "title": "Cat's Eye"}, {"url": "http://www.mangahere.co/manga/citrus_eyes/", "title": "Citrus Eyes"}, {"url": "http://www.mangahere.co/manga/close_your_eyes_hidaka_shoko/", "title": "Close Your Eyes (HIDAKA Shoko)"}, {"url": "http://www.mangahere.co/manga/close_your_eyes_inariya_fusanosuke/", "title": "Close Your Eyes (INARIYA Fusanosuke)"}, {"url": "http://www.mangahere.co/manga/cristo_orange_eyed_messiah/", "title": "Cristo ~ Orange-Eyed Messiah"}, {"url": "http://www.mangahere.co/manga/cry_eye/", "title": "Cry Eye"}, {"url": "http://www.mangahere.co/manga/dark_eyes/", "title": "Dark Eyes"}, {"url": "http://www.mangahere.co/manga/dragon_eye/", "title": "Dragon Eye"}, {"url": "http://www.mangahere.co/manga/eye_level/", "title": "Eye Level"}, {"url": "http://www.mangahere.co/manga/eyed_soul/", "title": "Eyed Soul"}, {"url": "http://www.mangahere.co/manga/eyeshield_21/", "title": "Eyeshield 21"}, {"url": "http://www.mangahere.co/manga/fisheye_placebo/", "title": "Fisheye Placebo"}, {"url": "http://www.mangahere.co/manga/golden_eyes/", "title": "Golden Eyes"}, {"url": "http://www.mangahere.co/manga/gravity_eyes/", "title": "Gravity Eyes"}], "MangaTown": [{"url": "http://www.mangatown.com/manga/11_eyes/", "title": "11 eyes"}, {"url": "http://www.mangatown.com/manga/3x3_eyes/", "title": "3x3 Eyes"}, {"url": "http://www.mangatown.com/manga/b_eyes/", "title": "B-Eyes"}, {"url": "http://www.mangatown.com/manga/black_eyed_witch/", "title": "Black Eyed Witch"}, {"url": "http://www.mangatown.com/manga/blue_eyes_hoshino_lily/", "title": "Blue Eyes (HOSHINO Lily)"}, {"url": "http://www.mangatown.com/manga/cat_eyed_boy/", "title": "Cat Eyed Boy"}, {"url": "http://www.mangatown.com/manga/cat_s_eye/", "title": "Cat's Eye"}, {"url": "http://www.mangatown.com/manga/citrus_eyes/", "title": "Citrus Eyes"}, {"url": "http://www.mangatown.com/manga/close_your_eyes_hidaka_shoko/", "title": "Close Your Eyes (HIDAKA Shoko)"}, {"url": "http://www.mangatown.com/manga/close_your_eyes_inariya_fusanosuke/", "title": "Close Your Eyes (INARIYA Fusanosuke)"}, {"url": "http://www.mangatown.com/manga/cristo_orange_eyed_messiah/", "title": "Cristo ~ Orange-Eyed Messiah"}, {"url": "http://www.mangatown.com/manga/cry_eye/", "title": "Cry Eye"}, {"url": "http://www.mangatown.com/manga/dark_eyes/", "title": "Dark Eyes"}, {"url": "http://www.mangatown.com/manga/dragon_eye/", "title": "Dragon Eye"}, {"url": "http://www.mangatown.com/manga/eye_level/", "title": "Eye Level"}, {"url": "http://www.mangatown.com/manga/eyed_soul/", "title": "Eyed Soul"}, {"url": "http://www.mangatown.com/manga/eyeshield_21/", "title": "Eyeshield 21"}, {"url": "http://www.mangatown.com/manga/fisheye_placebo/", "title": "Fisheye Placebo"}, {"url": "http://www.mangatown.com/manga/golden_eyes/", "title": "Golden Eyes"}, {"url": "http://www.mangatown.com/manga/gravity_eyes/", "title": "Gravity Eyes"}], "sites": ["KissManga", "MangaHere", "MangaTown"], "KissManga": [{"url": "http://kissmanga.com/Manga/11-Eyes", "title": "11 Eyes"}, {"url": "http://kissmanga.com/Manga/3-Years", "title": "3 Years"}, {"url": "http://kissmanga.com/Manga/31-Ai-Dream", "title": "31 Ai Dream"}, {"url": "http://kissmanga.com/Manga/3x3-Eyes", "title": "3x3 Eyes"}, {"url": "http://kissmanga.com/Manga/9-Faces-of-Love", "title": "9 Faces of Love"}, {"url": "http://kissmanga.com/Manga/Appearance-of-the-Yellow-Dragon", "title": "Appearance of the Yellow Dragon"}, {"url": "http://kissmanga.com/Manga/B-Eyes", "title": "B-Eyes"}, {"url": "http://kissmanga.com/Manga/Catch-Ai", "title": "Catch! Ai"}, {"url": "http://kissmanga.com/Manga/Cat-s-Eye", "title": "Cats Eye"}, {"url": "http://kissmanga.com/Manga/Cry-Eye", "title": "Cry Eye"}, {"url": "http://kissmanga.com/Manga/Eyed-Soul", "title": "Eyed Soul"}, {"url": "http://kissmanga.com/Manga/Eyeshield-21", "title": "Eyeshield 21"}, {"url": "http://kissmanga.com/Manga/Fisheye-Placebo", "title": "Fisheye Placebo"}, {"url": "http://kissmanga.com/Manga/Ghost-in-the-Shell-ARISE", "title": "Ghost in the Shell ARISE"}, {"url": "http://kissmanga.com/Manga/Glass-Shoes-IM-Hae-Yeon", "title": "Glass Shoes (IM Hae Yeon)"}, {"url": "http://kissmanga.com/Manga/Higurashi-no-Naku-Koro-ni-Kai-Meakashihen", "title": "Higurashi no Naku Koro ni Kai - Meakashihen"}, {"url": "http://kissmanga.com/Manga/Hitomi-kara-Destiny", "title": "Hitomi kara Destiny"}, {"url": "http://kissmanga.com/Manga/I-m-At-End-of-Your-Sight", "title": "Im At End of Your Sight"}, {"url": "http://kissmanga.com/Manga/Invincible-Yeonbyeongeol", "title": "Invincible Yeonbyeongeol"}, {"url": "http://kissmanga.com/Manga/Izayoi-no-Hitomi", "title": "Izayoi no Hitomi"}, {"url": "http://kissmanga.com/Manga/Jagan-wa-Gachirin-ni-Tobu", "title": "Jagan wa Gachirin ni Tobu"}, {"url": "http://kissmanga.com/Manga/Jewelry-Eyes", "title": "Jewelry Eyes"}, {"url": "http://kissmanga.com/Manga/Kiiroi-Kaigan", "title": "Kiiroi Kaigan"}, {"url": "http://kissmanga.com/Manga/Kiss-wa-Me-ni-Shite", "title": "Kiss wa Me ni Shite"}, {"url": "http://kissmanga.com/Manga/Kuroorihime-to-Kawaki-no-Ou", "title": "Kuroorihime to Kawaki no Ou"}, {"url": "http://kissmanga.com/Manga/Mayuge-no-Kakudo-wa-45\u00b0-de", "title": "Mayuge no Kakudo wa 45\u00b0 de"}, {"url": "http://kissmanga.com/Manga/Megane-Ouji", "title": "Megane Ouji"}, {"url": "http://kissmanga.com/Manga/Midori-no-Me", "title": "Midori no Me"}, {"url": "http://kissmanga.com/Manga/Mushi-To-Medama-To-Teddybear", "title": "Mushi To Medama To Teddybear"}, {"url": "http://kissmanga.com/Manga/Nekomedou-Kokoro-Tan", "title": "Nekomedou Kokoro Tan"}, {"url": "http://kissmanga.com/Manga/Netsu-Shisen", "title": "Netsu Shisen"}, {"url": "http://kissmanga.com/Manga/Onikiri-Jyuzo", "title": "Onikiri Jyuzo"}, {"url": "http://kissmanga.com/Manga/Ookami-no-Dou", "title": "Ookami no Dou"}, {"url": "http://kissmanga.com/Manga/Orange-Yellow", "title": "Orange Yellow"}, {"url": "http://kissmanga.com/Manga/Paperweight-Eye", "title": "Paperweight Eye"}, {"url": "http://kissmanga.com/Manga/Photo-Kano-Your-Eyes-Only", "title": "Photo Kano - Your Eyes Only"}, {"url": "http://kissmanga.com/Manga/Red-Eyes", "title": "Red Eyes"}, {"url": "http://kissmanga.com/Manga/Ryuugan", "title": "Ryuugan"}, {"url": "http://kissmanga.com/Manga/Seiten-no-Hekigan", "title": "Seiten no Hekigan"}, {"url": "http://kissmanga.com/Manga/Shakugan-no-Shana", "title": "Shakugan no Shana"}, {"url": "http://kissmanga.com/Manga/Shinrei-Tantei-Yakumo-2009", "title": "Shinrei Tantei Yakumo"}, {"url": "http://kissmanga.com/Manga/Sonna-Me-de-Mite-Kure", "title": "Sonna Me de Mite Kure"}, {"url": "http://kissmanga.com/Manga/Sono-Me-Kuchi-hodo-ni", "title": "Sono Me, Kuchi hodo ni."}, {"url": "http://kissmanga.com/Manga/Sunaebo", "title": "Sunaebo"}, {"url": "http://kissmanga.com/Manga/Takeru", "title": "Takeru"}, {"url": "http://kissmanga.com/Manga/The-Yellow-Chair", "title": "The Yellow Chair"}, {"url": "http://kissmanga.com/Manga/Tonari-no-Megane-kun", "title": "Tonari no Megane-kun"}, {"url": "http://kissmanga.com/Manga/TV-Eye", "title": "TV Eye"}, {"url": "http://kissmanga.com/Manga/Xue-Ye-Zhi-Cheng", "title": "Xue Ye Zhi Cheng"}, {"url": "http://kissmanga.com/Manga/Yami-no-Purple-Eye", "title": "Yami no Purple Eye"}, {"url": "http://kissmanga.com/Manga/Yellow-Heart", "title": "Yellow Heart"}, {"url": "http://kissmanga.com/Manga/Yubi-to-Kuchibiru-to-Hitomi-no-Ijiwaru", "title": "Yubi to Kuchibiru to Hitomi no Ijiwaru"}]}
    search_results = {
        'sites': []
    }

    if query:
        for site in sites:
            result = site._get_search_result(query)
            search_results['sites'].append(site._NAME)
            search_results[site._NAME] = result

    return json.dumps(search_results)


@app.route('/series-info', methods=['POST'])
def series_info():
    if not valid_post_data(request, ['site', 'url']):
        return False

    data = request.json
    site = data['site']
    url = data['url']

    site = list(filter(
        lambda x: x._NAME == site,
        sites
    ))[0]

    return json.dumps(site._get_series_info(url))


@app.route('/add-series', methods=['POST'])
def add_series():
    if not valid_post_data(request, ['name', 'url', 'site']):
        return False

    data = request.json
    img = data['imgUrl']

    new_series = get_or_create(
        db.session,
        models.Series,
        name=data['name'],
        url=data['url'],
        site_name=data['site']
    )

    data = new_series[0].get_json()
    new_dir = MANGA_DIR + data['directory']

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    # If it is actually new - commit the db.session
    if(new_series[1]):
        db.session.commit()

    download_image(img, '{}/cover_art.jpg'.format(new_dir))

    return json.dumps(data)


@app.route('/get-series')
def get_series():
    series = models.Series.query.order_by(models.Series.name).all()
    ret = []

    for s in series:
        ret.append(s.get_json())

    return json.dumps(ret)


@app.route('/dir-accessible')
def dir_accessible():
    ret = {}

    try:
        if not os.path.exists(MANGA_DIR):
            os.makedirs(MANGA_DIR)
        if not os.access(MANGA_DIR, os.W_OK):
            ret = {
                "error": "accessible",
                "dir": MANGA_DIR
            }
    except PermissionError:
        ret = {
            "error": "permission",
            "dir": MANGA_DIR
        }
    except FileNotFoundError:
        ret = {
            "error": "notFound",
            "dir": MANGA_DIR
        }

    return json.dumps(ret)
