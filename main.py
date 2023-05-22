import pandas
import older_scraper2 as gs
import Data_Cleaning as dc
import Extract_from_text as et
import older_scraper as old
import Glass_Door_Scraper_var0 as Sahar


def main_scraper():
    path = "C:/Users/avich/chromedriver"
    keyword = "software engineer Web development"
    # keyword = "data analyst"
    # keyword = "cyber"
    # keyword = 'QA'
    num_jobs = 900
    max_sleep_time = 1
    list_keywords = [
        'Cloud computing', 'Artificial Intelligence', 'Machine Learning engineer',
        'Data engineering'
        'DevOps', 'Cybersecurity', 'Data science and analytics', 'Augmented Reality', 'Robotics', 'Web development',
        'Internet of Things', 'Financial technology', 'HealthTech', 'E-commerce',
        'Enterprise software', 'Education technology', 'Social media and networking engineer',
        'Mobile app development', 'Desktop software development', 'Game development']
    for i, keyword in enumerate(list_keywords):
        df = Sahar.get_jobs(keyword, num_jobs, path, max_sleep_time, 0)  # call to scraper
        df_clean = dc.data_cleaning(df)
        df_clean.to_csv(f"{i}_{keyword}.csv")


def unique_values():
    df1 = pandas.read_csv('data files/raw data/QA raw data 500.csv')
    df2 = pandas.read_csv('data files/raw data/')
    df3 = pandas.read_csv('data files/raw data/QA raw data 500.csv')
    df4 = pandas.read_csv('data files/raw data/web developer raw data 3000.csv')
    df5 = pandas.read_csv('data files/raw data/@0_software engineer raw data 10000.csv')

    dc.column_unique_values(df1, df2, df3, df4, df5, 'Sector', 'QA')


def scale_check():
    df = pandas.read_csv('data files/clean data/3_software engineer scaling data 20.csv')
    column_names = ['Sector', 'Industry', 'Job Title', 'Revenue']
    df_one_hot_encoding = dc.one_hot_encoding(df, column_names)
    df_one_hot_encoding.to_csv(f"one_hot_encoding.csv")


def main_check_extract_from_text():
    with open('data files/raw text from job descriptions/row_text_data analyst20.txt', 'r') as f:
        text = f.read()
        result = et.nlp_for_years_of_experience(text)
        print(result)


# unique_values()
main_scraper()
# scale_check()
# main_check_extract_from_text()
