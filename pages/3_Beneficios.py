import streamlit as st
import numpy as np
import pandas as pd
import av_utils as av

st.title("Cálculo de beneficios económicos")
st.header("Resumen de costos económicos: ")
if "LCOE" in st.session_state:
    st.success(st.session_state["resultado_LCOE"])
else:
    st.write("Primero simule el costo del proyecto")