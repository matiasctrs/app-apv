import streamlit as st


st.title("Calculos económicos")

if "resultado" in st.session_state:
    st.success(st.session_state["resultado"])
    st.write(st.session_state["azimuth"])
    st.writw(st.session_state["pvrow_tilt"])
else:
    st.write("Primero simule un sistema fotovoltaico")