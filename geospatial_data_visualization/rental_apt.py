import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster, HeatMap
from shapely.geometry import Point
import geopandas as gpd
import webbrowser

df = pd.read_csv('rent.csv', encoding = 'gbk')
print(df.head())


# MarkerCluster

m1 = folium.Map(location = [31.2304, 121.4737], zoom_start = 11)
marker_cluster = MarkerCluster().add_to(m1)
 
# add a marker for each apartment, add it to the cluster, not the map
for name, row in df.iterrows():
    popup = "{0}：{1} m^2, ￥{2}".format(row['name'], row['area'], row['rent'])
    folium.RegularPolygonMarker([row['y'], row['x']], popup = popup, 
                                number_of_sides = 10, radius = 5, fill_color = 'red', color = 'red',
                               opacity = 0.8, fill_opacity = 0.8).add_to(marker_cluster)


m1.save('rental_apt.html')
webbrowser.open('rental_apt.html')


# HeatMap

m2 = folium.Map(location = [31.2304, 121.4737], zoom_start = 10)

num = len(df.x)
lat = np.array(df['y'][0:num])
lon = np.array(df['x'][0:num])


data = [[lat[i], lon[i]] for i in range(num)]

HeatMap(data, radius = 18).add_to(m2)

m2.save('rental_apt_heatmap.html')
webbrowser.open('rental_apt_heatmap.html')


# Choropleth Map

sh = gpd.read_file('shanghai.json')
geometry = [Point(xy) for xy in zip(df.x, df.y)]
gdf = gpd.GeoDataFrame(df, crs = sh.crs, geometry = geometry)

apt_sh = gpd.sjoin(sh, gdf, op = 'contains')
print(apt_sh.head())


# calculating total number of rental apartments per district
counts = apt_sh.groupby(['name_left']).size()
apt_counts = pd.DataFrame(counts)
apt_counts.reset_index(level = 0, inplace = True)
apt_counts.columns = ['district', 'apt_count']
                     
districts_with_counts = pd.merge(apt_sh, apt_counts, left_on = 'name_left', right_on = 'district')
districts_with_counts['area'] = districts_with_counts.geometry.area
                      
#districts_with_counts['density'] = districts_with_counts.apply(lambda row: row.apt_count/row.area, axis = 1)                      
  
# creation of the choropleth
m3 = folium.Map(location = [31.2304, 121.4737], zoom_start = 9)
folium.Choropleth(geo_data = districts_with_counts, 
              name = 'geometry',
              data = districts_with_counts,
              columns = ['district', 'apt_count'],
              key_on = 'feature.properties.district',
              fill_color = 'BuPu', 
              fill_opacity = 0.4, 
              line_opacity = 0.2,
              legend_name = 'Number of rental apartments per district',
              reset = True).add_to(m3)

m3.save('rental_apt_choropleth.html')
webbrowser.open('rental_apt_choropleth.html')

