#import ArcGis from the geopy library 
#this will allow us to retrieve the coordinates of the companies in San Francisco (latitude and latitude),
#using only their Full Address ie: Address, City, State and Country 
from geopy.geocoders import ArcGIS

#import os
#os.listdir()

#store the ArcGis object in a variable 
nom = ArcGIS()

#import pandas so we read the csv file containing the companies' various info 
import pandas 
df = pandas.read_csv('supermarkets-semi-colons.txt',sep=';') #ensure you specify that the columns are separated
                                                            #by a semi-colon in this file 

#Create a new column, which contains the the Full Address of the company,
# by combining the location info in the other columns 
df['Full Address'] = df['Address'] + ',' + df['City'] + ',' + df['State'] + ',' + df['Country']

#afterwards, create a coordinates column to store the latitude and longitude of each company
#this is acheived by applying a geocode function to the 'Full Address' column, by utilizing the ArcGis object
df['Coordinates'] = df['Full Address'].apply(nom.geocode)
#print(df['Coordinates'][0])

#separate the latitude and longitude into different columns by using a lambda function
df['Latitude'] = df['Coordinates'].apply(lambda x: x.latitude if x != None else None)
df['Longitude'] = df['Coordinates'].apply(lambda y: y.longitude if y != None else None)

#now import folium and mark the locations of each company on the map using the data above 
#Folium explanation can be found on my previous GIS Git Repo 
import folium 
map = folium.Map(location=[37.75,-122.42],tiles='Stamen Terrain',zoom_start=12)
lat = list(df['Latitude'])
lon = list(df['Longitude'])
nme = list(df['Name'])

fg = folium.FeatureGroup(name='My Map')


for lat, lon, nme in zip(lat,lon,nme):
    html = f"""
    Company name:<br>
    <a href="https://www.google.com/search?q=%22{nme}%22" target="_blank">{nme}</a><br>
    """
    iframe = folium.IFrame(html = html, width = 200, height = 100)
    fg.add_child(folium.Marker(location=[lat,lon], popup= folium.Popup(iframe),icon=folium.Icon(color='red')))
    

map.add_child(fg)
map.save('Map1.html')