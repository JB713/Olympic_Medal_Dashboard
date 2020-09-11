import pandas as pd
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, MetaData, Table, join, outerjoin
from config import connection_string


class Services():

    def __init__(self):
        self.engine = create_engine(connection_string)
        self.connection_string = connection_string
        self.inspector = inspect(self.engine)
        self.tables = self.inspector.get_table_names()
        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)
        self.Medal = self.Base.classes['medal']
        self.Country = self.Base.classes['country']
        self.Athlete = self.Base.classes['athlete']
        self.Master = self.Base.classes['master_olympics']
        self.Event = self.Base.classes['event']
        self.meta = MetaData()

    def get_medals(self):
        session = Session(self.engine)

        results = session.query(self.Medal)
        df = pd.read_sql(results.statement, session.connection())
        session.close()

        return df.to_dict(orient='records')

    def get_countries(self):
        session = Session(self.engine)

        results = session.query(self.Country)
        df = pd.read_sql(results.statement, session.connection())
        session.close()

        return df.to_dict(orient='records')

    def get_country_info_by_name(self, country_name):
        session = Session(self.engine)

        country_result = session.query(self.Country).filter(self.Country.Country == country_name)

        df = pd.read_sql(country_result.statement, session.connection())
        session.close()

        return df.to_dict(orient='records')

    def get_countries_medals_count(self):
        session = Session(self.engine)

        results = session.query(self.Country, self.Medal, self.Master, self.Athlete).filter(self.Country.country_id == self.Athlete.country_id, self.Athlete.Athlete_id == self.Master.Athlete_id, self.Master.medal_id == self.Medal.medal_id)
        df = pd.read_sql(results.statement, session.connection())
        session.close()

        return df.to_dict(orient='records')


if __name__ == '__main__':
    info = Services()
