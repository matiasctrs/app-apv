import streamlit as st
import numpy as np
import pandas as pd

st.title("Cálculos económicos")
variables_excluidas = ["tmy","tmy_24","resultado"]



if "resultado" in st.session_state:
    st.success(st.session_state["resultado"])
    #st.write(pd.DataFrame(st.session_state))
    def session_state_to_dataframe(session_state):
        data = {'Nombre de Variable': [], 'Valor': []}
        
        
        for variable_name, variable_value in session_state.items():
            #if isinstance(variable_value, str) and len(variable_value) < 4:
            if variable_name not in variables_excluidas:
                data['Nombre de Variable'].append(variable_name)
                data['Valor'].append(variable_value)  
                
  
        df = pd.DataFrame(data)
        
        return df

    # Crear un DataFrame a partir de st.session_state
    df_session_state = session_state_to_dataframe(st.session_state)

    # Mostrar el DataFrame
    st.write(df_session_state)
    
else:
    st.write("Primero simule un sistema fotovoltaico")