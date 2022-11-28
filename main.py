# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from ABN import DataManagement

def start():
    try:
        # load survey data
        df_survey_results = DataManagement.load_csv_as_df('ABN/data/survey_results_public.csv',
                                                          ['YearsCode', 'Country', 'Age'])
        # cleanse survey data
        df_survey_results = DataManagement.cleanseSurvey(df_survey_results)
        # store in mysql
        DataManagement.insertTable(df_survey_results, 'survey_results_public')
        # load gdp data
        df_survey_results = DataManagement.load_csv_as_df('ABN/data/nama_10_gdp_page_linear.csv',
                                                          ['geo','OBS_VALUE'])
        # cleanse GDP data
        df_GDP = DataManagement.cleanseGDP(df_survey_results)
        # insert to mysql
        DataManagement.insertTable(df_GDP, 'gdp_europe')
        # retrieve data from mysql
        df_GDP_and_age = DataManagement.getGDP_and_age()
        # plot data
        DataManagement.plot(df_GDP_and_age)

    except Exception as er:
        print("An exception occurred" + er)



if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
