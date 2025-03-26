import pandas as pd
import numpy as np

df = pd.read_csv('/Users/iryna/python/DA/full_project/dataset_part1.csv')

# Identify and calculate the percentage of the missing values in each attribute
print(df.isnull().sum()/len(df)*100)

# Identify which columns are numerical and categorical:
print(df.dtypes)

### TASK 1: Calculate the number of launches on each site
print(df['LaunchSite'].value_counts())

### TASK 2: Calculate the number and occurrence of each orbit
print(df['Orbit'].value_counts())

### TASK 3: Calculate the number and occurence of mission outcome of the orbits
landing_outcomes = df['Outcome'].value_counts()

# We create a set of outcomes where the second stage did not land successfully:
for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])

### TASK 4: Create a landing outcome label from Outcome column
# landing_class = [0 if outcome in bad_outcome else 1 for outcome in df['Outcome']]
landing_class = []
for outcome in df['Outcome']:
    if outcome in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)

df['Class']=landing_class

# We can use the following line of code to determine  the success rate:
print(df["Class"].mean())

df.to_csv("/Users/iryna/python/DA/full_project/dataset_part_2.csv", index=False)

# Date	Time (UTC)	Booster_Version	Launch_Site	Payload	PAYLOAD_MASS__KG_	Orbit	Customer	Mission_Outcome	Landing_Outcome


print(df.head())