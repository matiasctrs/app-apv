import streamlit as st


st.title("Cálculos económicos")

if "resultado" in st.session_state:
    st.success(st.session_state["resultado"])
    st.write(pd.DataFrame(st.session_state))
else:
    st.write("Primero simule un sistema fotovoltaico")