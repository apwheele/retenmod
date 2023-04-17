"""
Example testing
spark query
"""

import pandas as pd
import retenmod

# Creating fake dataframe to test spark on
x = [1, 2, 3, 4]
y = ["a", "b", "c", "c"]
test_table = pd.DataFrame(zip(x, y), columns=["x", "y"])

# sql to test
# note this can be a function or grab
# from a file
query = """
SELECT
  SUM(x) AS cum_x,
  COUNT(y) AS n,
  y
FROM test_table
GROUP BY y"""


# Creating datetime/end failure to test
# discrete time for

beg_date = ["1/1/2020", "1/2/2020", "1/3/2020", "1/5/2020"]
end_date = ["1/3/2020", "1/6/2020", "1/3/2020", "1/15/2020"]
test_table["beg_date"] = pd.to_datetime(beg_date, utc=True)
test_table["end_date"] = pd.to_datetime(end_date, utc=True)
test_table["fail"] = [0, 1, 0, 1]


######################################################
# Test 1 for SQL above


def test_sql(spark):
    # Create the temporary table
    # in session
    sdf = spark.createDataFrame(test_table)
    sdf.createOrReplaceTempView("test_table")
    # Test out our sql query
    res = spark.sql(query).toPandas()
    # No guarantees on row order in this result
    # so I sort pandas dataframe to make 100% sure
    res.sort_values(by="y", inplace=True, ignore_index=True)
    # Then I do tests
    # Type like tests, shape and column names
    assert res.shape == (3, 3)
    assert list(res) == ["cum_x", "n", "y"]
    # Mathy type tests
    dif_x = res["cum_x"] != [1, 2, 7]
    assert dif_x.sum() == 0
    dif_n = res["n"] != [1, 1, 2]
    assert dif_n.sum() == 0


######################################################


######################################################
# Test 2 for retenmod function for discrete time


def test_discrete(spark):
    # Note that test_sql runs first,
    # so do not need to re init the temp
    # spark dataframes!
    res = retenmod.discrete_time(
        table="test_table",
        vars=["x", "y"],
        begin="beg_date",
        end="end_date",
        fail="fail",
        max_time=7,
    )
    spark_dt = spark.sql(res)
    dt = spark_dt.toPandas()
    dt.sort_values(by=[], inplace=True, ignore_index=True)
    # Should only have 1 failure, and max time of 7 here
    assert dt["t"].max() == 7
    assert dt["fail"].sum() == 1


######################################################
