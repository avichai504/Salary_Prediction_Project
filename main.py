import Glass_Door_Scarper as gs
import Data_Cleaning as dc



def main_scraper():
    path = "C:/Users/avich/chromedriver"
    keyword = "software developer"
    num_jobs = 1000
    sleep_time = 0.9
    df = gs.get_jobs(keyword, num_jobs, path, sleep_time)  # call to scraper
    df.to_csv(f"{keyword} raw data {num_jobs}.csv")
    df_clean = dc.data_cleaning(df)
    df_clean.to_csv(f"{keyword} clean data {num_jobs}.csv")
    df_final_clean = dc.final_clean(df_clean)
    df_final_clean.to_csv(f"{keyword} final data {num_jobs}.csv")  # DataBase!!!!!




main_scraper()




