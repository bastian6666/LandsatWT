import ee
import google.oauth2.credentials
import pywt
import folium

# Trigger the authentication flow.
ee.Authenticate(auth_mode='notebook')

# Initialize the library.
ee.Initialize(project='wavelet-project')


def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

folium.Map.add_ee_layer = add_ee_layer

# Define the geographical area and filtering criteria
point = ee.Geometry.Point([-99.9018, 41.4925])
region = point.buffer(10000).bounds()
l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA')\
        .filterDate('2022-01-01', '2023-12-31')\
        .filterBounds(region)\
        .filter(ee.Filter.lt('CLOUD_COVER', 20))

if l8.size().getInfo() > 0:
    image = l8.first()
    clipped_image = image.clip(region)
    vis_params = {
        'bands': ['B4', 'B3', 'B2'],
        'min': 0,
        'max': 1,  # Adjusted for typical scaled TOA reflectance values
        'gamma': 1
    }

    map = folium.Map(location=[41.4925, -99.9018], zoom_start=10)
    map.add_ee_layer(clipped_image, vis_params, "Landsat 8 TOA Image")
    map.add_child(folium.LayerControl())
    map # Explicitly display the map in the notebook
else:
    print("No images found for the specified filters and date range.")