import streamlit as st


st.title("Calculos económicos")

if "my_input" in st.session_state:
    st.success(st.session_state["my_input"])
else:
    st.write("Primero simule un sistema fotovoltaico")