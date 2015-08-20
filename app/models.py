from app import db


def jsonify(self):
    blacklist = ['_sa_instance_state']
    ret = {}

    for key, value in self.__dict__.items():
        if key not in blacklist:
            ret[key] = value

    return ret


class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    directory = db.Column(db.String(256), unique=True)
    url = db.Column(db.String(512), unique=True)
    site_name = db.Column(db.String(64))

    def get_json(self):
        return jsonify(self)

    def __init__(self, name, url, site_name):
        self.name = name
        self.directory = '/{}'.format(name)
        self.url = url
        self.site_name = site_name

    def __repr__(self):
        return '<Series \'{}\'>'.format(self.name)


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16))
    directory = db.Column(db.String(256))
    url = db.Column(db.String(512))
    site_name = db.Column(db.String(64))
    max_pages = db.Column(db.Integer)
    read = db.Column(db.Boolean)
    downloaded = db.Column(db.Boolean)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    prev_chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    next_chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))

    def get_json(self):
        return jsonify(self)

    def __init__(self, number, directory, url, site_name):
        self.number = number
        self.directory = directory
        self.url = url
        self.site_name = site_name

    def __repr__(self):
        return '<Chapter \'{}\'>'.format(self.name)


class Options(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    properties = db.Column(db.String(256))

    def get_json(self):
        return jsonify(self)

    def __repr__(self):
        return '<Options \'{}\'>'.format(self.name)
