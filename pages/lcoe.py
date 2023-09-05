import streamlit as st


st.title("Calculos económicos")

if "my_input" in st.session_state:
    st.write("La generación fotovoltaica con la simulación anterior es: ",st.session_state["my_input"])
else:
    st.writw("Primero simule un sistema fotovoltaico")