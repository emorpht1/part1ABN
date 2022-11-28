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
        DataManagement.insertTable(df_GDP, 'gdp_europe')

        df_GDP_and_age = DataManagement.getGDP_and_age()
        DataManagement.plot(df_GDP_and_age)

    except Exception as er:
        print("An exception occurred" + er)


    # load gdp data
    # process survey data
    # insert to mysql
    # retrieve data
    # plot data

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
