# -*- coding: utf-8 -*-
"""UniVerse.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WcaubRyucovlsbzSz8aT3CEJg1nj1_lP
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, accuracy_score

collegeData = pd.read_csv("Admission_Predict_Ver1.1.csv")
trimColNames = [name.strip() for name in collegeData.columns]
collegeData.columns = trimColNames

collegeData.head()

"""Breakdown of Attributes
GRE Score - Out of 340
TOEFL Score - Out of 120
University Rating - Between 1 to 5 (5 being the best)
SOP - Between 1 to 5 (5 being the best)
LOR - Between 1 to 5 (5 being the best)
CGPA - Out of 10
Research - 1 if student has research experience, else 0
Chance of Admit - Probability of getting accepted into graduate program
"""

collegeData = collegeData.drop("Serial No.", axis = 1)

collegeData["Research"].dtype

collegeData["Research"] = collegeData["Research"].astype('category')

correlation_matrix = collegeData.iloc[:,:].corr().round(2)
sns.heatmap(data=correlation_matrix, annot=True)

sns.catplot(data = collegeData, x = "Research", y = "Chance of Admit")

X = collegeData.iloc[:,0:7]
y = collegeData.iloc[:,7]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1005)

rf = RandomForestRegressor(n_estimators=250,
                           max_features=(2/7),
                           min_samples_split=5,
                           n_jobs=2,
                           random_state=1005)

rf.fit(X_train, y_train)

train_predictions = rf.predict(X_train)
test_predictions = rf.predict(X_test)

train_mse = np.sqrt(mean_squared_error(y_train, train_predictions))
test_mse = np.sqrt(mean_squared_error(y_test, test_predictions))
train_r2 = rf.score(X_train, y_train)
test_r2 = rf.score(X_test, y_test)

print("Train MSE ::", train_mse)
print("Test MSE ::", test_mse)
print("Train R^2 ::", train_r2)
print("Test R^2 ::", test_r2)

features = X.columns
importances = rf.feature_importances_
indices = np.argsort(importances)

plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()

newPerson = [[330, 110, 4, 4.5, 4.5, 9.5, 0]]

pred = rf.predict(newPerson)
pred[0]