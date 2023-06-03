import pandas
import pandas as pd

import Data_Cleaning as dc
import Extract_from_text as et
import Glass_Door_Scraper_var0 as Sahar

# GLOBAL
NUM_JOBS = 100
PATH_DRIVER = "C:/Users/avich/chromedriver"
MAX_SLEEP_TIME = .7



def main_scraper():


    columns = ['Job Title', 'Type of Ownership', 'Time Unit', 'Revenue', 'Company Size',
               'Location']  # for one-hot encoding

    # Software Engineer
    list_keywords_SE = [
        'Artificial Intelligence', 'Machine Learning engineer',
        'Data engineering'
        'DevOps', 'Cybersecurity', 'Data science and analytics', 'Augmented Reality', 'Robotics', 'Web development',
        'Internet of Things', 'Financial technology', 'HealthTech', 'E-commerce',
        'Enterprise software', 'Education technology', 'Social media and networking engineer']

    # Data Science
    list_keywords_DS = [
        'Data Scientist', 'Data Analyst', 'Machine Learning Engineer',
        'Data Engineer', 'Business Intelligence Analyst', 'Data Architect',
        'Statistician', 'Quantitative Analyst', 'Data Product Manager',
        'Research Scientist'
    ]

    # QA
    list_keywords_QA = [
        'Quality Assurance Analyst', 'Software Tester', 'QA Engineer', 'Automation Tester',
        'Test Lead', 'Test Manager', 'Performance Tester', 'Security Tester', 'User Acceptance Tester',
        'Test Automation Engineer', 'Mobile Tester', 'Game Tester', 'Test Architect',
        'Regression Tester', 'Load Tester', 'Accessibility Tester', 'Functional Tester',
        'Usability Tester', 'Localization Tester', 'Database Tester', 'API Tester',
        'Penetration Tester', 'Compliance Tester', 'Test Coordinator', 'Test Consultant',
        'Test Strategist', 'Test Trainer', 'Test Process Engineer', 'Test Data Analyst', 'Test Environment Manager']

    # Machin learning
    list_keywords_ML = ['Machine Learning Engineer', 'AI Researcher', 'Computer Vision Engineer',
                        'Natural Language Processing (NLP) Engineer',
                        'Deep Learning Engineer', 'Robotics Engineer', 'Recommender Systems Engineer',
                        'Data Analyst', 'Business Intelligence Analyst', 'Fraud Detection Analyst',
                        'Image Recognition Engineer', 'Speech Recognition Engineer', 'Predictive Analytics Specialist',
                        'Autonomous Vehicle Engineer', 'Healthcare Data Scientist', 'Financial Analyst (ML)',
                        'Social Media Analyst', 'Sentiment Analysis Specialist', 'Text Mining Expert',
                        'Data Mining Engineer', 'Pattern Recognition Engineer', 'Anomaly Detection Specialist',
                        'Virtual Assistant Developer', 'Chatbot Developer', 'AI Consultant',
                        'Predictive Maintenance Engineer', 'Energy Analyst (ML)',
                        'Manufacturing Optimization Specialist', 'Agriculture Analytics Specialist']

    # Game Development
    list_keywords_GD = ['Game Designer', 'Game Programmer', 'Game Artist', 'Game Animator', 'Game Sound Designer',
                        'Game Tester', 'Game Producer', 'Game Writer', 'Game Level Designer', 'Game UI/UX Designer',
                        'Game Monetization Specialist', 'Game Quality Assurance Tester', 'Game Engine Developer',
                        'Game Localization Specialist', 'Gameplay Programmer', 'Gameplay Designer',
                        # VR & AR
                        'VR Developer', 'AR Developer', 'VR/AR Designer', 'VR/AR Artist', 'VR/AR Engineer',
                        'VR/AR Content Creator', 'VR/AR UX Designer', 'VR/AR Software Engineer'


                        # Computer Graphics
                                                                      'Graphics Programmer',
                        'Graphics Software Engineer', 'Shader Developer', 'Rendering Engineer',
                        'Computer Vision Engineer', '3D Modeler', 'Texture Artist', 'Lighting Artist',
                        'Character Artist',
                        'Environment Artist', 'Rigging Artist'

                        # Simulation and Training
                                              'Simulation Developer', 'Training Developer', 'Simulation Engineer',
                        'Training Specialist',
                        'Simulation Programmer', 'Training Coordinator', 'Simulation Designer', 'Training Instructor'


                        # Serious Games
                                                                                                'Serious Games Developer',
                        'Educational Game Developer', 'Healthcare Game Developer',
                        'Military Training Game Developer', 'Corporate Training Game Developer',
                        'Government Simulation Developer'

                        # Interactive Media
                        'Interactive Media Developer', 'Interactive Media Designer', 'Interactive Media Artist',
                        'Interactive Media Programmer', 'Interactive Storyteller', 'Interactive Experience Designer'

                        # Game Analytics
                                                                                   'Game Data Analyst',
                        'Game Data Scientist', 'Game Analytics Specialist', 'Game User Researcher',
                        'Game Market Research Analyst', 'Game Business Intelligence Analyst']

    # calling the scraper with different category
    scrape_jobs_and_save(list_keywords_GD, "game development", "GD")
    scrape_jobs_and_save(list_keywords_SE, "software engineer", "SE")
    scrape_jobs_and_save(list_keywords_QA, "QA", "QA")
    scrape_jobs_and_save(list_keywords_DS, "data scientist", "DS")
    scrape_jobs_and_save(list_keywords_ML, "machine learning", "ML")


    # for i, keyword in enumerate(list_keywords_DS):
    #     try:
    #         df = Sahar.get_jobs(keyword, num_jobs, path, max_sleep_time, 0)  # call to scraper
    #         df_clean = dc.data_cleaning(df)  # first clean: calculate the salary, fixing the location and more
    #         df_clean.to_csv(f"data files/data scientist/{i}_DS_{keyword}.csv")
    #     except Exception as e:
    #         print("!!!!!!!!!!!!main exception!!!!!!!!!", e)
    #
    # for i, keyword in enumerate(list_keywords_QA):
    #     try:
    #         df = Sahar.get_jobs(keyword, num_jobs, path, max_sleep_time, 0)  # call to scraper
    #         df_clean = dc.data_cleaning(df)  # first clean: calculate the salary, fixing the location and more
    #         df_clean.to_csv(f"data files/QA/{i}_QA_{keyword}.csv")
    #     except Exception as e:
    #         print("!!!!!!!!!!!!main exception!!!!!!!!!", e)
    #
    #
    # for i, keyword in enumerate(list_keywords_GD):
    #     try:
    #         df = Sahar.get_jobs(keyword, num_jobs, path, max_sleep_time, 0)  # call to scraper
    #         df_clean = dc.data_cleaning(df)  # first clean: calculate the salary, fixing the location and more
    #         df_clean.to_csv(f"data files/game development/{i}_GD_{keyword}.csv")
    #     except Exception as e:
    #         print("!!!!!!!!!!!!main exception!!!!!!!!!", e)
    #
    # for i, keyword in enumerate(list_keywords_SE):
    #     try:
    #         df = Sahar.get_jobs(keyword, num_jobs, path, max_sleep_time, 0)  # call to scraper
    #         df_clean = dc.data_cleaning(df)  # first clean: calculate the salary, fixing the location and more
    #         df_clean.to_csv(f"data files/software engineer/{i}_SE_{keyword}.csv")
    #     except Exception as e:
    #         print("!!!!!!!!!!!!main exception!!!!!!!!!", e)
    #
    # for i, keyword in enumerate(list_keywords_ML):
    #     try:
    #         df = Sahar.get_jobs(keyword, num_jobs, path, max_sleep_time, 0)  # call to scraper
    #         df_clean = dc.data_cleaning(df)  # first clean: calculate the salary, fixing the location and more
    #         df_clean.to_csv(f"data files/machine learning/{i}_ML_{keyword}.csv", index=False)
    #     except Exception as e:
    #         print("!!!!!!!!!!!!main exception!!!!!!!!!", e)



def unique_values():
    df1 = pandas.read_csv('data files/software engineer/0_Cloud computing.csv')
    df2 = pandas.read_csv('data files/software engineer/1_Mobile app development.csv')
    df3 = pandas.read_csv('data files/software engineer/0_Web development.csv')
    df4 = pandas.read_csv('data files/software engineer/2_Desktop software development.csv')
    df5 = pandas.read_csv('data files/software engineer/3_Game development.csv')

    dc.column_unique_values(df1, df2, df3, df4, df5, 'Sector', 'software engineer')


def main_one_hot_encoding():
    df = pandas.read_csv('data files/software engineer/software engineer.csv')
    column_names = ['Job Title', 'Type of Ownership', 'Time Unit', 'Revenue', 'Company Size',
                    'Location']  # for one_hot encodings
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


def main_single_keyword():
    keyword = 'Game Tester'
    num_jobs = 900
    path = "C:/Users/avich/chromedriver"
    max_sleep_time = 1
    i = 10
    columns = ['Job Title', 'Type of Ownership', 'Time Unit', 'Revenue', 'Company Size',
               'Location']  # for one-hot encoding

    df = Sahar.get_jobs(keyword, num_jobs, path, max_sleep_time, 0)  # call to scraper

    df_clean = dc.data_cleaning(df)  # first clean: calculate the salary, fixing the location and more
    df_clean.to_csv(f"{i} {keyword} raw data.csv")

    df_clean = dc.one_hot_encoding(df_clean, columns)  # one-hot encoding process

    df_clean = dc.final_clean(df_clean)  # Removing all unnecessary columns and staying only with numeric values!
    df_clean.to_csv(f"{i} {keyword} final data.csv")


def main_clean_and_marge_files_from_directory():
    merged_df = dc.merge_csv_files_in_folder("data files/game development/raw data")
    merged_df.to_csv('dataBase game development.csv')


def scrape_jobs_and_save(list_keywords, category, file_prefix):
    for i, keyword in enumerate(list_keywords):
        try:
            df = Sahar.get_jobs(keyword, NUM_JOBS, PATH_DRIVER, MAX_SLEEP_TIME)  # call to scraper
            df_clean = dc.data_cleaning(df)  # first clean: calculate the salary, fixing the location and more
            df_clean.to_csv(f"data files/{category}/{file_prefix}_{i}_{keyword}.csv", index=False)
        except Exception as e:
            print("!!!!!!!!!!!!main exception!!!!!!!!!", e)



main_scraper()
# main_final_data()
# unique_values()
# main_one_hot_encoding()
# main_check_extract_from_text()
# main_single_keyword()
# main_clean_and_marge_files_from_directory()


