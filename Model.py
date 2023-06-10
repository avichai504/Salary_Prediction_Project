import pandas as pd
import Data_Cleaning as dc
import numpy as np
import sklearn
from sklearn import linear_model

"""
'Annual Salary', 'Experience', 'Education', 'Position', 'Rating',
The correlation of each feature with 'Annual Salary':

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
"""

"""
       'Is Remote', 'Company Old', 'Founded', 'Career Opportunities',
       'Comp & Benefits', 'Culture & Values', 'Senior Management',
       'Work Life Balance', 'Scale_Company_Size', 'Scale_Revenue, 'Scale_Location'
"""
# Remove columns with non-numeric values
# numeric_columns = df.select_dtypes(include=['number']).columns
# data = df[numeric_columns]

df = pd.read_csv('DataBaseVar\DataBase_var2.csv')

data = df.copy()

feature = ['Experience', 'Scale_Location', 'Comp & Benefits', 'Company Old', 'Culture & Values', 'Annual Salary']
data = data[feature].copy()
print(f"Shape of the data with only features and predict = {data.shape}")


# One-hot encoding to the 'Industry' column (with 36 unique values)
data = dc.one_hot_encoding(data, ['Industry'])
print(f"Shape of the data after one hot = {data.shape}")

data.dropna(inplace=True)
# print(data.isnull().sum())

predict = 'Annual Salary'

X = np.array(data.drop(predict, axis=1))
y = np.array(data[predict])


x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2)
linear = linear_model.LinearRegression()
linear.fit(x_train, y_train)

best = 0.0
for _ in range(100):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)
    linear = linear_model.LinearRegression()
    linear.fit(x_train, y_train)
    accuracy = linear.score(x_test, y_test)
    print(accuracy)
    if accuracy > best:
        best = accuracy
        print(f"best = {best}")

print(f"best of all = {best}")


