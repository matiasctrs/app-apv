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
# Define una función para mostrar información emergente cuando se hace clic en un enlace.
def show_info_popup(text):
    st.info(text)

# Crear un input de texto con un enlace para mostrar información emergente.
user_input = st.text_input("Ingrese su nombre", help="Haga clic aquí para obtener información sobre este campo.")

# Define la información que se mostrará en el popup emergente.
info_text = "Ingrese su nombre en este campo. Este es un ejemplo de cómo puede proporcionar información adicional al usuario cuando pasa el mouse sobre el ícono de información."

# Verificar si el usuario hizo clic en el enlace de información y mostrar el popup correspondiente.
if st.button("ℹ️"):
    show_info_popup(info_text)

# Otra forma es usar un enlace de texto en lugar de un botón.
# if st.text("ℹ️"):
#     show_info_popup(info_text)


#def TIR(loce,years,)