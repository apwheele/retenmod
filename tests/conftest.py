"""
Setting up a spark fixture
for all of the tests

pytest --disable-warnings ./tests

Note this is just for illustration
to show off for spark, see blog
post ??????

Andy Wheeler
"""

import pytest
from pyspark.sql import SparkSession


# This sets the spark object for the entire session
@pytest.fixture(scope="session")
def spark():
    sp = SparkSession.builder.getOrCreate()
    # Then can do other stuff to set
    # the spark object
    sp.sparkContext.setLogLevel("ERROR")
    sp.conf.set("spark.sql.execution.array.pyspark.enabled", "true")
    return sp
