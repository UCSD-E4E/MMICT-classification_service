import openeo

# the central gateway to the OpenEO platform
connection = openeo.connect("https://earthengine.openeo.org")
connection.authenticate_basic("group11", "test123")

# Now that we are connected, we can initialize our datacube object with the area around Vienna
# and the time range of interest using Sentinel 1 data.
datacube = connection.load_collection(
    "COPERNICUS/S1_GRD",
    spatial_extent={"west": 16.06, "south": 48.06, "east": 16.65, "north": 48.35},
    temporal_extent=["2017-03-01", "2017-06-01"],
    bands=["VV"],
)

# Since we are creating a monthly RGB composite, we need three (R, G and B) separated time ranges.
# Therefore, we split the datacube into three datacubes by filtering temporal for March, April and May.
march = datacube.filter_temporal("2017-03-01", "2017-04-01")
april = datacube.filter_temporal("2017-04-01", "2017-05-01")
may = datacube.filter_temporal("2017-05-01", "2017-06-01")

# Now that we split it into the correct time range, we have to aggregate the timeseries values into a single image.
# Therefore, we make use of the Python Client function `mean_time`, which reduces the time dimension,
# by taking for every timeseries the mean value.

mean_march = march.mean_time()
mean_april = april.mean_time()
mean_may = may.mean_time()

# Now the three images will be combined into the temporal composite.
# Before merging them into one datacube, we need to rename the bands of the images, because otherwise,
# they would be overwritten in the merging process.
# Therefore, we rename the bands of the datacubes using the `rename_labels` process to "R", "G" and "B".
# After that we merge them into the "RGB" datacube, which has now three bands ("R", "G" and "B")

R_band = mean_march.rename_labels(dimension="bands", target=["R"])
G_band = mean_april.rename_labels(dimension="bands", target=["G"])
B_band = mean_may.rename_labels(dimension="bands", target=["B"])

RG = R_band.merge_cubes(G_band)
RGB = RG.merge_cubes(B_band)


# Last but not least, we add the process to save the result of the processing. There we define that
# the result should be a GeoTiff file.
# We also set, which band should be used for "red", "green" and "blue" color in the options.

RGB = RGB.save_result(format="PNG", options={"red": "R", "green": "G", "blue": "B"})

# With the last process we have finished the datacube definition and can create and start the job at the back-end.

job = RGB.create_job()
job.start_and_wait().download_results()
