import pandas as pd
import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, MetaData, desc, func, asc
from config import connection_string


class Services:

    def __init__(self):
        self.connection_string = os.environ.get('HEROKU_POSTGRESQL_NAVY_URL', '') or connection_string

        self.engine = create_engine(self.connection_string)
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

    def get_all_data(self):
        session = Session(self.engine)

        results = session.query(self.Country, self.Medal, self.Master, self.Athlete, self.Event).filter(
            self.Country.country_id == self.Athlete.country_id, self.Athlete.athlete_id == self.Master.athlete_id,
            self.Master.medal_id == self.Medal.medal_id, self.Event.event_id == self.Master.event_id)
        df = pd.read_sql(results.statement, session.connection())
        session.close()
        return df

    def get_country_codes(self):
        df = self.get_all_data()
        gender_df = df[['Year', 'Code', 'Medal', 'Gender']]
        gender_df_2 = gender_df.loc[gender_df['Year'] > 1992]
        gender_medal_df = gender_df_2.groupby(['Year', 'Code', 'Gender']).count().reset_index()
        gender_medal_df2 = gender_medal_df.drop_duplicates()
        gender_medal_df3 = gender_medal_df2.groupby(["Code", "Year"]).filter(
            lambda x: (x["Gender"] == "Men").any() and (x["Gender"] == "Women").any())
        gender_medal_female = gender_medal_df3.loc[gender_medal_df2["Gender"] == "Women"]
        unique_contcodes = gender_medal_female['Code'].unique()

        return unique_contcodes.tolist()

    def gender_medal_dict(self):
        df = self.get_all_data()
        gender_df = df[['Year', 'Code', 'Medal', 'Gender']]
        gender_df_2 = gender_df.loc[gender_df['Year'] > 1992]
        gender_medal_df = gender_df_2.groupby(['Year', 'Code', 'Gender']).count().reset_index()
        gender_medal_df2 = gender_medal_df.drop_duplicates()
        gender_medal_df3 = gender_medal_df2.groupby(["Code", "Year"]).filter(
            lambda x: (x["Gender"] == "Men").any() and (x["Gender"] == "Women").any())
        gender_medal_male = gender_medal_df3.loc[gender_medal_df2["Gender"] == "Men"]
        gender_medal_female = gender_medal_df3.loc[gender_medal_df2["Gender"] == "Women"]
        gender_medal_male = gender_medal_male.rename(columns={'Medal': 'Male_Medal'})
        gender_medal_male["period"] = gender_medal_male['Year'].astype(str) + gender_medal_male['Code']
        gender_medal_female = gender_medal_female.rename(columns={'Medal': 'Female_Medal'})
        gender_medal_female["period"] = gender_medal_female['Year'].astype(str) + gender_medal_female['Code']
        df_gender_merged = pd.merge(gender_medal_female, gender_medal_male, on='period', how='inner')
        clean_df = df_gender_merged.drop(columns=['Code_y', 'Gender_x', 'Gender_y', 'period', 'Year_y', 'Gender_y'])
        clean_df = clean_df.rename(columns={'Year_x': 'Year', 'Code_x': 'Code'})
        group = clean_df.groupby("Code")
        istedigimiz_dict = {}
        for key, item in group:
            istedigimiz_dict[key] = {'Year': item.Year.values.tolist(),
                                     'Male_Medal': item.Male_Medal.values.tolist(),
                                     'Female_Medal': item.Female_Medal.values.tolist()}
        return istedigimiz_dict

    # Population Medals
    def get_countries_medals_count_population(self):
        session = Session(self.engine)
        results = session.query(
            self.Country.Country,
            func.count(self.Medal.medal_id).label("medals_count"),
            self.Country.Population,
            (self.Country.Population / func.count(self.Medal.medal_id)).label("medals_by_population")
        ).filter(
            self.Country.country_id == self.Athlete.country_id,
            self.Athlete.athlete_id == self.Master.athlete_id,
            self.Master.medal_id == self.Medal.medal_id,
            self.Event.event_id == self.Master.event_id,
            self.Event.Year.between(1993, 2015),
            self.Country.Population.isnot(None)
        ).group_by(
            self.Country.country_id
        ).order_by(
            asc("medals_by_population")
        )

        df = pd.read_sql(results.statement, session.connection())
        session.close()

        return df.to_dict(orient='records')

    def get_medal_count_by_country_and_year(self):
        session = Session(self.engine)

        results = session.query(
            self.Country.Country,
            self.Country.Code,
            self.Event.Year,
            func.count(self.Medal.medal_id).label("medals_count"),
            self.Country.latitude,
            self.Country.longitude
        ).filter(
            self.Country.country_id == self.Athlete.country_id,
            self.Athlete.athlete_id == self.Master.athlete_id,
            self.Master.medal_id == self.Medal.medal_id,
            self.Event.event_id == self.Master.event_id
        ).group_by(
            self.Country.country_id,
            self.Event.Year
        ).order_by(
            desc("medals_count")
        )

        df = pd.read_sql(results.statement, session.connection())

        session.close()

        return df.to_dict(orient='records')

    def get_country_medals(self, country_name):
        session = Session(self.engine)

        results = session.query(
            self.Country.Country,
            self.Medal.Medal,
            func.count(self.Medal.medal_id).label("medals_count")
        ).filter(
            self.Country.country_id == self.Athlete.country_id,
            self.Athlete.athlete_id == self.Master.athlete_id,
            self.Master.medal_id == self.Medal.medal_id,
            self.Event.event_id == self.Master.event_id,
            self.Country.Country == country_name
        ).group_by(
            self.Country.country_id,
            self.Medal.medal_id
        ).order_by(
            self.Country.Country,
            self.Medal.importance
        )

        df = pd.read_sql(results.statement, session.connection())

        session.close()

        return df.to_dict(orient='records')

    def get_medal_count_total_by_country(self):
        session = Session(self.engine)

        results = session.query(
            self.Country.Country,
            self.Country.latitude,
            self.Country.longitude,
            func.count(self.Medal.medal_id).label("medals_count")
        ).filter(
            self.Country.country_id == self.Athlete.country_id,
            self.Athlete.athlete_id == self.Master.athlete_id,
            self.Master.medal_id == self.Medal.medal_id,
            self.Event.event_id == self.Master.event_id
        ).group_by(
            self.Country.country_id
        ).order_by(
            self.Country.Country
        )

        df = pd.read_sql(results.statement, session.connection())

        session.close()

        return df.to_dict(orient='records')


if __name__ == '__main__':
    info = Services()
