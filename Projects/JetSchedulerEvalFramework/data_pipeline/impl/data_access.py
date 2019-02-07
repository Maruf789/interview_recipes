import os
import pandas as pd
import sqlite3
from sqlite3 import Error


class DataAccess:
    """Static Class exposing static methods to access and load data from different Db"""

    def __init__(self):
        pass

    @staticmethod
    def load_from_csv(csv_file_full_path,
                      list_of_columns=None,
                      sep=","
                      ):
        """Loads data from a csv file
        :param csv_file_full_path
        :param list_of_columns (optional)
        :param sep (optional)
        :return Pandas DataFrame
        """
        assert os.path.isfile(csv_file_full_path)

        try:
            return pd.read_csv(csv_file_full_path, sep, header=None, names=list_of_columns)
        except NameError as e:
            print("File Not Found.", e)
        except Exception as ex:
            print(ex)

        return pd.DataFrame()

    @staticmethod
    def load_from_sql(db_file,
                      sql_query
                      ):
        """
        Connects to SQL and loads data into Pandas DataFrame.
        :param db_file
        :param sql_query
        :return: Pandas DataFrame
        """
        df = pd.DataFrame()

        try:

            conn = sqlite3.connect(db_file)
            df = pd.read_sql_query(sql_query, conn)
            conn.close()
        except Error as e:
            print(e)

        return df

