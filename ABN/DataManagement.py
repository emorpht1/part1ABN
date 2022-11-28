import pandas as pd
import pymysql
import country_converter as coco
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from urllib.parse import quote

def load_csv_as_df(file_name,column_names):
  """load data from csv using column names and return as dataframe"""
  print('loading csv: '+ file_name)
  result_df = pd.read_csv(file_name, header = 0, usecols=column_names)
  #remove empty data
  result_df.dropna(inplace=True)
  return result_df


def cleanseSurvey(df_survey):
  """custom cleansing for Survey"""
  print('### Cleansing Survey')
  # remove rows with 'Age' column as 'Prefer not to say'
  df_survey.drop(df_survey[df_survey['Age'] == 'Prefer not to say'].index, inplace=True)
  # duplicate age column (to create an integer field)
  df_survey['Age_range'] = df_survey.loc[:, 'Age']
  # start replacing texts to int
  df_survey.loc[df_survey['Age'] == 'Under 18 years old', 'Age'] = '17'
  df_survey.loc[df_survey['Age'] == '65 years or older', 'Age'] = '66'
  df_survey['Age'] = df_survey['Age'].str[:2]
  df_survey.loc[df_survey['YearsCode'] == 'Less than 1 year', 'YearsCode'] = '1'
  df_survey.loc[df_survey['YearsCode'] == 'More than 50 years', 'YearsCode'] = '51'
  #convert to int fields
  df_survey = df_survey.astype({"YearsCode": "int", "Age": "int"})
  #calculate the age at which a user starts coding
  df_survey['Started_coding_age'] = df_survey['Age'] - df_survey['YearsCode']
  # less than 4 age to start coding is unrealistic and incorrect data hence dropping
  df_survey.drop(df_survey[df_survey['Started_coding_age'] < 4].index, inplace=True)
  return df_survey

def cleanseGDP(df_gdp):
  """custom cleansing for GDP"""
  print('### Cleansing GDP')
  df_gdp['Country'] = df_gdp.geo.apply(lambda x: coco.convert(names=x, to='name_short', not_found=None))
  #convert to float
  df_gdp["OBS_VALUE"].astype("float")
  return df_gdp

def insertTable(df,table_name):
  """insert a df to mysql"""
  print('### inserting ' + table_name)
  pymysql.install_as_MySQLdb()
  # would store the connection string in a config in Databricks or atleast a text file. Would also do connection pooling, but leaving as it is due to time constraints
  engine = create_engine('mysql://root:%s@localhost:3306/abn' % quote('P@ssw0rd'))
  with engine.begin() as connection:
    df.to_sql(name=table_name, con=connection, if_exists='replace', index=False)


def getGDP_and_age():
  """custom sql query to retrieve data to plot"""
  print('### querying mysql')
  pymysql.install_as_MySQLdb()
  engine = create_engine('mysql://root:%s@localhost:3306/abn' % quote('P@ssw0rd'))
  with engine.begin() as connection:
   return pd.read_sql(
      "SELECT AVG(s.Started_coding_age) as 'Average coding started age', p.OBS_VALUE as GDP FROM `survey_results_public` s, `gdp_europe` p where s.Country=p.Country GROUP BY OBS_VALUE;",
      connection)

def plot(df):
  """Plot the df"""
  df.plot()
  plt.show()
