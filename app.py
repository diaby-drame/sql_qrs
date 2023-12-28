# pylint: disable=missing-module-docstring
import logging
import os
import duckdb
import streamlit as st

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables_duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercises_sql_tables_duckdb", read_only=False)

st.write(
    """
# SQL SRS
Pratiquer le SQL"""
)

#con = duckdb.connect(database="data/exercises_sql_tables_duckdb", read_only=False)

with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "Que voulez vous reviser",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Selectionnez un thème",
    )
    st.write("Vous avez choisi", theme)

    if not theme:
        st.write("Vous n'avez pas encore choisi un thème")
        exit()

    exercise = (
        con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
        .df()
        .sort_values("last_reviewed")
        .reset_index()
    )
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution = con.execute(answer).df()


st.header("entrez votre code:")
query = st.text_area(label="votre code SQL ici", key="user_input")
if query:
    result = con.execute(query).df()
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
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"tables : {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("résultat attendu:")
#     st.dataframe(solution)
#
with tab3:
    st.text(answer)
