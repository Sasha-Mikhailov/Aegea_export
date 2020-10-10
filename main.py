import os
from sqlalchemy import create_engine
import mysql.connector

from dotenv import load_dotenv

import pandas as pd


def connect_to_database():
    load_dotenv()
    # get data from .env file
    # password is stored separately for security reasons
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')

    con_string = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}'

    engine = create_engine(con_string)

    return engine


def get_aegea_data():
    engine = connect_to_database()

    BLOG_URL = os.environ.get('BLOG_URL')
    os.environ.clear()

    QUERY = f'''
        select notes.Title as title
            , CONCAT({BLOG_URL}, notes.OriginalAlias) as url
            , from_unixtime(notes.Stamp) as "date"
            , notes.Text as body
            , char_length(notes.Text) as text_len
            , coalesce(views.hits, 0) as hits
            , coalesce(comments.comments_count, 0) as comments
        from e2BlogNotes notes
        left join (select EntityID
                    , sum(HitCount) as hits
                from e2BlogActions
                group by 1) as views on views.EntityID = notes.ID
        left join (select NoteID
            , count(distinct ID) as comments_count
            from e2BlogComments
            group by 1) as comments on comments.NoteID = notes.ID
        '''

    return pd.read_sql(QUERY, engine)


def main():
    df = get_aegea_data()

    df.to_csv('aegea_export.csv', index=False)


if __name__ == '__main__':
    main()
