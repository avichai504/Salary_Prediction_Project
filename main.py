import Glass_Door_Scarper as gs
import Data_Cleaning as dc


def main_scraper():
    path = "C:/Users/avich/chromedriver"
    # keyword = "software engineer"
    # keyword = "QA"
    keyword = "cyber"
    num_jobs = 15
    max_sleep_time = 2
    i = '1'
    df = gs.get_jobs(keyword, num_jobs, path, max_sleep_time)  # call to scraper
    df.to_csv(f"{i}_{keyword} raw data {num_jobs}.csv")
    df_clean = dc.data_cleaning(df)
    df_clean.to_csv(f"{i}_{keyword} clean data {num_jobs}.csv")
    df_final_clean = dc.final_clean(df_clean)
    df_final_clean.to_csv(f"{i}_{keyword} final data {num_jobs}.csv")  # DataBase!!!!!


main_scraper()
