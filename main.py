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

    engine = None

    try:
        engine = create_engine(con_string)
        print('successfully connected to the database')
    except Exception as e:
        print('ERROR! cant connect to the database')
        print(e)

    return engine


def get_aegea_data():
    engine = connect_to_database()

    BLOG_URL = os.environ.get('BLOG_URL')
    os.environ.clear()

    QUERY = f'''
        select notes.Title as title
            , CONCAT("{BLOG_URL}", notes.OriginalAlias) as url
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

    df = pd.DataFrame()
    if engine:
        try:
            df = pd.read_sql(QUERY, engine)
            print(f'got {len(df)} rows from the database')
        except Exception as e:
            print('ERROR during fetching data from database')
            print(e)

    return df

def main():
    try:
        df = get_aegea_data()
    except Exception as e:
        print('ERROR unexpected')

    RESULT_FOLDER = 'output'
    RESULT_FNAME = 'aegea_export.csv'
    result_filepath = os.path.join(RESULT_FOLDER, RESULT_FNAME)

    os.makedirs(RESULT_FOLDER, exist_ok=True)

    if len(df) > 0:
        try:
            df.to_csv(result_filepath, index=False)
            print(f'successfully wrote file to {result_filepath}')
        except Exception as e:
            print(f'ERROR during writing the file with path {result_filepath}')


if __name__ == '__main__':
    main()
