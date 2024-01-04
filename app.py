# pylint: disable=missing-module-docstring
import logging
import os
import duckdb
import pandas as pd
import streamlit as st

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables_duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercises_sql_tables_duckdb", read_only=False)


def exercise_by_theme(user_theme, user_theme_exercise=None):
    """
    Choose the exercise according to the selected theme
    :param user_theme: user selected theme
    :param user_theme_exercise: user selected exercise by theme
    :return: the exercise and exercise name
    """

    if user_theme_exercise:
        exercise = (
            con.execute(
                f"SELECT * FROM memory_state WHERE theme = '{user_theme}' and exercise_name = '{user_theme_exercise}'"
            )
            .df()
            .sort_values("last_reviewed")
            .reset_index()
        )
        exercise_name = user_theme_exercise
    else:
        exercise = (
            con.execute(f"SELECT * FROM memory_state WHERE theme = '{user_theme}'")
            .df()
            .sort_values("last_reviewed")
            .reset_index()
        )
        exercise_name = exercise.loc[0, "exercise_name"]

    return exercise, exercise_name


def check_users_solution(user_query: str, solution: pd.DataFrame):
    """
    Checks that user SQL query is correct by:
    1: checking the columns
    2: checking the values
    :param user_query: a string containing the query inserted by the user
    :param solution: the correct data frame response
    """

    # user response
    result = con.execute(user_query).df()
    st.table(result)

    try:
        # if the user response is correct
        result = result[solution.columns]
        if result.compare(solution).shape == (0, 0):
            st.write("Bravo !")
            st.balloons()

    except KeyError:
        # if user response is not correct
        st.write("Mauvaise réponse !")
        st.info("Il manque des colonnes")
        n_lines_difference = result.shape[0] - solution.shape[0]
        if n_lines_difference != 0:
            st.info(
                f"Il y a {abs(n_lines_difference)} lignes de différence avec la solution"
            )
        exit()


st.write(
    """
# Bienvenue dans mon application !"""
)
clear = st.empty()
clear.write(
    "Veuillez choisir un thème **SQL** et un exercice que vous voulez révisez dans la barre de gauche"
)

with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "Que voulez-vous réviser ?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Sélectionnez un thème",
    )
    st.write("Vous avez choisi :", theme)

    if theme:
        exercise, exercise_name = exercise_by_theme(theme)
        theme_exercise = st.selectbox(
            "",
            exercise["exercise_name"].unique(),
            index=None,
            placeholder="Sélectionnez un exercice",
        )
        st.write("Vous avez choisi :", theme_exercise)

    if not theme:
        st.write("Vous n'avez pas encore choisi un thème")
        exit()

    elif not theme_exercise:
        st.write("Vous n'avez pas encore choisi un exercice")
        exit()

    if theme_exercise:
        exercise, _ = exercise_by_theme(theme, theme_exercise)

        st.write(exercise)
        tab2, tab3 = st.tabs(["Tables", "Solution"])
        with tab2:
            exercise_tables = exercise.loc[0, "tables"]
            for table in exercise_tables:
                st.write(f"table : {table}")
                df_table = con.execute(f"SELECT * FROM {table}").df()
                st.table(df_table)
        with open(f"answers/{theme_exercise}.sql", "r") as f:
            answer = f.read()
        solution = con.execute(answer).df()
        with tab3:
            st.text(answer)


if theme and theme_exercise:
    clear.empty()
    if st.checkbox("Consignes"):
        if theme == "CROSS JOIN":
            st.markdown(
                """
            Vous devez faire le produit cartésien des tables disponibles\n
            **Note importante**: Pour une jointure, vous devez utiliser au minimum 2 tables"""
            )

        elif theme == "INNER JOIN":
            st.markdown(
                """
            Vous devez faire une jointure interne pour rassembler les commandes avec les détails\n
            **Note importante**: Pour une jointure, vous devez utiliser au minimum 2 tables"""
            )

        elif theme == "GROUP BY":
            st.markdown(
                """
            Avec la table sales, vous devez calculer pour chaque client, la somme de ses dépenses 
            """
            )

        elif theme == "GROUPING SETS":
            st.markdown(
                """
            Avec la table population, vous devez grouper la poluation par:\n
            année, région\n
            année seulement"""
            )

        elif theme == "OVER":
            st.markdown(
                """
            Avec la table furniture, vous devez créer une nouvelle colonne qui contiendra 
            le poids total de tous les articles"""
            )

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
