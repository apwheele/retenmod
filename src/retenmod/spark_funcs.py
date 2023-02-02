"""
This is an illustrative
function to show off
generating SQL

this works for spark
unfortunately the explode
query changes across databases
(but a similar logic would work)
"""

# Create discrete time table
# Just generates the SQL text


def discrete_time(table, vars, begin, end, fail, max_time=60, interval=1):
    """
    table - string table name
    vars - list of strings to include in final exploded table
    begin - string of begin date
    end - string of end date (may be censored or failure)
    fail - string for failure, presumes 0/1
    max_time - integer for days for max time (default 60)
    interval - integer for interval, default 1 day, but can use say 7 days
               for weekly, 30 days for approx monthly, etc.

    returns SQL string to submit to spark object
    """
    # inner subquery table to calculate events
    v_sql = ",\n".join(vars)
    sub_query = f"SELECT {begin},"
    sub_query += f"\n{end},\n{fail},\n"
    sub_query += v_sql
    sub_query += f",\nCASE WHEN datediff({end},{begin}) + 1 > {max_time}"
    sub_query += f"\nTHEN {max_time} ELSE datediff({end},{begin}) + 1 END AS end_time"
    sub_query += f"\nFROM {table}"
    # Now for the outer explode query
    query = f"SELECT \n{begin}, \n{end}, \n{v_sql}"
    query += f",\ndate_add({begin},t) AS tdate"
    query += ",\nEXPLODE(SEQUENCE(1,end_time)) AS t"
    query += f",\nCASE WHEN {fail} = 1 AND t = datediff({end},{begin}) + 1"
    query += " THEN 1 ELSE 0 END AS fail"
    query += f"\nFROM ({sub_query}) s"
    return query
