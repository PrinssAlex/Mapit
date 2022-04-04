#import needed libraries
import pandas as pd
import folium as fl
from folium.plugins import BeautifyIcon
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
mapit = fl.Map(location=[48.77, -121.81], zoom_start = 7, tiles='Stamen Terrain')
#FeatureGroup method added to group marker layers together
fg_mkr = fl.FeatureGroup(name='markers')
# a For-loop to iterate through the df and fill the map object to produce the needed markers on the map
for lt,ln,el,nm in zip(lat,lon,elv,name):
    html_data = f''' Volcano Name: <a onMouseOver = "this.style.color = 'Tomato'", onMouseOut = "This.style.color = 'Red'", \
        style = 'text-decoration: none; color: red;', href = 'https://www.google.com/search?q= mount {nm}', \
             target = '_blank'> {nm} .</a> <br> \
                 <i style = 'display: inline-block; font-size: 12px; color: Gray;'> (click name for more info)</i> <br>
                 Height: {el} m '''
    iframe_obj = fl.IFrame(html=html_data, width=220, height=80) # create's an interactive frame that pop's up on clicking the marker
    fg_mkr.add_child(fl.CircleMarker(location=[lt,ln], radius=6, popup=fl.Popup(iframe_obj), fill_color=el_Icon(el), \
        color=el_color(el), fill_opacity=0.7, tooltip=f'mount {nm}', parse_html=True ) ) 
#FeatureGroup added to group polygon (mark out territories on the map) layer together - adds a chloropleth feature
fg_pol = fl.FeatureGroup(name='polygons')
fg_pol.add_child( fl.GeoJson( data= open('Geo_JSON.json', 'r', encoding='utf-8-sig').read() ,
style_function=lambda x: {'fillColor':'yellow' if x['properties']['POP2005'] < 10000000 else 'orange' if 
10000000 <= x['properties']['POP2005'] < 20000000 else 'red' } ) ) #adding a color overlay wrt country populationn using a lambda function
# Add feature group to map
mapit.add_child(fg_mkr)
mapit.add_child(fg_pol)
# Add layers to map layer control
mapit.add_child(fl.LayerControl())
# Save map to local machine
mapit.save('mapit.html')

