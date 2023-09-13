import streamlit as st
import numpy as np
import pandas as pd
import av_utils as av

st.title("Cálculo de beneficios económicos")
st.header("Resumen de costos económicos: ")

variables_incluidas=["Opex","Capex","WACC"]
if "LCOE" in st.session_state:
    st.success(st.session_state["resultado_LCOE"])
    def session_state_to_dataframe(session_state):
        data = {'Nombre de Variable': [], 'Valor': []}
        
        
        for variable_name, variable_value in session_state.items():
            #if isinstance(variable_value, str) and len(variable_value) < 4:
            if variable_name in variables_incluidas:
                data['Nombre de Variable'].append(variable_name)
                data['Valor'].append(variable_value)  
                
  
        df = pd.DataFrame(data)
        
        return df

    # Crear un DataFrame a partir de st.session_state
    df_session_state = session_state_to_dataframe(st.session_state)

    # Mostrar el DataFrame
    st.write(df_session_state, width = 1000)


else:
    st.write("Primero simule el costo del proyecto")