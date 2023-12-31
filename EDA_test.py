#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV


# In[3]:


data=pd.read_csv("E:/sliit/Year 3/SEM 1/FDM/Project/Customer-Churn-Prediction-System/Dataset/WA_Fn-UseC_-Telco-Customer-Churn.csv")


# In[4]:


data.head()


# In[5]:


def dataoveriew(df, message):
    print(f'{message}:\n')
    print('Number of rows: ', df.shape[0])
    print("\nNumber of Columns:", df.shape[1])
    print("\nData Features:")
    print(df.columns.tolist())
    print("\nData Types:\n",data.dtypes)
    print("\nDupicate Values:",data.duplicated().sum())
    print("\nUnique values:")
    print(df.nunique())

dataoveriew(data, 'Overview of the dataset')


# # Find Null Values

# In[6]:


data.isnull().sum()


# # Explore target variable

# In[7]:


churn_counts = data['Churn'].value_counts()

plt.figure(figsize=(3, 3))
plt.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Churn Distribution')
plt.show()


# # Compare categorical variables with churn column

# In[8]:


#Defining bar chart function
def bar(feature, df=data ):
    #Groupby the categorical feature
    temp_df = df.groupby([feature, 'Churn']).size().reset_index()
    temp_df = temp_df.rename(columns={0:'Count'})
    #Calculate the value counts of each distribution and it's corresponding Percentages
    value_counts_df = df[feature].value_counts().to_frame().reset_index()
    categories = [cat[1][0] for cat in value_counts_df.iterrows()]
    #Calculate the value counts of each distribution and it's corresponding Percentages
    num_list = [num[1][1] for num in value_counts_df.iterrows()]
    div_list = [element / sum(num_list) for element in num_list]
    percentage = [round(element * 100,1) for element in div_list]
    #Defining string formatting for graph annotation
    #Numeric section
    def num_format(list_instance):
        formatted_str = ''
        for index,num in enumerate(list_instance):
            if index < len(list_instance)-2:
                formatted_str=formatted_str+f'{num}%, ' #append to empty string(formatted_str)
            elif index == len(list_instance)-2:
                formatted_str=formatted_str+f'{num}% & '
            else:
                formatted_str=formatted_str+f'{num}%'
        return formatted_str
    #Categorical section
    def str_format(list_instance):
        formatted_str = ''
        for index, cat in enumerate(list_instance):
            if index < len(list_instance)-2:
                formatted_str=formatted_str+f'{cat}, '
            elif index == len(list_instance)-2:
                formatted_str=formatted_str+f'{cat} & '
            else:
                formatted_str=formatted_str+f'{cat}'
        return formatted_str


    #Running the formatting functions
    num_str = num_format(percentage)
    cat_str = str_format(categories)

    #Setting graph framework
    fig = px.bar(temp_df, x=feature, y='Count', color='Churn', title=f'Churn rate by {feature}', barmode="group", color_discrete_sequence=["#3700B3", "#03DAC6"])
    fig.add_annotation(
                text=f'Value count of distribution of {cat_str} are<br>{num_str} percentage respectively.',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.25,  # Adjust the x-coordinate to move the box to the left
                y=1.15,   # Adjust the y-coordinate to move the box higher or lower
                bordercolor='black',
                borderwidth=1)
    fig.update_layout(
        # margin space for the annotations on the right
        margin=dict(r=400),
    )

    return fig.show()


# In[9]:


bar('StreamingMovies')
bar('PaperlessBilling')
bar('Contract')
bar('Dependents')
bar('Partner')
bar('InternetService')
bar('PhoneService')
bar('gender')
bar('SeniorCitizen')


# In[10]:


#replace no internet service in to NO and no phone service in to No
data.replace('No internet service','No',inplace=True)
data.replace('No phone service','No',inplace=True)


# In[11]:


def print_unique_col_values(data):

 for column in data:
   if data[column].dtypes=='object':
     print(f'{column} : {data[column].unique()}')
print_unique_col_values(data)


# In[12]:


# Save the updated DataFrame to the CSV file
data.to_csv('E:/sliit/Year 3/SEM 1/FDM/Project/Customer-Churn-Prediction-System/Dataset/Telco-Customer-Churn.csv', index=False)


# In[13]:


bar('MultipleLines')
bar('OnlineSecurity')
bar('OnlineBackup')
bar('DeviceProtection')
bar('StreamingTV')
bar('StreamingMovies')
bar('TechSupport')


# # Explore Numeric Features

# In[14]:


# Convert "TotalCharges" column to float
data["TotalCharges"] = pd.to_numeric(data["TotalCharges"], errors="coerce")

# Verify the updated data types
print(data.dtypes)


# # Fill the Null values with median
# 

# In[15]:


# Fill missing values with the median
median_value = data["TotalCharges"].median()
data["TotalCharges"].fillna(median_value,inplace=True)

# Verify the updated columnprint(data["TotalCharges"])


# In[16]:


data.isnull().sum()


# In[17]:


# Save the updated DataFrame to the CSV file
data.to_csv('E:/sliit/Year 3/SEM 1/FDM/Project/Customer-Churn-Prediction-System/Dataset/Telco-Customer-Churn.csv', index=False)


# # Exploring the Outliers

# In[18]:


import matplotlib.pyplot as plt

# Assuming you have a 'data' variable containing the necessary data

# Create a list of data to plot
data_to_plot = [data['tenure'], data['MonthlyCharges'], data['TotalCharges']]

# Create a list of labels for the box plots
labels = ['tenure', 'MonthlyCharges', 'TotalCharges']

# Create separate figures and axes for each box plot
for i in range(len(data_to_plot)):
    fig, ax = plt.subplots()

    # Plot the box plot for the current variable
    ax.boxplot(data_to_plot[i], vert=False)

    # Set the title and axes labels for the current plot
    ax.set_title(f'Box Plot of {labels[i]}')
    ax.set_xlabel('Values')
    ax.set_ylabel(labels[i])

    # Display the plot
    plt.show()


# It seems that there are no outliers in tenure , monthlycharges and totalcharges columns

# # Data Transformation

# Simplifying the dataset by binning on numerical variables (tenure, MonthlyCharges, and TotalCharges) and transforms them into categorical variables with three levels: 'low', 'medium', and 'high'.

# In[19]:


#Create an empty dataframe
bin_df = pd.DataFrame()

#Update the binning dataframe
bin_df['tenure_bins'] =  pd.qcut(data['tenure'], q=3, labels= ['low', 'medium', 'high'])
bin_df['MonthlyCharges_bins'] =  pd.qcut(data['MonthlyCharges'], q=3, labels= ['low', 'medium', 'high'])
bin_df['TotalCharges_bins'] =  pd.qcut(data['TotalCharges'], q=3, labels= ['low', 'medium', 'high'])
bin_df['Churn'] = data['Churn']

#Plot the bar chart of the binned variables
bar('tenure_bins', bin_df)
bar('MonthlyCharges_bins', bin_df)
bar('TotalCharges_bins', bin_df)


# 
# Based on binning, the low tenure and high monthly charge bins have higher churn rates as supported with the previous analysis. While the low Total charge bin has a higher churn rate.

# # Data Preprocessing

# In[20]:


#Encording the Categorical Features

# yes and no replace with 1 and 0
yes_no_columns = ['Partner','Dependents','PhoneService','MultipleLines','OnlineSecurity','OnlineBackup','DeviceProtection',
                        'TechSupport','StreamingTV','StreamingMovies','PaperlessBilling','Churn']
for col in yes_no_columns:
  data[col].replace({'Yes':1,'No': 0},inplace=True)

#one hot encoding to other columns
data= pd.get_dummies(data=data,columns=['InternetService','Contract','PaymentMethod'])
data.columns

#geneder column
data['gender'].replace({'Female':0,'Male':1},inplace=True)


# In[21]:


# Save the updated DataFrame to the CSV file
data.to_csv('E:/sliit/Year 3/SEM 1/FDM/Project/Customer-Churn-Prediction-System/Dataset/Telco-Customer-Churn.csv', index=False)


# In[22]:


print(data.dtypes)


# In[23]:


#reindexing the dataset
column_name = 'Churn'

# Get a list of column names excluding the column to be moved
other_columns = [col for col in data.columns if col != column_name]

# Reorder the DataFrame with the column moved to the last position
data = data[other_columns + [column_name]]

data.head()


# In[24]:


# Save the updated DataFrame to the CSV file
data.to_csv('E:/sliit/Year 3/SEM 1/FDM/Project/Customer-Churn-Prediction-System/Dataset/Telco-Customer-Churn.csv', index=False)


# In[25]:


# Checking the correlation between features
corr = data.corr(numeric_only=True)

fig = go.Figure(data=go.Heatmap(
                   z=corr.values,
                   x=corr.columns,
                   y=corr.index,
                   colorscale='Viridis'))

fig.update_layout(
    title='Correlation Matrix',
    width=1000,
    height=1000,
    xaxis_title='Features',
    yaxis_title='Features')

fig.show()


# Correlation refers to the statistical relationship or association between two or more variables. It measures the strength and direction of the linear relationship between variables, indicating how changes in one variable are related to changes in another variable.
# 
# - A positive correlation (r > 0) indicates that as one variable increases, the other variable tends to increase as well. The closer the value of r is to +1, the stronger the positive correlation.
# - A negative correlation (r < 0) indicates that as one variable increases, the other variable tends to decrease. The closer the value of r is to -1, the stronger the negative correlation.
# - A correlation of 0 (r = 0) indicates no linear relationship between the variables.
# 

# In[26]:


#Change variable name seperators to '_'
all_columns = [column.replace(" ", "_").replace("(", "_").replace(")", "_").replace("-", "_") for column in data.columns]
data.columns=all_columns


# In[27]:


print(data.dtypes)


# In[28]:


#Feature Scaling
cols_to_scale=['tenure','MonthlyCharges','TotalCharges']

scaler = MinMaxScaler()

data[cols_to_scale] = scaler.fit_transform(data[cols_to_scale])


# In[29]:


data.head()


# In[30]:


# Save the updated DataFrame to the CSV file
data.to_csv('E:/sliit/Year 3/SEM 1/FDM/Project/Customer-Churn-Prediction-System/Dataset/Telco-Customer-Churn.csv', index=False)


# In[31]:


#Droping the unuseful columns
data.drop(["customerID"],axis=1,inplace = True)


# In[32]:


churn_counts = data['Churn'].value_counts()
print(churn_counts)

plt.figure(figsize=(3, 3))
plt.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Churn Distribution')
plt.show()



# Data set is unbalanced

# In[33]:


#balancing the dataset using SMOTE oversampling method

X= data.drop('Churn',axis='columns')
y=data['Churn']
y.value_counts()

smote = SMOTE(sampling_strategy='minority')
X_sm, y_sm = smote.fit_resample(X,y)

y_sm.value_counts()


# In[34]:


X_sm.shape


# In[35]:


y_sm


# # Model Creation

# In[36]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report

# Splitting the balanced dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_sm, y_sm, test_size=0.2, random_state=42)


# In[37]:


# Create and train the  LogisticRegression  model
log_model = LogisticRegression()
log_model.fit(X_train, y_train)

# Making predictions on the test set
y_pred = log_model.predict(X_test)

# Evaluating the model
print("Logistic Regression")
print(classification_report(y_test, y_pred))


# In[38]:


# Create and train the Decision Tree model
dt_model = DecisionTreeClassifier()
dt_model.fit(X_train, y_train)

dt_y_pred = dt_model.predict(X_test)

print("Decision Tree:")
print(classification_report(y_test, dt_y_pred))


# In[39]:


# Create and train the Naive Bayes model
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)

nb_y_pred = nb_model.predict(X_test)

print("Naive Bayes:")
print(classification_report(y_test, nb_y_pred))


# In[40]:


# Create and train the SVM model
svm_model = SVC()
svm_model.fit(X_train, y_train)

svm_y_pred = svm_model.predict(X_test)

print("Support Vector Machine:")
print(classification_report(y_test, svm_y_pred))


# In[41]:


# Create and train the Random Forest model
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)

rf_y_pred = rf_model.predict(X_test)

print("Random Forest:")
print(classification_report(y_test, rf_y_pred))


# ## Compare accuracy scores of each model

# In[42]:


accuracy_scores = {
    'Logistic Regression': accuracy_score(y_test, y_pred),
    'Decision Tree': accuracy_score(y_test, dt_y_pred),
    'Naive Bayes': accuracy_score(y_test, nb_y_pred),
    'Support Vector Machine': accuracy_score(y_test, svm_y_pred),
    'Random Forest': accuracy_score(y_test, rf_y_pred)
}

# Set the figure size
plt.figure(figsize=(10, 6))

# Plot the bar graph
plt.bar(accuracy_scores.keys(), accuracy_scores.values())
plt.xlabel('Models')
plt.ylabel('Accuracy')
plt.title('Accuracy Comparison of Different Models')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

plt.tight_layout()  # Adjust the layout to prevent label cutoff
plt.show()


# ## Improve best model by hyperparameter tuning

# In[43]:


# Define the Random Forest model
rf_model = RandomForestClassifier()

# Define the parameter grid
param_grid = {
    'n_estimators': [100, 300, 500],
    'max_features': ['sqrt', 'log2'],
    'max_depth': [None, 5, 10],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'bootstrap': [True, False]
}

# Perform grid search with cross-validation
grid_search = GridSearchCV(rf_model, param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Get the best model and its predictions
best_rf_model = grid_search.best_estimator_
rf_y_pred = best_rf_model.predict(X_test)

# Evaluate the model
print("Random Forest (after parameter tuning):")
print(classification_report(y_test, rf_y_pred))


# In[44]:


# Fit the model
best_rf_model.fit(X_train, y_train)


# In[45]:


#Saving best model 
import joblib
#Sava the model to disk
filename = 'model.sav'
joblib.dump(best_rf_model, filename)


# In[ ]:





# In[ ]:




