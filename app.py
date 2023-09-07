import streamlit as st
import numpy as np
import pandas as pd
import importlib
import av_utils as av
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from folium.plugins import MousePosition
import folium
import matplotlib.pyplot as plt
importlib.reload(av)



#####---------main tittle-----------------
st.set_page_config(page_title="APV data analysis")

st.title("Fotovoltaico")

st.sidebar.success("Seleccione una pagina")

#------Header section ----------

st.subheader("Rellene este formulario para simular la generación APV")

#_____BODY_________



st.session_state["Latitude"]= st.number_input("Ingresa la latitud", value = -15.087836, format = "%.6f")
st.session_state["Longitude"]= st.number_input("Ingresa la longitud", value = -44.015762, format = "%.6f")
# Crear un mapa centrado en una ubicación específica
m = folium.Map(location=[-15.087836, -44.015762], zoom_start=9)

MousePosition().add_to(m)
popup1 = folium.LatLngPopup()
m.add_child(popup1)
# Agregar un control de clic en el mapa
folium.Marker([-15.087836, -44.015762], tooltip="Ubicación seleccionada").add_to(m)

# Mostrar el mapa en Streamlit
st_folium(m, height=500, width = 700)

# definición de variables


tz_options = ["Seleccione una opción","Brazil/East"]
st.session_state["Time zone"] = st.selectbox("Ingresa la zona horaria",tz_options)

generar_tmy = st.button("Generar TMY", key = "TMY")   #
  
if generar_tmy:
    if st.session_state["Latitude"] and st.session_state["Longitude"] !=0:
        if st.session_state["Time zone"] != "Seleccione una opción":
            tmy, altitude = av.tmy_download(st.session_state["Latitude"], st.session_state["Longitude"], st.session_state["Time zone"])
            st.session_state["tmy"]  = tmy  
            st.session_state["tmy_24"]  = tmy.head(24)  
        else:
            st.write("Ingrese una zona horaria válida")

    else:
        st.write("Ingrese coordenadas válidas")


if "tmy_24" in st.session_state:
    st.header("TMY:")
    st.dataframe(st.session_state["tmy_24"])
#------ Simulacion de generacion electrica-----

st.subheader("Simulación eléctrica:")
Track_options = [True,False]
st.session_state["Track"] = st.selectbox("Tracking",Track_options)
st.session_state["Azimuth"] = st.number_input("Ingresa el angulo Azimut en °", min_value=0, max_value=360, value = 90)
st.session_state["Pv row tilt"] = st.number_input("Ingresa el tilt en °",min_value=0, max_value=189, value = 60)

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

simular = st.button("Simular", key = "simular")      

if simular:
    if "tmy" in st.session_state:
        if st.session_state["Azimuth"] and st.session_state["Pv row tilt"] !=0:
            pv = av.pv_yield(tmy_data = st.session_state["tmy"], 
                                albedo = albedo, 
                                track = st.session_state["Track"] , 
                                pvrow_azimuth = st.session_state["Azimuth"], 
                                pvrow_tilt = st.session_state["Pv row tilt"] , 
                                n_pvrows = n_pvrows, 
                                pvrow_width = pvrow_width, 
                                pvrow_pitch = pvrow_pitch, 
                                pvrow_height = pvrow_height, 
                                bifaciality = bifaciality)

            gen_mess = pv.sum()/1000
            st.session_state["pv_gen"]  = float("{:.2f}".format(gen_mess))    
            ##-------GUARDA resultado EN LA SESION PARA OCUPAR EN OTRAS PAGINAS------            
            st.session_state["resultado"]  = f"La generación fotovoltaica es: ${st.session_state['pv_gen']}\\frac{{kWh}}{{kWp*year}}$."
                                
                    
        else:
            st.write("Ingrese datos validos")
    else:
        st.write("Pimero genere un TMY válido")
  
 
if "resultado" in st.session_state:
    st.success(st.session_state["resultado"])
    fig, ax1=plt.subplots()
    ax1.set_title("30° tilt, North oriented fixed")
    ax1.set_ylabel("DC power")
    ax1.set_xlabel("month of the year")
    ax1.plot(pdc_bifi,label="Generated power")
    ax1.tick_params(axis='y')
    plt.legend()
    fig.tight_layout()
    st.pyplot(fig)