import streamlit as st
import numpy as np
import pandas as pd
#import pvlib
import importlib
#import datetime
#import pytz
import av_utils as av
importlib.reload(av)

st.set_page_config(page_title="APV data analysis")

st.title("Fotovoltaico")
st.sidebar.success("Seleccione una pagina")

#------Header section ----------

st.subheader("Rellene este formulario para simular la generación APV")

#_____BODY_________

latitude= st.number_input("Ingresa la latitud", value = -15.087836, format = "%.6f")
longitude= st.number_input("Ingresa la longitud", value = -44.015762, format = "%.6f")
tz_options = ["Seleccione una opción","Brazil/East"]
tz = st.selectbox("Ingresa la zona horaria",tz_options)

generar_tmy = st.button("Generar TMY", key = "TMY")   

#------ Simulacion de generacion electrica-----

st.subheader("Simulación eléctrica:")
track_options = [True,False]
track = st.selectbox("Tracking",track_options)
#pvrow_azimuth = st.number_input("Ingresa el angulo Azimut en °", min_value=0, max_value=360, value = 90)
st.session_state["azimuth"] = st.number_input("Ingresa el angulo Azimut en °", min_value=0, max_value=360, value = 90)
#pvrow_tilt = st.number_input("Ingresa el tilt en °",min_value=0, max_value=189, value = 60)
st.session_state["pvrow_tilt"] = st.number_input("Ingresa el tilt en °",min_value=0, max_value=189, value = 60)

# fijos
with st.expander("Otros parámetros"):
    albedo =  st.number_input("Ingresa el valor del albedo", value=0.2)
    n_pvrows = st.number_input("Ingresa el número de filas", value=3)
    pvrow_width = st.number_input("Ingresa el ancho de las filas en metros", value=1)
    pvrow_pitch = st.number_input("Ingresa el pitch de las filas", value=4)
    pvrow_height = st.number_input("Ingresa la altura de las filas", value=3) 
    bifaciality = st.number_input("Ingresa el factor de bifacialidad", value=0.9)

"---"


######---------función para estado de sesion y guardar variables

def get_session_state():
    return st.session_state

session_state = get_session_state()

    
            
##__________________simulacion________________--

# PV simulation (pvlib viewfactors)

simular = st.button("Simular", key = "simular")          

if generar_tmy:
    if latitude and longitude !=0:
        if tz != "Seleccione una opción":
            tmy, altitude = av.tmy_download(latitude, longitude, tz)
            st.session_state["tmy"]  = tmy  
            st.session_state["tmy_24"]  = tmy.head(24)  
        else:
            st.write("Ingrese una zona horaria válida")

    else:
        st.write("Ingrese coordenadas válidas")

if simular:
    if latitude and longitude !=0:
        if tz != "Seleccione una opción":

            if "tmy" in st.session_state:

            
                if st.session_state["azimuth"] and st.session_state["pvrow_tilt"] !=0:
                    pv = av.pv_yield(tmy_data = st.session_state["tmy"], 
                                albedo = albedo, 
                                track = track, 
                                pvrow_azimuth = st.session_state["azimuth"], 
                                pvrow_tilt = st.session_state["pvrow_tilt"] , 
                                n_pvrows = n_pvrows, 
                                pvrow_width = pvrow_width, 
                                pvrow_pitch = pvrow_pitch, 
                                pvrow_height = pvrow_height, 
                                bifaciality = bifaciality)

                    gen_mess = pv.sum()/1000
                    gen_mess = float("{:.2f}".format(gen_mess))    
                    ##-------GUARDA resultado EN LA SESION PARA OCUPAR EN OTRAS PAGINAS------            
                    st.session_state["resultado"]  = f"La generación fotovoltaica es: ${gen_mess}\\frac{{kWh}}{{kWp*year}}$."
                                
                    
                else:
                    st.write("Ingrese datos validos")
            else:
                st.write("Pimero genere un TMY")
        else:
            st.write("Ingrese una zona horaria válida")
    else:
        st.write("Ingrese coordenadas válidas")
   
 
if "tmy_24" in st.session_state:
    st.header("TMY:")
    st.dataframe(st.session_state["tmy_24"])


if "resultado" in st.session_state:
    st.success(st.session_state["resultado"])









    
#----CONTACT----

with st.container():
    st.write("---")
    st.header("Contactate con nosotros")
    st.write("##")

    contact_form= """
    <form action="https://formsubmit.co/david.jung@fraunhofer.cl" method="POST">
        <input type="hidden" name="_captcha" value = "false">
        <input type="text" name="name" placeholder ="Tu nombre" required>
        <input type="email" name="email" placeholder = "Tu email" required>
        <textarea name= "message" placeholder = "Tu mensaje aqui" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
left_column, right_column = st.columns(2)
with left_column:
    st.markdown(contact_form, unsafe_allow_html=True)
with right_column:
    st.empty()

#Use local css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<style>",unsafe_allow_html=True)

local_css("style.css")
