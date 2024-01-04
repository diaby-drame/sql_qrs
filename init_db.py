import io
import duckdb
import pandas as pd

con = duckdb.connect(database="data/exercises_sql_tables_duckdb", read_only=False)

# ------------------------------------
# EXERCISES LIST
# ------------------------------------
data = {
    "theme": [
        "CROSS JOIN",
        "CROSS JOIN",
        "INNER JOIN",
        "CASE WHEN",
        "GROUP BY",
        "GROUPING SETS",
        "OVER",
    ],
    "exercise_name": [
        "beverages_and_food",
        "sizes_and_trademarks",
        "orders_and_details",
        "wages_table",
        "sales_table",
        "population_table",
        "furniture_table",
    ],
    "tables": [
        ["beverages", "food_items"],
        ["sizes", "trademarks"],
        ["orders", "details"],
        ["wages"],
        ["sales"],
        ["population"],
        ["furniture"],
    ],
    "last_reviewed": [
        "1980-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
    ],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

# ------------------------------------
# CROSS JOIN
# ------------------------------------
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")


SIZES = """
size
XS
M
L
XL
"""
sizes = pd.read_csv(io.StringIO(SIZES))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

TRADEMARKS = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""
trademarks = pd.read_csv(io.StringIO(TRADEMARKS))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

# ------------------------------------
# INNER JOIN
# ------------------------------------

orders_data = {"order_id": [1, 2, 3, 4, 5], "customer_id": [101, 102, 103, 104, 105]}

df_orders = pd.DataFrame(orders_data)
con.execute("CREATE TABLE IF NOT EXISTS orders AS SELECT * FROM df_orders")

order_details_data = {
    "order_id": [1, 2, 3, 4, 5],
    "product_id": [102, 104, 101, 103, 105],
    "quantity": [2, 1, 3, 2, 1],
}

df_order_details = pd.DataFrame(order_details_data)
con.execute("CREATE TABLE IF NOT EXISTS details AS SELECT * FROM df_order_details")

# ------------------------------------
# CASE WHEN
# ------------------------------------

data = {
    "name": [
        "Toufik",
        "Jean-Nicolas",
        "Daniel",
        "Kaouter",
        "Sylvie",
        "Sebastien",
        "Diane",
        "Romain",
        "François",
        "Anna",
        "Zeinaba",
        "Gregory",
        "Karima",
        "Arthur",
        "Benjamin",
    ],
    "wage": [
        60000,
        75000,
        55000,
        80000,
        70000,
        90000,
        65000,
        72000,
        68000,
        85000,
        100000,
        120000,
        95000,
        83000,
        110000,
    ],
    "department": [
        "IT",
        "HR",
        "SALES",
        "IT",
        "IT",
        "HR",
        "SALES",
        "IT",
        "HR",
        "SALES",
        "IT",
        "IT",
        "HR",
        "SALES",
        "CEO",
    ],
}

wages = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS wages AS SELECT * FROM wages")

# ------------------------------------
# GROUP BY
# ------------------------------------

clients = ["Oussama", "Julie", "Chris", "Tom"]
sales = [120, 49, 35, 23, 19, 5.99, 20, 18.77, 39, 10, 17, 12]

sales = pd.DataFrame(sales)
sales.columns = ["montant"]
sales["client"] = clients * 3

con.execute("CREATE TABLE IF NOT EXISTS sales AS SELECT * FROM sales")

# ------------------------------------
# GROUPING SETS
# ------------------------------------

datapop = {
    "year": [2016, 2017, 2018, 2019, 2020] * 3,
    "region": (["IDF"] * 5) + (["HDF"] * 5) + (["PACA"] * 5),
    "population": [1010000, 1020000, 1030000, 1040000, 1000000]
    + [910000, 920000, 930000, 940000, 900000]
    + [810000, 820000, 830000, 840000, 950000],
}

pop = pd.DataFrame(datapop)
con.execute("CREATE TABLE IF NOT EXISTS population AS SELECT * FROM pop")

# ------------------------------------
# OVER
# ------------------------------------

furniture_data = [
    ("Chairs", "Chair 1", 5.2),
    ("Chairs", "Chair 2", 4.5),
    ("Chairs", "Chair 3", 6.8),
    ("Sofas", "Sofa 1", 25.5),
    ("Sofas", "Sofa 2", 20.3),
    ("Sofas", "Sofa 3", 30.0),
    ("Tables", "Table 1", 15.0),
    ("Tables", "Table 2", 12.5),
    ("Tables", "Table 3", 18.2),
]

# Create a pandas DataFrame from the predefined data
furniture = pd.DataFrame(furniture_data, columns=["category", "item", "weight"])
con.execute("CREATE TABLE IF NOT EXISTS furniture AS SELECT * FROM furniture")

con.close()
