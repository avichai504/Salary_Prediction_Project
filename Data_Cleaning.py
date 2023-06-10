import numpy as np
import pandas as pd
import os

from sklearn.preprocessing import StandardScaler


def hourly_to_annual(salary):
    return round(float(salary * 2080), 2)  # assuming 40 hours/week and 52 weeks/year


def monthly_to_annual(salary):
    return round(float(salary * 12), 2)


def data_cleaning(df1):
    df = df1.copy()
    df = df[df['Salary Estimate'] != -1].copy()

    # Remove (est.)
    try:
        df["Time Unit"] = df["Salary Estimate"].apply(lambda x: x.split(' ')[1])
    except Exception as e:
        pass
        # print(e, "e1")

    # Add more columns to calculate the salary
    try:
        df["Time Unit"] = df["Time Unit"].apply(lambda x: x.split('/')[1])
    except Exception as e:
        pass
        # print(e, "e2")

    # Split the "Salary Estimate" column by the '/' separator and extract the first element
    try:
        df["Annual Salary"] = df["Salary Estimate"].apply(lambda x: (x.split('/')[0]))
    except Exception as e:
        pass
        # print(e, "e3")

    # Remove the dollar sign ($) from the "Salary Estimate" column
    try:
        df["Annual Salary"] = df["Annual Salary"].apply(lambda x: x.split('$')[1])
    except Exception as e:
        pass
        # print(e, "e4")

    # Remove any commas from the "Salary Estimate" column
    try:
        df["Annual Salary"] = df["Annual Salary"].apply(lambda x: x.replace(',', ''))
    except Exception as e:
        pass
        # print(e, "e5")

    # Convert the "Salary Estimate" column to a float data type
    try:
        df["Annual Salary"] = df["Annual Salary"].apply(lambda x: float(x))
    except Exception as e:
        pass
        # print(e, "e6")

    # Convert hourly salaries to annual salaries
    try:
        df.loc[df['Time Unit'] == 'hr', 'Annual Salary'] = df.loc[df['Time Unit'] == 'hr', 'Annual Salary'].apply(
            hourly_to_annual)
    except Exception as e:
        pass
        # print(e, "e7")

    # Convert monthly salaries to annual salaries
    try:
        df.loc[df['Time Unit'] == 'mo', 'Annual Salary'] = df.loc[df['Time Unit'] == 'mo', 'Annual Salary'].apply(
            monthly_to_annual)
    except Exception as e:
        pass
        # print(e, "e8")

    try:
        df['Company Name'] = df['Company Name'].apply(lambda x: x.split('\n')[0])
    except Exception as e:
        pass
        # print(e, "e9")

    # Convert the 'Founded' to 'Company Old'
    try:
        df['Founded'] = df['Founded'].apply(lambda x: -1 if x == -1 else int(x))
        df['Company Old'] = df['Founded'].apply(lambda x: x if x == -1 else 2023 - x)
        df.insert(9, 'Company Old', df.pop('Company Old'))  # insert it into a specific index
    except Exception as e:
        pass
        # print(e, "e10")

    # Convert 'Is Remote' to 0/1
    try:
        df['Is Remote'] = df['Is Remote'].astype(int)
    except Exception as e:
        pass
        # print(e, "e11")

    desired_columns = ['Salary Estimate', 'Annual Salary']
    df = df.reindex(columns=desired_columns + [col for col in df.columns if col not in desired_columns])

    # make location only two characters or Remote
    try:
        # print(df.dtypes)
        df['Location'] = df['Location'].fillna('')
        df['Location'] = df['Location'].apply(lambda x: x.split(',')[-1])
    except Exception as e:
        print(e, 'e location')

    df = pd.DataFrame(df)
    return df


def preprocess_scaling(df):

    # Convert the values in Location to a string
    df["Location"] = df["Location"].astype(str)
    # Deleting the space in the values on Location if exist
    df["Location"] = df["Location"].apply(lambda x: x if ' ' not in x else x.replace(' ', ''))

    # Preprocess the 'Location' column
    location_mapping = {
        "Remote": 1,
        "NJ": 2,
        "LA": 3,
        "CA": 4,
        "AZ": 5,
        "MD": 6,
        "FL": 7,
        "WA": 8,
        "MI": 9,
        "NY": 10,
        "CT": 11,
        "TX": 12,
        "MN": 13,
        "MA": 14,
        "MS": 15,
        "CO": 16,
        "VA": 17,
        "GA": 18,
        "NC": 19,
        "KY": 20,
        "WI": 21,
        "IN": 22,
        "AL": 23,
        "ID": 24,
        "TN": 25,
        "OH": 26,
        "IL": 27,
        "ME": 28,
        "Michigan": 29,
        "Pennsylvania": 30,
        "PA": 31,
        "Colorado": 32,
        "DC": 33,
        "MO": 34,
        "RI": 35,
        "UT": 36,
        "NV": 37,
        "OR": 38,
        pd.NA: 3,
        "KS": 39,
        "SC": 40,
        "NM": 41,
        "AK": 42,
        "PR": 43,
        "IA": 44,
        "WY": 45,
        "OK": 46,
        "MT": 47,
        "AR": 48,
        "NE": 49,
        "DE": 50,
        "HI": 51,
        "ND": 52,
        "NH": 53,
        "SD": 54,
        "VT": 55,
        "WV": 56
    }
    df["Scale_Location"] = df["Location"].map(location_mapping)

    # Preprocess the 'Company Size' column
    company_size_mapping = {
        "Unknown / Non-Applicable": None,
        "-1": None,
        "1 to 50 Employees": int(1),
        "51 to 200 Employees": int(2),
        "201 to 500 Employees": int(3),
        "501 to 1000 Employees": int(4),
        "1001 to 5000 Employees": int(5),
        "5001 to 10000 Employees": int(6),
        "10000+ Employees": int(7)
    }
    df["Scale_Company_Size"] = df["Company Size"].map(company_size_mapping)

    # Preprocess the 'Revenue' column
    revenue_mapping = {
        "Unknown / Non-Applicable / -1": None,
        "Less than $1 million (USD)": 1,
        "$1 to $5 million (USD)": 2,
        "$5 to $25 million (USD)": 3,
        "$25 to $50 million (USD)": 4,
        "$50 to $100 million (USD)": 5,
        "$100 to $500 million (USD)": 6,
        "$500 million to $1 billion (USD)": 7,
        "$1 to $2 billion (USD)": 7,
        "$1 to $5 billion (USD)": 7,
        "$2 to $5 billion (USD)": 8,
        "$5 to $10 billion (USD)": 8,
        "$10+ billion (USD)": 9
    }
    df["Scale_Revenue"] = df["Revenue"].map(revenue_mapping)


        # Define the frequency mapping for scaling
    industry_mapping = {
        'Unknown': 0,
        'Information Technology Support Services': 1,
        'Other': 2,
        'Video Game Publishing': 3,
        'Computer Hardware Development': 4,
        'Internet & Web Services': 5,
        'Enterprise Software & Network Solutions': 6,
        'Aerospace & Defense': 7,
        'Health Care Services & Hospitals': 8,
        'Colleges & Universities': 9,
        'Business Consulting': 10,
        'Banking & Lending': 11,
        'Biotech & Pharmaceuticals': 12,
        'Software Development': 13,
        'Transportation Equipment Manufacturing': 14,
        'Advertising & Public Relations': 15,
        'Film Production': 16,
        'Insurance Carriers': 17,
        'Consumer Product Manufacturing': 18,
        'Electronics Manufacturing': 19,
        'Investment & Asset Management': 20,
        'HR Consulting': 21,
        'Machinery Manufacturing': 22,
        'Energy & Utilities': 23,
        'National Agencies': 24,
        'Research & Development': 25,
        'Sports & Recreation': 26,
        'Real Estate': 27,
        'Culture & Entertainment': 28,
        'Financial Transaction Processing': 29,
        'Telecommunications Services': 30,
        'Food & Beverage Manufacturing': 31,
        'Health Care Products Manufacturing': 32,
        'State & Regional Agencies': 33,
        'Broadcast Media': 34,
        'Architectural & Engineering Services': 35,
        'Construction': 36
        # Add remaining values as per your requirement
    }

    # Map the industry frequencies to scale the 'Industry' column
    df['Scale_Industry'] = df['Industry'].map(industry_mapping)

    return df


def column_unique_values(df, column_name):
    concatenated_column = pd.concat(df[column_name])

    unique_values = concatenated_column.unique()
    str_unique = ''
    for i, unique in enumerate(unique_values):
        str_unique += unique
        if i % 5 == 0:
            str_unique += '\n'
        else:
            str_unique += ','

    with open(f"unique_values_'{column_name}'.txt", 'w') as f:
        f.write(str_unique)
        f.write(f"\n\nThe number of unique values is {len(unique_values)}")


def one_hot_encoding(df, column_names):
    df = pd.get_dummies(df, columns=column_names)
    return df


def final_clean(df):  # call this function after one-hot encoding!
    columns = list(df)

    if 'Salary Estimate' in columns:
        df.drop('Salary Estimate', axis=1, inplace=True)
    if 'Company Name' in columns:
        df.drop('Company Name', axis=1, inplace=True)
    if '<null>' in columns:
        df.drop('<null>', axis=1, inplace=True)
    if 'null' in columns:
        df.drop('null', axis=1, inplace=True)
    if 'Company Size' in columns:
        df.drop('Company Size', axis=1, inplace=True)
    if 'Revenue' in columns:
        df.drop('Revenue', axis=1, inplace=True)
    if 'Time Unit' in columns:
        df.drop('Time Unit', axis=1, inplace=True)
    if 'Industry' in columns:
        df.drop('Industry', axis=1, inplace=True)
    if 'Sector' in columns:
        df.drop('Sector', axis=1, inplace=True)
    if 'Type of Ownership' in columns:
        df.drop('Type of Ownership', axis=1, inplace=True)
    if 'Time of Scrape' in columns:
        df.drop('Time of Scrape', axis=1, inplace=True)
    if 'Location' in columns:
        df.drop('Location', axis=1, inplace=True)
    if 'Unnamed: 0' in columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)
    if 'Unnamed: 0.1' in columns:
        df.drop('Unnamed: 0.1', axis=1, inplace=True)
    if 'Founded' in columns:
        df.drop('Founded', axis=1, inplace=True)
    if 'Job Title' in columns:
        df.drop('Job Title', axis=1, inplace=True)
    if 'anonymous' in columns:
        df.drop('anonymous', axis=1, inplace=True)
    # df = df.loc[:, ~df.columns.str.contains('^anonymous')]

    print(f"The number of Duplicated = {df.duplicated().sum()}")
    df.drop_duplicates(keep='first', inplace=True)
    print(f"The final files = {df.shape} ")

    df = pd.DataFrame(df)
    return df


def merge_csv_files_in_folder(folder_path):
    df_list = []  # List to hold DataFrames

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):  # Check a file extension
            df = pd.read_csv(os.path.join(folder_path, filename))
            df_list.append(df)

    # Concatenate all dataframes in the list
    merged_df = pd.concat(df_list, ignore_index=True)
    if 'Unnamed: 0' in list(merged_df):
        merged_df.drop('Unnamed: 0', axis=1, inplace=True)
    if 'Time of Scrape' in list(merged_df):
        merged_df.drop('Time of Scrape', axis=1, inplace=True)
    if 'Origin' in list(merged_df):
        merged_df.drop('Origin', axis=1, inplace=True)


    print(f"Before dropping duplicates: {merged_df.shape}")
    merged_df.drop_duplicates(keep='first', inplace=True)
    print(f"After dropping all duplicates: {merged_df.shape}")

    return merged_df


"""
New way of dilling with data cleaning and preparation - OOP !
"""


class DataInfo:
    def __init__(self, data):
        if type(data) == str:
            self.df = pd.read_csv(data, index_col=0)
        else:
            self.df = pd.DataFrame(data)

        if 'Time of Scrape' in list(self.df):
            self.df.drop('Time of Scrape', axis=1, inplace=True)
        if 'Origin' in list(self.df):
            self.df.drop('Origin', axis=1, inplace=True)
        if 'Unnamed: 0' in list(self.df):
            self.df.drop('Unnamed: 0', axis=1, inplace=True)

        print(f"Sum of duplicated: {self.df.duplicated().sum()}")
        self.df.drop_duplicates(keep='first', inplace=True)
        print(f"Shape after remove duplication: {self.df.shape}")

    def scaling(self):
        # Preprocess the 'Revenue' column
        revenue_mapping = {
            "Unknown / Non-Applicable / -1": None,
            "Less than $1 million (USD)": 1,
            "$1 to $5 million (USD)": 2,
            "$5 to $25 million (USD)": 3,
            "$25 to $50 million (USD)": 4,
            "$50 to $100 million (USD)": 5,
            "$100 to $500 million (USD)": 6,
            "$500 million to $1 billion (USD)": 7,
            "$1 to $2 billion (USD)": 7,
            "$1 to $5 billion (USD)": 7,
            "$2 to $5 billion (USD)": 8,
            "$5 to $10 billion (USD)": 8,
            "$10+ billion (USD)": 9
        }
        # Preprocess the 'Company Size' column
        company_size_mapping = {
            "Unknown / Non-Applicable": None,
            "-1": None,
            "1 to 50 Employees": int(1),
            "51 to 200 Employees": int(2),
            "201 to 500 Employees": int(3),
            "501 to 1000 Employees": int(4),
            "1001 to 5000 Employees": int(5),
            "5001 to 10000 Employees": int(6),
            "10000+ Employees": int(7)
        }

        self.df["Scale_Company_Size"] = self.df["Company Size"].map(company_size_mapping)
        self.df["Scale_Revenue"] = self.df["Revenue"].map(revenue_mapping)

    def to_csv(self, path):
        self.df.to_csv(path, index=False)


    def fill_all_missing_values_with_mean(self):
        # List of columns with missing values
        columns_with_missing = ['Experience', 'Education', 'Rating',
                                'Career Opportunities', 'Comp & Benefits', 'Culture & Values',
                                'Senior Management', 'Work Life Balance', 'Scale_Revenue', 'Scale_Company_Size', 'Location']
        # Iterate through each column
        for column_with_missing in columns_with_missing:
            if column_with_missing in list(self.df):

                # Replace -1 with NaN
                self.df[column_with_missing] = self.df[column_with_missing].replace(-1, np.nan)

                # Handle Education column separately
                if column_with_missing == 'Education':
                    self.df[column_with_missing].fillna(0, inplace=True)
                elif column_with_missing == 'Education':
                    self.df[column_with_missing].fillna('LA', inplace=True)

                else:
                    # Create a reference column without missing values
                    self.df['Reference'] = self.df[column_with_missing].copy()

                    # Calculate the mean value of the reference column
                    mean_value = self.df['Reference'].mean()

                    # Fill missing values with the mean value
                    self.df[column_with_missing].fillna(mean_value, inplace=True)

                    # Remove the reference column
                    self.df.drop('Reference', axis=1, inplace=True)


    def final(self):
        columns = list(self.df)
        df = self.df
        if 'Salary Estimate' in columns:
            df.drop('Salary Estimate', axis=1, inplace=True)
        if 'Company Name' in columns:
            df.drop('Company Name', axis=1, inplace=True)
        if '<null>' in columns:
            df.drop('<null>', axis=1, inplace=True)
        if 'null' in columns:
            df.drop('null', axis=1, inplace=True)
        if 'Company Size' in columns:
            df.drop('Company Size', axis=1, inplace=True)
        if 'Revenue' in columns:
            df.drop('Revenue', axis=1, inplace=True)
        if 'Time Unit' in columns:
            df.drop('Time Unit', axis=1, inplace=True)
        if 'Industry' in columns:
            df.drop('Industry', axis=1, inplace=True)
        if 'Sector' in columns:
            df.drop('Sector', axis=1, inplace=True)
        if 'Type of Ownership' in columns:
            df.drop('Type of Ownership', axis=1, inplace=True)
        if 'Time of Scrape' in columns:
            df.drop('Time of Scrape', axis=1, inplace=True)
        if 'Location' in columns:
            df.drop('Location', axis=1, inplace=True)
        if 'Unnamed: 0' in columns:
            df.drop('Unnamed: 0', axis=1, inplace=True)
        if 'Unnamed: 0.1' in columns:
            df.drop('Unnamed: 0.1', axis=1, inplace=True)
        if 'Founded' in columns:
            df.drop('Founded', axis=1, inplace=True)
        if 'Job Title' in columns:
            df.drop('Job Title', axis=1, inplace=True)
        if 'anonymous' in columns:
            df.drop('anonymous', axis=1, inplace=True)
        self.df = df.copy()



def filling_missing_values(job):
    columns_with_missing = ['Experience', 'Rating', 'Company Old',
                            'Career Opportunities', 'Comp & Benefits', 'Culture & Values',
                            'Senior Management', 'Work Life Balance', 'Scale_Revenue', "Scale_Company_Size", 'Type of Ownership']

    list_types_of_ownership = ['Private', 'Public', 'Government', 'College / University', 'Hospital', 'Nonprofit Organization',
                               'Subsidiary or Business Segment', 'Unknown'
                               'School', 'Self-employed', 'Contract']


    # Iterate through each column
    for column_with_missing in columns_with_missing:
        # Replace -1 with NaN
        job[column_with_missing] = job[column_with_missing].replace(-1, np.nan)
        job[column_with_missing] = job[column_with_missing].replace('-1', np.nan)


        # Margin all options of 'Type of ownership'
        if 'Type of Ownership' in list(job):
            if column_with_missing == 'Type of Ownership':
                job[column_with_missing] = job[column_with_missing].apply(lambda x: 'Private' if x == 'Company - Private' or x == 'Unknown' or x == 'Private Practice / Firm' else x)
                job[column_with_missing] = job[column_with_missing].apply(lambda x: 'Public' if x == 'Company - Public' else x)


        elif column_with_missing == 'Type of Ownership':
            job[column_with_missing].fillna('Private', inplace=True)

        else:
            # Create a reference column without missing values
            job['Reference'] = job[column_with_missing].copy()

            # Calculate the mean value of the reference column
            mean_value = job['Reference'].mean()

            # Fill missing values with the mean value
            job[column_with_missing].fillna(mean_value, inplace=True)

            # Remove the reference column
            job.drop('Reference', axis=1, inplace=True)



