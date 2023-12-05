import openeo

# the central gateway to the OpenEO platform
connection = openeo.connect("https://earthengine.openeo.org")

connection.authenticate_basic("group1", "test123")

# https://openeo.org/documentation/1.0/python/#creating-a-datacube
datacube = connection.load_collection(
    "COPERNICUS/S2",
    spatial_extent={"west": 16.06, "south": 48.06, "east": 16.65, "north": 48.35},
    temporal_extent=["2017-03-01", "2017-04-01"],
    bands=["B4", "B8"],
)

result = datacube.save_result("PNG")
result.download("output.png")
