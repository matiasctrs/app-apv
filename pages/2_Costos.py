import streamlit as st
import numpy as np
import pandas as pd
import av_utils as av

st.title("Cálculo de costos económicos")
#variables_excluidas = ["tmy","tmy_24","resultado","TMY", "simular","02f54165e180ca5593fb2dd5541301619d8ae709186fe25176bcc476b592d8d1",
 #                      "kWp","WACC","Capex"]

variables_incluidas = ["Latitude","Longitude","Track","Azimuth","Pv row tilt","Time zone"]
st.header("Resumen de generación fotovoltaica:")
if "resultado" in st.session_state:
    st.success(st.session_state["resultado"])
    #st.write(pd.DataFrame(st.session_state))
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
    st.dataframe(df_session_state, width = 1000)
    
else:
    st.write("Primero simule un sistema fotovoltaico")

"---"


####-----LCOE----------------------


st.header("Cálculo del costo nivelado de energía LCOE")

#st.session_state["kWp"] = st.number_input("Ingresa el tamaño de la planta (kWp)", min_value=1, value = 50)
st.session_state["Capex"] = st.number_input("Ingresa el Capex del proyecto", min_value=1,  value = 900,help = "Gastos de capital del proyecto en USD")
st.session_state["Opex"] = st.number_input("Ingresa el Opex del proyecto", min_value=1,  value = 25, help = "Gastos de operación del proyecto en USD")
st.session_state["WACC"] = st.number_input("Ingresa el WACC del proyecto", value = 0.055, format = "%.3f",help ="Costo Promedio Ponderado de Capital")


simular_lcoe = st.button("Simular LCOE", key = "Simular LCOE") 

if simular_lcoe:
    if "resultado" in st.session_state:
        st.session_state["LCOE"] = av.lcoe_calc(pv_gen=st.session_state["pv_gen"],
                                             kWp=50,
                                             capex=st.session_state["Capex"],
                                             wacc=st.session_state["WACC"],
                                             opex=st.session_state["Opex"])
        
        #float("{:.2f}".format(gen_mess))

    else: 
        st.write("Primero simule un sistema fotovoltaico")    


if "LCOE" in st.session_state:
    st.session_state["resultado_LCOE"]  = f"El LCOE del sistema simulado es: ${float('{:.2f}'.format(st.session_state['LCOE']))}\\frac{{USD}}{{kWh}}$."

    st.success(st.session_state["resultado_LCOE"])
    

