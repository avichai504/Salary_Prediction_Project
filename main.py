import pandas
import pandas as pd

import Data_Cleaning as dc
import Extract_from_text as et
import Glass_Door_Scraper_var0 as Sahar


def main_scraper():
    path = "C:/Users/avich/chromedriver"
    keyword = "software engineer Web development"
    keyword = "data analyst"
    keyword = "cyber"
    keyword = 'QA'

    num_jobs = 500
    max_sleep_time = 1

    list_keywords = [
        'Artificial Intelligence', 'Machine Learning engineer',
        'Data engineering'
        'DevOps', 'Cybersecurity', 'Data science and analytics', 'Augmented Reality', 'Robotics', 'Web development',
        'Internet of Things', 'Financial technology', 'HealthTech', 'E-commerce',
        'Enterprise software', 'Education technology', 'Social media and networking engineer']

    list_keywords = [
        'Data Scientist', 'Data Analyst', 'Machine Learning Engineer',
        'Data Engineer', 'Business Intelligence Analyst', 'Data Architect',
        'Statistician', 'Quantitative Analyst', 'Data Product Manager',
        'Research Scientist'
    ]


    columns = ['Job Title', 'Type of Ownership', 'Time Unit', 'Revenue', 'Company Size', 'Location']  # for one-hot encoding

    for i, keyword in enumerate(list_keywords):
        try:

            df = Sahar.get_jobs(keyword, num_jobs, path, max_sleep_time, 0)  # call to scraper

            df_clean = dc.data_cleaning(df)  # first clean: calculate the salary, fixing the location and more
            df_clean.to_csv(f"{i} {keyword} raw data.csv")

            df_clean = dc.one_hot_encoding(df_clean, columns)  # one-hot encoding process

            df_clean = dc.final_clean(df_clean)  # Removing all unnecessary columns and staying only with numeric values!
            df_clean.to_csv(f"{i} {keyword} final data.csv")


        except Exception as e:
            print("!!!!!!!!!!!!main exception!!!!!!!!!", e)


def unique_values():
    df1 = pandas.read_csv('data files/software engineer/0_Cloud computing.csv')
    df2 = pandas.read_csv('data files/software engineer/1_Mobile app development.csv')
    df3 = pandas.read_csv('data files/software engineer/0_Web development.csv')
    df4 = pandas.read_csv('data files/software engineer/2_Desktop software development.csv')
    df5 = pandas.read_csv('data files/software engineer/3_Game development.csv')

    dc.column_unique_values(df1, df2, df3, df4, df5, 'Sector', 'software engineer')


def main_one_hot_encoding():
    df = pandas.read_csv('data files/software engineer/software engineer.csv')
    column_names = ['Job Title', 'Type of Ownership', 'Time Unit', 'Revenue', 'Company Size', 'Location']
    df_one_hot_encoding = dc.one_hot_encoding(df, column_names)
    df_one_hot_encoding.to_csv(f"one_hot_encoding_software_engineer.csv")


def main_check_extract_from_text():
    with open('data files/raw text from job descriptions/row_text_data analyst20.txt', 'r') as f:
        text = f.read()
        result = et.nlp_for_years_of_experience(text)
        print(result)


def main_final_data():
    df = pd.read_csv('data files/software engineer/software engineer.csv')
    df = dc.data_cleaning(df)
    df.to_csv('EEEE.csv')


# main_final_data()
# unique_values()
main_scraper()
# main_one_hot_encoding()
# main_check_extract_from_text()
