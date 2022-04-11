from app import db


class Markers(db.Model):
    __tablename__ = 'markers'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    name_infect = db.Column(db.String(255))
    marker = db.Column(db.Boolean)


    def __init__(self, name_infect, marker):
        self.name_infect = name_infect
        self.marker = marker

    def json(self):
        return {
            'name_infect': self.name_infect,
            'marker': self.marker
        }

    @classmethod
    def find_marker(self, name_infect):
        try:
            marker = db.session.query(Markers.name_infect).filter(Markers.name_infect==name_infect).first()

            if marker:
                return marker
            return None
        except Exception as e:
            print(e)

    def save_marker(self):
       try:

            db.session.add(self)
            db.session.commit()

       except Exception as e:
            print(e)