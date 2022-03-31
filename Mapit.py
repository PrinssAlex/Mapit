#import needed libraries
import pandas as pd
import folium as fl
df = pd.read_csv('volcano.txt')  # path to csv file 
# df should have columns corresponding to the fllg columns or the codes below should be edited to include the respective columns
lat = list(df['LAT'])
lon = list(df['LON'])
elv = list(df['ELEV'])
name = list(df['NAME'])
# create funcion to determine marker and marker icon color based on mountain elevation height
def el_color(elevation):
    if elevation > 3000:
        return 'red'
    elif elevation > 1500:
        return 'orange'
    else:
        return 'cadetblue'
def el_Icon(elevation):
    if elevation > 3000:
        return 'white'
    elif elevation > 1500:
        return 'beige'
    else:
        return 'lightgray'
# map object. Must be created at the start of any map application development
mappit = fl.Map(location=[48.77, -121.81], zoom_start = 7, tiles='Stamen Terrain')
# a For-loop to iterate through the df and fill the map object to produce the needed markers on the map
for lt,ln,el,nm in zip(lat,lon,elv,name):
    html_data = f''' Volcano Name: <a onMouseOver = "this.style.color = 'Tomato'", onMouseOut = "This.style.color = 'Red'", \
        style = 'text-decoration: none; color: red;', href = 'https://www.google.com/search?q= mount {nm}', \
             target = '_blank'> {nm} .</a> <br> \
                 <i style = 'display: inline-block; font-size: 12px; color: Gray;'> (click name for more info)</i> <br>
                 Height: {el} m '''
    iframe_obj = fl.IFrame(html=html_data, width=220, height=80) # create's an interactive frame that pop's up on clicking the marker
    mappit.add_child(fl.Marker(location=[lt, ln], popup=fl.Popup(iframe_obj), icon=fl.Icon(color=el_color(el), icon_color=el_Icon(el), icon='info-sign', prefix='fa'), tooltip=f'mount {nm}')) #create's markers on the map

mappit.save('mapit.html')

