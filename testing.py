import pandas as pd
from sklearn.feature_extraction import FeatureHasher
import Data_Cleaning as dc

df = pd.read_csv('DataBaseVar\DataBase_var2.csv')

# df['Scale Job Title'] = pd.factorize(df['Job Title'])[0]
# df.to_csv('DataBaseVar\DataBase_var1.3.csv', index=False)

unique = df['Industry'].unique()

# unique_values_string = ', '.join(str(value) for value in unique)

value_counts = df['Industry'].value_counts()

# sorted_values = value_counts.sort_values(ascending=False)

top_1000_values = value_counts.index[:1000].tolist()

# top_50_values_for_matrix = value_counts.head(50)

# matrix = pd.DataFrame({'Name': top_50_values_for_matrix.index, 'Frequency': top_50_values_for_matrix.values})

unique_counter = 0
str_unique = ''

for i, unique in enumerate(top_1000_values):
    str_unique += f"{unique}    {value_counts[i]} \n"
    unique_counter = i
print(str_unique)
print()

with open("unique_Industry_by_freq.txt", 'w') as f:
    f.write(str_unique)
    f.write(f"\n\nThe number of unique values is {unique_counter} ")

print("HELLO")

#
# from fuzzywuzzy import fuzz
#
# # Step 1: Load the list of job titles
# job_titles = [
#     "AI Researcher",
#     "Artificial Intelligence Specialist",
#     "Back-end Developer",
#     "Business Analyst",
#     "Business Intelligence Analyst",
#     "Cloud Architect",
#     "Cloud Engineer",
#     "Cloud Solutions Architect",
#     "Content Writer",
#     "Customer Support Specialist",
#     "Cyber Security and Cloud Computing Tutor",
#     "Data Analyst",
#     "Data Architect",
#     "Data Engineer",
#     "Data Entry Operator",
#     "Data Scientist",
#     "Data Visualization Specialist",
#     "Database Administrator",
#     "Database Developer",
#     "DevOps Engineer",
#     "Digital Marketing Specialist",
#     "E-commerce Manager",
#     "Financial Analyst",
#     "Front-end Developer",
#     "Frontend Architect",
#     "Full Stack Developer",
#     "Game Developer",
#     "Graphic Designer",
#     "HR Manager",
#     "Information Security Analyst",
#     "IT Auditor",
#     "IT Business Analyst",
#     "IT Consultant",
#     "IT Operations Manager",
#     "IT Project Manager",
#     "IT Security Specialist",
#     "IT Support Technician",
#     "IT Systems Analyst",
#     "IT Trainer",
#     "Machine Learning Engineer",
#     "Machine Learning Specialist",
#     "Marketing Coordinator",
#     "Mobile App Developer",
#     "Network Administrator",
#     "Network Engineer",
#     "Network Security Engineer",
#     "Operations Manager",
#     "Product Manager",
#     "Product Owner",
#     "Project Manager",
#     "Quality Assurance Engineer",
#     "Sales Executive",
#     "Social Media Manager",
#     "Software Developer",
#     "Software Tester",
#     "Systems Administrator",
#     "Systems Analyst",
#     "Systems Engineer",
#     "Technical Writer",
#     "UI/UX Designer",
#     "UI/UX Developer",
#     "UX Researcher",
#     "UX/UI Designer",
#     "Web Designer",
#     "Web Development Foundations (Complex) || Fresher",
# ]
#
#
# # Step 2: Identify similar job titles
# def find_similar_titles(job_titles, threshold=80):
#     similar_titles = {}
#     for i in range(len(job_titles)):
#         for j in range(i + 1, len(job_titles)):
#             title1 = job_titles[i]
#             title2 = job_titles[j]
#             similarity_score = fuzz.token_sort_ratio(title1, title2)
#             if similarity_score >= threshold:
#                 similar_titles.setdefault(title1, set()).add(title2)
#                 similar_titles.setdefault(title2, set()).add(title1)
#     return similar_titles
#
#
# unique_job_titles = df['Job Title'].unique()
# similar_job_titles = find_similar_titles(unique_job_titles)
#
#
# # Step 3: Apply string similarity measures
#
# # Function to get the most frequent job title in a cluster
# def get_normalized_category(cluster):
#     title_counts = df[df['Job Title'].isin(cluster)]['Job Title'].value_counts()
#     return title_counts.idxmax()
#
#
# normalized_categories = {}
# for title, similar_titles in similar_job_titles.items():
#     normalized_category = get_normalized_category(similar_titles.union({title}))
#     normalized_categories[title] = normalized_category
#
# # Step 4: Assign normalized categories
# df['Normalized Job Title'] = df['Job Title'].map(normalized_categories)
#
# # Step 5: Update your dataset
# df['Normalized Job Title'] = df['Normalized Job Title'].fillna(df['Job Title'])
#
# # Print the updated DataFrame
# df.to_csv('DataBaseVar\DataBase_var1.2.csv', index=False)

"""
My model of machine learning is not preforming well, with just 0.33405 score of accurasy.
Im using Linear Regression to predict the Annual Salary of an employ in the Tech industry, by using the following features, with the number of its correlation with 'Annual Salary':


The correlation of the features with 'Annual Salary': 

Experience              0.436344
Scale_Location          0.243389
Comp & Benefits         0.204343
Career Opportunities    0.133141
Company Old             0.114363
Founded                 0.109870
Culture & Values        0.106292
Rating                  0.103219
Scale_Revenue           0.089053
Position                0.088656
Is Remote               0.088026
Senior Management       0.080886
Work Life Balance       0.073341
Scale_Company_Size      0.050103
Education               0.005286

Now, in order to make my model more accurate I need to find a why to use column named: 'Industry' with some-kind of feature engineering because right now they are represented as stings with NO any tipe of order. I need to find a why to classify them and to make them usable for my model.

"""

"""
Yes, I do have very large number of unique values in the 'Industry' column. 
I am thinking how can I reduce the number of unique values by applying some methods based on AI approach.
I know that significant number of unique values can be united in to each oder.
Here is the current list of values, with the number of its frequency of each one:

Unknown    4289 
Information Technology Support Services    1064 
Video Game Publishing    919 
Computer Hardware Development    615 
Internet & Web Services    586 
Enterprise Software & Network Solutions    514 
Aerospace & Defense    480 
Health Care Services & Hospitals    399 
Colleges & Universities    344 
Business Consulting    292 
Banking & Lending    287 
Biotech & Pharmaceuticals    247 
Software Development    203 
Transportation Equipment Manufacturing    201 
Advertising & Public Relations    192 
Film Production    183 
Insurance Carriers    157 
Consumer Product Manufacturing    148 
Electronics Manufacturing    145 
Investment & Asset Management    142 
HR Consulting    130 
Machinery Manufacturing    126 
Energy & Utilities    121 
National Agencies    107 
Research & Development    87 
Sports & Recreation    81 
Real Estate    80 
Culture & Entertainment    78 
Financial Transaction Processing    77 
Telecommunications Services    76 
Food & Beverage Manufacturing    75 
Health Care Products Manufacturing    74 
State & Regional Agencies    71 
Broadcast Media    64 
Architectural & Engineering Services    57 
Construction    55 
Wholesale    48 
Gambling    47 
Shipping & Trucking    45 
Primary & Secondary Schools    44 
Grantmaking & Charitable Foundations    43 
Civic & Social Services    43 
Accounting & Tax    41 
Publishing    40 
Cable, Internet & Telephone Providers    36 
Chemical Manufacturing    36 
Department, Clothing & Shoe Stores    33 
Insurance Agencies & Brokerages    32 
Education & Training Services    32 
Municipal Agencies    31 
Staffing & Subcontracting    29 
Hotels & Resorts    28 
Taxi & Car Services    26 
Other Retail Stores    23 
Sporting Goods Stores    21 
General Merchandise & Superstores    21 
Home Furniture & Housewares Stores    18 
Beauty & Wellness    17 
Legal    17 
Security & Protective    16 
Membership Organizations    16 
Airlines, Airports & Air Transportation    15 
Restaurants & Cafes    14 
Grocery Stores    13 
Farm Support    12 
Hospitals & Health Clinics    12 
Vehicle Dealers    12 
Building & Personnel Services    11 
Travel Agencies    11 
Metal & Mineral Manufacturing    8 
Crop Production    8 
Gift, Novelty & Souvenir Stores    8 
Consumer Electronics & Appliances Stores    8 
Beauty & Personal Accessories Stores    8 
Ticket Sales    6 
Translation & Linguistic Services    6 
Stock Exchanges    6 
Commercial Equipment Services    6 
Audiovisual    6 
Media & Entertainment Stores    6 
General Repair & Maintenance    5 
Preschools & Child Care Services    5 
Mining & Metals    5 
Drug & Health Stores    5 
Law Firms    5 
Commercial Printing    4 
Pet & Pet Supplies Stores    4 
Biotechnology    3 
Food & Beverage Stores    3 
Consumer Product Rental    3 
Debt Relief    3 
Toy & Hobby Stores    3 
Catering & Food Service Contractors    3 
Car & Truck Rental    3 
Rail Transportation    3 
Medical Testing & Clinical Laboratories    2 
Convenience Stores    2 
Vehicle Repair & Maintenance    2 
Automotive Parts & Accessories Stores    2 
Forestry, Logging & Timber Operations    1 
Office Supply & Copy Stores    1 
Wood & Paper Manufacturing    1 
Religious Institutions    1 
Pet Care & Veterinary    1 
Pharmaceutical    1 


The number of unique values is 104
  
"""

"""
You are correct that using feature hashing alone without reducing the number of unique values 
may result in overfitting.
Feature hashing is primarily used to handle high-dimensional categorical features by mapping them
to a fixed-size feature space. 
However, it does not inherently reduce the number of unique values or address the issue of overfitting.

To mitigate the risk of overfitting and reduce the number of unique values in the 'Industry' column,
you can consider the following approaches:

1) Group infrequent categories:
You can group categories with low frequencies 
into a single category, such as 'Other' or 'Miscellaneous'.
This way, you reduce the number of unique values while still retaining some information
about the less frequent categories.

2) Group similar categories:
Analyze the unique values and identify categories that are similar in nature.
For example, you could group 'Health Care Services & Hospitals', 'Hospitals & Health Clinics',
and 'Medical Testing & Clinical Laboratories' into a single category called 'Health Care'.
This consolidation helps reduce the number of unique values while capturing the underlying similarity
in the industry types.

3) Domain knowledge or external resources:
Utilize domain knowledge or external resources to categorize or classify the industries into broader,
more meaningful groups.
For instance, you could create broader categories like 'Technology', 'Finance',
'Healthcare', 'Manufacturing', etc.
,and map the unique values to these categories based on their characteristics.

Once you have reduced the number of unique values through one of these approaches,
you can then apply feature hashing to further transform the categorical 
values into a fixed-size feature space.
This combined approach helps in handling the high dimensionality and potential overfitting
issues associated with a large number of unique values.

"""


# Dictionary of named industries and their frequencies
industry_freq = {
    'Unknown': 4289,
    'Information Technology Support Services': 1064,
    'Video Game Publishing': 919,
    'Computer Hardware Development': 615,
    'Internet & Web Services': 586,
    'Enterprise Software & Network Solutions': 514,
    'Aerospace & Defense': 480,
    'Health Care Services & Hospitals': 399,
    'Colleges & Universities': 344,
    'Business Consulting': 292,
    'Banking & Lending': 287,
    'Biotech & Pharmaceuticals': 247,
    'Software Development': 203,
    'Transportation Equipment Manufacturing': 201,
    'Advertising & Public Relations': 192,
    'Film Production': 183,
    'Insurance Carriers': 157,
    'Consumer Product Manufacturing': 148,
    'Electronics Manufacturing': 145,
    'Investment & Asset Management': 142,
    'HR Consulting': 130,
    'Machinery Manufacturing': 126,
    'Energy & Utilities': 121,
    'National Agencies': 107,
    'Research & Development': 87,
    'Sports & Recreation': 81,
    'Real Estate': 80,
    'Culture & Entertainment': 78,
    'Financial Transaction Processing': 77,
    'Telecommunications Services': 76,
    'Food & Beverage Manufacturing': 75,
    'Health Care Products Manufacturing': 74,
    'State & Regional Agencies': 71,
    'Broadcast Media': 64,
    'Architectural & Engineering Services': 57,
    'Construction': 55,
    'Wholesale': 48,
    'Gambling': 47,
    'Shipping & Trucking': 45,
    'Primary & Secondary Schools': 44,
    'Grantmaking & Charitable Foundations': 43,
    'Civic & Social Services': 43,
    'Accounting & Tax': 41,
    'Publishing': 40,
    'Cable, Internet & Telephone Providers': 36,
    'Chemical Manufacturing': 36,
    'Department, Clothing & Shoe Stores': 33,
    'Insurance Agencies & Brokerages': 32,
    'Education & Training Services': 32,
    'Municipal Agencies': 31,
    'Staffing & Subcontracting': 29,
    'Hotels & Resorts': 28,
    'Taxi & Car Services': 26,
    'Other Retail Stores': 23,
    'Sporting Goods Stores': 21,
    'General Merchandise & Superstores': 21,
    'Home Furniture & Housewares Stores': 18,
    'Beauty & Wellness': 17,
    'Legal': 17,
    'Security & Protective': 16,
    'Membership Organizations': 16,
    'Airlines, Airports & Air Transportation': 15,
    'Restaurants & Cafes': 14,
    'Grocery Stores': 13,
    'Farm Support': 12,
    'Hospitals & Health Clinics': 12,
    'Vehicle Dealers': 12,
    'Building & Personnel Services': 11,
    'Travel Agencies': 11,
    'Metal & Mineral Manufacturing': 8,
    'Crop Production': 8,
    'Gift, Novelty & Souvenir Stores': 8,
    'Consumer Electronics & Appliances Stores': 8,
    'Beauty & Personal Accessories Stores': 8,
    'Ticket Sales': 6,
    'Translation & Linguistic Services': 6,
    'Stock Exchanges': 6,
    'Commercial Equipment Services': 6,
    'Audiovisual': 6,
    'Media & Entertainment Stores': 6,
    'General Repair & Maintenance': 5,
    'Preschools & Child Care Services': 5,
    'Mining & Metals': 5,
    'Drug & Health Stores': 5,
    'Law Firms': 5,
    'Commercial Printing': 4,
    'Pet & Pet Supplies Stores': 4,
    'Biotechnology': 3,
    'Food & Beverage Stores': 3,
    'Consumer Product Rental': 3,
    'Debt Relief': 3,
    'Toy & Hobby Stores': 3,
    'Catering & Food Service Contractors': 3,
    'Car & Truck Rental': 3,
    'Rail Transportation': 3,
    'Medical Testing & Clinical Laboratories': 2,
    'Convenience Stores': 2,
    'Vehicle Repair & Maintenance': 2,
    'Automotive Parts & Accessories Stores': 2,
    'Forestry, Logging & Timber Operations': 1,
    'Office Supply & Copy Stores': 1,
    'Wood & Paper Manufacturing': 1,
    'Religious Institutions': 1,
    'Pet Care & Veterinary': 1,
    'Pharmaceutical': 1
}

# Set the threshold for infrequent categories to 50
# Identify infrequent categories
# infrequent_categories = [industry for industry, freq in industry_freq.items() if freq < 50]

# Replace infrequent categories with 'Other'
# df['Industry'] = df['Industry'].apply(lambda x: 'Other' if x in infrequent_categories else x)
# df['Industry'] = df['Industry'].apply(lambda x: 'Unknown' if x == '-1' else x)

# df.to_csv('DataBaseVar\DataBase_var2.csv', index=False)



# Hash the 'Industry' column
# hasher = FeatureHasher(n_features=10, input_type='string')
# hashed_features = hasher.transform(df['Industry'])
# hashed_df = pd.DataFrame(hashed_features.toarray())
# df = pd.concat([df.drop('Industry', axis=1), hashed_df], axis=1)

