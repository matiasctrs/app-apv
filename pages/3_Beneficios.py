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

st.header("Cálculo de la Tasa interna de retorno (TIR)", help ="Se calculará la Tasa interna de retorno como la tasa de crecimiento"+ 
          " anual que se espera que la inversión genere de por vida"+"      "+
          "-Se asume que el proyecto tiene un plazo de vida de 25 años"+"     "+
          "-Se asume un factor de degradación en los paneles, lo cual afectará a la generación electrica")


st.session_state["kWp"]= st.number_input("Tamaño de la planta en kWp",min_value = 1,value = 50, help ="Tamaño de la planta en kWp (kilo Watts peak)")
st.session_state["Precio"]= st.number_input("Precio de venta del kilo Watt",min_value = 0.00001,value = 0.085, format = '%.4f',help ="Precio al que se vende cada kilowatt hora en USD, asumiendo que la energía generada se inyecta a la red")

simular_tir = st.button("Simular TIR", key = "Simular TIR")

if simular_tir:
    if "LCOE" in st.session_state:
        st.session_state["TIR"], st.session_state["Flujos"] = av.tir(opex = st.session_state["Opex"],
                                                                    capex = st.session_state["Capex"],
                                                                    pv_gen = st.session_state["pv_gen"],
                                                                    kWp= st.session_state["kWp"],
                                                                    price =st.session_state["Precio"])
        st.session_state["resultado_TIR"]  = f"La Tasa interna de retorno del sistema simulado es: % ${float('{:.2f}'.format(st.session_state['TIR']*100))}$."

        


    else:
        st.write("Primero simule el costo del proyecto")


if "TIR" in st.session_state:
    st.success(st.session_state["resultado_TIR"])
    st.write("Los flujos de caja en USD, asociados a los 25 periodos del proyecto son:")
    st.dataframe(st.session_state["Flujos"])


