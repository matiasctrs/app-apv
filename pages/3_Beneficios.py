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


"---"

st.header("Cálculo de la Tasa interna de retorno (TIR)")


#st.session_state["kWp"]= 50 #st.number_input("kWp",min_value = 1,value = 50, help ="Tamaño de la planta en kWp (kilo Watts peak)")

simular_tir = st.button("Simular TIR", key = "Simular TIR")

if simular_tir:
    st.session_state["TIR"], st.session_state["Flujos"] = av.tir(opex = st.session_state["Opex"],
                                     capex = st.session_state["Capex"],
                                     pv_gen = st.session_state["pv_gen"])
    st.session_state["resultado_TIR"]  = f"La Tasa interna de retorno del sistema simulado es: % ${float('{:.2f}'.format(st.session_state['TIR']*100))}$."

    st.success(st.session_state["resultado_TIR"])
    st.write("Los flujos de caja en USD, asociados a los 25 periodos del proyecto son:")
    st.dataframe(st.session_state["Flujos"])
