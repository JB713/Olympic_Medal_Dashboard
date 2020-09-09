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
        self.meta = MetaData()

    def get_medals(self):
        session = Session(self.engine)

        results = session.query(self.Medal)
        df = pd.read_sql(results.statement, session.connection())
        session.close()
        return df.to_dict(orient='records')


if __name__ == '__main__':
    info = Services()
