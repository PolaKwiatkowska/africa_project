import psycopg2
from psycopg2 import OperationalError
import pandas as pd
#import sqlalchemy
#from sqlalchemy import create_engine


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connection("postgres", "postgres", "postgres123", "127.0.0.1", "5432")


connection = create_connection("africa", "postgres", "postgres123", "127.0.0.1", "5432")

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

create_hypertension_table = """
CREATE TABLE IF NOT EXISTS hypertension (
  id SERIAL PRIMARY KEY,
  country TEXT NOT NULL, 
  iso TEXT NOT NULL,
  sex TEXT NOT NULL,
  year INTEGER,
  hypertension_prevalence REAL
)
"""

# execute_query(connection, create_hypertension_table)

create_diabetes_table = """
CREATE TABLE IF NOT EXISTS diabetes (
  id SERIAL PRIMARY KEY,
  country TEXT NOT NULL, 
  iso TEXT NOT NULL,
  sex TEXT NOT NULL,
  year INTEGER,
  diebetes_prevalence REAL
)
"""

create_bmi_table = """
CREATE TABLE IF NOT EXISTS bmi (
  id SERIAL PRIMARY KEY,
  country TEXT NOT NULL, 
  iso TEXT NOT NULL,
  sex TEXT NOT NULL,
  year INTEGER,
  bmi_mean REAL
)
"""

#execute_query(connection, create_diabetes_table)
#execute_query(connection, create_bmi_table)


    # helper function to load csv data
def load_data(csv_file):
    # read csv as data frame
    df = pd.read_csv(csv_file, delimiter = ';', decimal=",")
    df.rename(columns={"Country Name": "country", "Country Code": "code", "Indicator Name": "variable", "Indicator Code": "indicator" }, inplace = True)
     # changing data frame to clean data frame
    unpivoted_df = pd.melt(df, id_vars =['country', 'code', 'variable', 'indicator'], var_name ='year', value_name ='value')


    #correct Population, total, Egypt, Arab Rep.

    unpivoted_df['country'].replace({"Egypt, Arab Rep.": "Egypt"}, inplace=True)
    unpivoted_df['variable'].replace({"Population, total": "population"}, inplace=True)
    unpivoted_df['variable'].replace({"GDP per capita (current US$)": "gdp"}, inplace=True)
    unpivoted_df['variable'].replace({"Domestic general government health expenditure per capita, PPP (current international $)": "gov_exp"}, inplace=True)
    unpivoted_df['variable'].replace({"Domestic private health expenditure (% of current health expenditure)": "private_exp"}, inplace=True)
    unpivoted_df['variable'].replace({"Foreign direct investment, net inflows (BoP, current US$)": "for_dir_inv"}, inplace=True)

    # change year data type from object to int
    unpivoted_df.year = pd.to_numeric(unpivoted_df.year)

    # if year lower than 2000 - drop rows, if year hihger than 2014 drop rows

    cleaned_df = unpivoted_df[ (unpivoted_df['year'] <= 2014) & (unpivoted_df['year'] >= 2000)].reset_index()


    #assign name of data frame as variable

    # pick vaule form any variable and set it as variable
    name = unpivoted_df.iloc[0:1, 2].item()
    #generate a unique file name based on the id and record
    file_name = str(name) + ".csv"

    #create the CSV
    # ??? problem to solve how to define directory
    return cleaned_df.to_csv(file_name, index = False)

#load_data('/Users/pola/Documents/Africa Project/gdp_per_capita.csv')

create_gdp_table = """
CREATE TABLE IF NOT EXISTS gdp (
  id SERIAL PRIMARY KEY,
  index INTEGER,
  country TEXT NOT NULL, 
  code TEXT NOT NULL,
  variable TEXT NOT NULL,
  indicator TEXT NOT NULL,
  year INTEGER,
  value REAL
)
"""
#execute_query(connection, create_gdp_table)
#/Users/file_name


#??? porblem to solve --> how to import data frame directly to postgres
# engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')
#df.to_sql('table_name', engine)

#load_data('/Users/pola/Documents/Africa Project/population.csv')

create_population_table = """
CREATE TABLE IF NOT EXISTS population (
  id SERIAL PRIMARY KEY,
  index INTEGER,
  country TEXT NOT NULL, 
  code TEXT NOT NULL,
  variable TEXT NOT NULL,
  indicator TEXT NOT NULL,
  year INTEGER,
  value REAL
)
"""

#execute_query(connection, create_population_table)

#load_data('/Users/pola/Documents/Africa Project/Domestic general government health expenditure per capita.csv')

create_gov_exp_table = """
CREATE TABLE IF NOT EXISTS gov_exp (
  id SERIAL PRIMARY KEY,
  index INTEGER,
  country TEXT NOT NULL, 
  code TEXT NOT NULL,
  variable TEXT NOT NULL,
  indicator TEXT NOT NULL,
  year INTEGER,
  value REAL
)
"""

#execute_query(connection, create_gov_exp_table)

#load_data('/Users/pola/Documents/Africa Project/Domestic private health expenditure.csv')

create_private_exp_table = """
CREATE TABLE IF NOT EXISTS private_exp (
  id SERIAL PRIMARY KEY,
  index INTEGER,
  country TEXT NOT NULL, 
  code TEXT NOT NULL,
  variable TEXT NOT NULL,
  indicator TEXT NOT NULL,
  year INTEGER,
  value REAL
)
"""

#execute_query(connection, create_private_exp_table)

#load_data('/Users/pola/Documents/Africa Project/for_dir_inv.csv')

create_for_dir_inv_table = """
CREATE TABLE IF NOT EXISTS for_dir_inv (
  id SERIAL PRIMARY KEY,
  index INTEGER,
  country TEXT NOT NULL, 
  code TEXT NOT NULL,
  variable TEXT NOT NULL,
  indicator TEXT NOT NULL,
  year INTEGER,
  value REAL
)
"""

#execute_query(connection, create_for_dir_inv_table)