"""
This is an example of loading
in data in a package wheel file
"""

import json
import numpy as np
import pkg_resources


# Reading the csv data
def staff():
    stream = pkg_resources.resource_stream(__name__, "agency.csv")
    df = np.genfromtxt(stream, delimiter=",", skip_header=1)
    return df


# Reading the metadata
def metaf():
    stream = pkg_resources.resource_stream(__name__, "notes.json")
    res = json.load(stream)
    return res


# just having it available as object
metadata = metaf()
