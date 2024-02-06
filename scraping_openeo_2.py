#!/usr/bin/python3

import json
import socket
from flask import Flask, app
import openeo
from flask_sock import Sock
import numpy as np
import asyncio
import rasterio


# First, we connect to the back-end and authenticate.
con = openeo.connect("openeo.dataspace.copernicus.eu")
con.authenticate_oidc()

app = Flask(__name__)
app.debug = False
sock = Sock(app)


@app.route("/")
def home():
    return "<h1>Classification Server</h1>"


@sock.route("/echo")
def ws_process(ws):
    while True:
        data = ws.receive()
        ws.send("Classification Server is echoing: " + data)


def get_satelite_image(
    south=20.009732,
    west=-90.518366,
    north=20.089912,
    east=-90.499288,
    start_date="2021-02-01",
    end_date="2021-02-02",
):
    # Now that we are connected, we can initialize our datacube object with the area of interest
    # and the time range of interest using Sentinel 1 data.
    datacube = con.load_collection(
        "SENTINEL2_L2A",
        spatial_extent={
            "south": south,
            "west": west,
            "north": north,
            "east": east,
        },
        temporal_extent=[start_date, end_date],
        bands=["B02", "B03", "B04", "B08", "B12"],
        max_cloud_cover=85,
    )

    # SW: 20.009732, -90.518366
    # EN: 20.089912, -90.499288

    # By filtering as early as possible (directly in load_collection() in this case),
    # we make sure the back-end only loads the data we are interested in and avoid incurring unneeded costs.

    # From this data cube, we can now select the individual bands with the DataCube.band() method and rescale the digital number values to physical reflectances:
    blue = datacube.band("B02") * 0.0001
    green = datacube.band("B03") * 0.0001
    red = datacube.band("B04") * 0.0001
    nir = datacube.band("B08") * 0.0001
    swir = datacube.band("B12") * 0.0001
    ndvi = (nir - red) / (nir + red)
    ndwi = (green - nir) / (green + nir)
    mi = (nir - swir) / (nir + swir)

    blue.download("blue.tiff")
    green.download("green.tiff")
    red.download("red.tiff")
    nir.download("nir.tiff")
    swir.download("swir.tiff")
    ndvi.download("ndvi.tiff")
    ndwi.download("ndwi.tiff")
    mi.download("mi.tiff")

    toRet = np.array([])

    features = ["blue", "green", "red", "nir", "swir", "ndvi", "ndwi", "mi"]
    arrs = []
    for feature in features:
        with rasterio.open(f"{feature}.tiff") as src:
            data = src.read()
            print(data)
            arrs.append(data)

    toRet = np.array(arrs)

    # convert from openeo datacube to numpy array

    # blue = np.array(blue, dtype=np.float64)
    # green = np.array(green)
    # red = np.array(red)
    # nir = np.array(nir)
    # swir = np.array(swir)

    # ndvi = np.divide(nir - red, nir + red, where=(nir + red != 0), dtype=np.float64)

    # ndwi = np.divide(
    #     green - nir, green + nir, where=(green + nir != 0), dtype=np.float64
    # )

    # mi = np.divide(nir - swir, nir + swir, where=(nir + swir != 0), dtype=np.float64)

    return toRet


@sock.route("/ws-satelite-image")
def ws_satelite_image(ws):
    while True:
        print("ws_satelite_image")

        d = ws.receive()
        print(d)
        ws.send("Hello, " + d)
        data = json.loads(d)
        south = data["south"]
        west = data["west"]
        north = data["north"]
        east = data["east"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        result = get_satelite_image(south, west, north, east, start_date, end_date)
        print(result.shape)
        ws.send(result)
    # spatial_extent={
    #         "south": 20.104,
    #         "west": -90.478,
    #         "north": 20.111,
    #         "east": -90.474,
    #     },


if __name__ == "__main__":
    app.run(debug=False, port=5001, host="0.0.0.0")
