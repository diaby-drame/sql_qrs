import streamlit as st
import pandas as pd
import duckdb

st.write("Welcome")
data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    query = st.text_area("entrez votre input")
    st.write(f"Vous avez entré la query suivante : {query}")
    result = duckdb.sql(query).df()
    st.dataframe(result)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with tab2:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")
