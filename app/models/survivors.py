from app import db
from sqlalchemy import create_engine
from sqlalchemy import text
from math import sqrt, radians, cos, acos, sin, pow, degrees
import os


class Survivors(db.Model):
    __tablename__ = 'survivors'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    gender = db.Column(db.String(20))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)


    def __init__(self, name, gender, lat, lon):
        self.name = name
        self.gender = gender
        self.lat = lat
        self.lon = lon

    def json(self):
        return {
            'name': self.name,
            'gender': self.gender,
            'lat': self.lat,
            'lon': self.lon
        }

    @classmethod
    def find_survivors(self, name):
        try:
            # Search survivors for name
            survivors = db.session.query(Survivors.name).filter(Survivors.name==name).first()

            #Case survivors exist return, case not return none
            if survivors:
                return survivors
            return None
        except Exception as e:
            print(e)

    @classmethod
    def find_survivor(cls, name):
        try:
            survivors = cls.query.filter_by(name=name).first()

            if survivors:
                return survivors
            return None
        except Exception as e:
            print(e)

    @classmethod
    def find_survivors_id(self, id):
        try:
            # Search survivors for id
            survivors = db.session.query(Survivors.name).filter(Survivors.id==id).first()

            #Case survivors exist return, case not return none
            if survivors:
                return survivors
            return None
        except Exception as e:
            print(e)

    def find_survivors_next(self, name):
        try:
            
            #This SQL, looks for the closest survivors
            usuario_out = []
            #sql_engine = create_engine('sqlite:///C://projetos-pythons//projeto-maxhost//app//banco.db', echo=False)
            sql_engine = create_engine('sqlite:///'+ os.path.abspath(os.path.expanduser(os.path.expandvars('app/'))) + '/banco.db', echo=False)
            raw_con = sql_engine.raw_connection()
            raw_con.create_function("cos", 1, cos)
            raw_con.create_function("acos", 1, acos)
            raw_con.create_function("sin", 1, sin)
            raw_con.create_function("radians", 1, radians)
            raw_con.create_function("sqrt", 1, sqrt)
            raw_con.create_function("pow", 1, pow)
            raw_con.create_function("degrees", 1, degrees)

            sql = "SELECT A.NAME AS NAME, B.NAME AS NAME_PROX, \
                                        (111.111 * degrees(ACOS(COS(RADIANS(a.Lat)) * COS(RADIANS(b.Lat)) * COS(RADIANS(a.Lon - b.Lon))  + SIN(RADIANS(a.Lat))  * SIN(RADIANS(b.Lat))))) \
                                        AS DISTANCE_KM  FROM SURVIVORS AS A  JOIN SURVIVORS AS B ON A.ID <> B.ID WHERE A.NAME = (?) ORDER BY DISTANCE_KM ASC LIMIT 0, 1"

            result = raw_con.execute(sql, (name,))

            for i in result.fetchall():
                usuario_out.append(i)

            return usuario_out
        except Exception as e:
            print(e)

    def save_survivors(self):
       try:
            db.session.add(self)
            db.session.commit()
       except Exception as e:
            print(e)

    def update_survivors(self, id, name, gender, lat, lon):
        try:
            #Update survivors
            db.session.query(Survivors).filter(Survivors.id==id).update({"name":name,
                                                                "gender": gender,
                                                                "lat": lat,
                                                                "lon": lon})
            db.session.commit()
        except Exception as e:
            print(e)