import DataManagement




def test_load_csv():
    """Test if load_csv is working."""
    df = DataManagement.load_csv_as_df('ABN/data/survey_results_public.csv',
                                                          ['YearsCode', 'Country', 'Age'])
    count = len(df.index)
    assert count > 100, "Should have more than 100"

def test_survey_cleanising():
    """Test if the cleansing was done properly."""
    df_survey_results = DataManagement.load_csv_as_df('ABN/data/survey_results_public.csv',
                                                      ['YearsCode', 'Country', 'Age'])
    # cleanse survey data
    df_survey_results = DataManagement.cleanseSurvey(df_survey_results)
    df_U_18 = df_survey_results['Age'].where(df_survey_results['Age'] == 'Under 18 years old')
    assert (df_U_18.count().sum())==0, "U 18 text not removed in cleanising"

if __name__ == "__main__":
    test_load_csv()
    test_survey_cleanising()
    print("All Tests passed")