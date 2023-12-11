# pylint: disable=missing-module-docstring

import io
import duckdb
import pandas as pd
import streamlit as st

st.write(
    """
# SQL SRS
Pratiquer le SQL"""
)

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = duckdb.sql(ANSWER).df()

with st.sidebar:
    option = st.selectbox(
        "Que voulez vous reviser",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Selectionnez un thème",
    )
    st.write("Vous avez choisi", option)

st.header("entrez votre code:")
query = st.text_area(label="votre code SQL ici", key="user_input")
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

    try:
        result = result[solution.columns]
        st.dataframe(result.compare(solution))
    except KeyError as e:
        st.write("Il manque des colonnes")

    n_lines_difference = result.shape[0] - solution.shape[0]
    if n_lines_difference != 0:
        st.write(f"Il y a {n_lines_difference} lignes de différence avec la solution")

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("résultat attendu:")
    st.dataframe(solution)

with tab3:
    st.write(ANSWER)
