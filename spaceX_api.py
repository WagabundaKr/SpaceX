import requests
import pandas as pd
import numpy as np
import datetime


#Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []



def getBoosterVersion(data):
    # Takes the dataset and uses the rocket column to call the API and append the data to the list
    # From the 'rocket' column we would like to learn the booster name
    for x in data['rocket']:
       if x:
        response = requests.get("https://api.spacexdata.com/v4/rockets/" +str(x)).json()
        BoosterVersion.append(response['name'])

def getLaunchSite(data):
    # Takes the dataset and uses the launchpad column to call the API and append the data to the list
    # From the 'launchpad' we would like to know the name of the launch site being used, the logitude, and the latitude.
    for x in data['launchpad']:
       if x:
         response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
         Longitude.append(response['longitude'])
         Latitude.append(response['latitude'])
         LaunchSite.append(response['name'])

def getPayloadData(data):
    # Takes the dataset and uses the payloads column to call the API and append the data to the lists
    # From the 'payload' we would like to learn the mass of the payload and the orbit that it is going to.
    for load in data['payloads']:
       if load:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])

def getCoreData(data):
    # Takes the dataset and uses the cores column to call the API and append the data to the lists
    # From 'cores'</code>' we would like to learn the outcome of the landing, the type of the landing, 
    # number of flights with that core, whether gridfins were used, wheter the core is reused, 
    # wheter legs were used, the landing pad used, the block of the core which is a number 
    # used to seperate version of cores, the number of times this specific core has been reused, 
    # and the serial of the core.
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])



# spacex_url="https://api.spacexdata.com/v4/launches/past"
# response = requests.get(spacex_url)

# To make the requested JSON results more consistent, we will use the following static response object for this project:
static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
response=requests.get(static_json_url)

# check content of the response
# print(response.content)
# We should see that the request was successfull with the 200 status response code
# print(response.status_code)

data = pd.json_normalize(response.json())
# print(type(data))
# print(data.head())

# Lets take a subset of our dataframe keeping only the features we want and the flight number, and date_utc.
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])

# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]





getBoosterVersion(data)
getLaunchSite(data)
getPayloadData(data)
getCoreData(data)

launch_dict = {'FlightNumber': list(data['flight_number']),
               'Date': list(data['date']),
               'BoosterVersion':BoosterVersion,
               'PayloadMass':PayloadMass,
               'Orbit':Orbit,
               'LaunchSite':LaunchSite,
               'Outcome':Outcome,
               'Flights':Flights,
               'GridFins':GridFins,
               'Reused':Reused,
               'Legs':Legs,
               'LandingPad':LandingPad,
               'Block':Block,
               'ReusedCount':ReusedCount,
               'Serial':Serial,
               'Longitude': Longitude,
               'Latitude': Latitude}

launch_df = pd.DataFrame(launch_dict)

# Finally we will remove the Falcon 1 launches keeping only the Falcon 9 launches
data_falcon9 = launch_df[launch_df['BoosterVersion'] != 'Falcon 1']

# Now that we have removed some values we should reset the FlgihtNumber column
data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))



# Data Wrangling:
# We can see below that some of the rows are missing values in our dataset.
# print(data_falcon9.isnull().sum())

PayloadMass_mean = data_falcon9['PayloadMass'].mean()
data_falcon9['PayloadMass'].replace(np.nan, PayloadMass_mean, inplace=True)
# print(data_falcon9.isnull().sum())

data_falcon9.to_csv('/Users/iryna/python/DA/full_project/dataset_part1.csv', index=False)
print(data_falcon9.head())