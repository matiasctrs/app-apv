import streamlit as st
import numpy as np
import pandas as pd
import importlib
import av_utils as av
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from streamlit_image_select import image_select
from folium.plugins import MousePosition
import folium
import matplotlib.pyplot as plt
from PIL import Image
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
m = folium.Map(location=[-15.087836, -44.015762], zoom_start=5)
# Agregar un control de clic en el mapa
MousePosition().add_to(m)
popup1 = folium.LatLngPopup()
m.add_child(popup1)

#agregar un marcador con la posición inicial

#marcador=folium.Marker([-15.087836, -44.015762], tooltip="Ubicación seleccionada")
#marcador.add_to(m)
if st.session_state["Latitude"] !=-15.087836 and st.session_state["Longitude"] !=-44.015762: 
    marcador = folium.Marker([st.session_state["Latitude"], st.session_state["Longitude"]], tooltip="Ubicación seleccionada")
    marcador.add_to(m)

# Mostrar el mapa en Streamlit

st_folium(m, height=500, width = 700)





# definición de variables

tz_options = ["Seleccione una opción","Brazil/East",'America/Santiago']
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


if "tmy" in st.session_state:
    st.header("TMY:")
    st.dataframe(st.session_state["tmy_24"])
#------ Simulacion de generacion electrica-----

st.subheader("Simulación eléctrica:")


#### Fotos para parametros ------------

images = ["elevado.png",
              "vertical_new.png",
              "tracking_new.png"]
images_r = []
for image in images:
    # Carga de la imagen
    image = Image.open(image)

    # Redimensiona la imagen
    width, height = image.size
    new_width = 617 # Define el nuevo ancho deseado
    new_height = 617 #int(height * (new_width / width))
    resized_image = image.resize((new_width, new_height))
    images_r.append(resized_image)

images_r.append("personalizado.png")
img = image_select(
    label = "Selecciona un diseño",
    images = images_r,
    captions=["Elevado", "Vertical","Tracking","Personalizado"],
    use_container_width=True,
    return_value="index", #index empieza de 0

)

st.session_state["Diseño"] = str(img)

#variables sensibles a diseños
tilt = 60
Track_options = [True,False]
azimut = 90
distancia_filas = 4
altura_filas = 3

if st.session_state["Diseño"] =="0":
    st.write("Has seleccionado el diseño Agrovoltaico Elevado")
    Track_options = [False,True]
    azimut = 330
    tilt = 15
    distancia_filas = 3.5
    altura_filas = 3
    


if st.session_state["Diseño"] =="1":
    st.write("Has seleccionado el diseño Agrovoltaico Vertical")
    tilt = 90
    Track_options = [False,True]
    azimut = 60
    altura_filas = 0.5
    distancia_filas = 9.3

if st.session_state["Diseño"] =="2":
    st.write("Has seleccionado el diseño Agrovoltaico con Tracking")
    tilt = 60
    Track_options = [True,False]
    azimut = 60
    altura_filas = 1.5
    distancia_filas = 11.3


#st.write(str(img)[:100])

st.session_state["Track"] = st.selectbox("Tracking",Track_options,help="True = Sistema si cuenta con seguimiento, False = Sistema no cuenta con seguimiento")
st.session_state["Azimuth"] = st.number_input("Ingresa el angulo Azimut en °", min_value=0, max_value=360, value =azimut, help =" orientación horizontal en relación con el norte geográfico, N = 0°, E = 90°")
st.session_state["Pv row tilt"] = st.number_input("Ingresa el tilt en °",min_value=0, max_value=189, value = tilt, help ="Inclinación de los módulos")

# fijos
with st.expander("Otros parámetros"):
    albedo =  st.number_input("Ingresa el valor del albedo", value=0.2)
    n_pvrows = st.number_input("Ingresa el número de filas", value=3)
    pvrow_width = st.number_input("Ingresa el ancho de las filas en metros", value=1)
    pvrow_pitch = st.number_input("Ingresa el pitch de las filas", value=distancia_filas)
    pvrow_height = st.number_input("Ingresa la altura de las filas", value=altura_filas) 
    bifaciality = st.number_input("Ingresa el factor de bifacialidad", value=0.9)



"---"


######---------función para estado de sesion y guardar variables

def get_session_state():
    return st.session_state

session_state = get_session_state()

    
            
##__________________simulacion________________--

simular = st.button("Simular")      
if 'pv_sum' not in st.session_state:
    st.session_state['pv_sum'] = 0 
if simular:
    if "tmy" in st.session_state:
        #if st.session_state["Azimuth"] and st.session_state["Pv row tilt"] !=0:

        st.session_state["pv_sum"], st.session_state["pv"] = av.pv_yield(tmy_data = st.session_state["tmy"], 
                            albedo = albedo, 
                            track = st.session_state["Track"] , 
                            pvrow_azimuth = st.session_state["Azimuth"], 
                            pvrow_tilt = st.session_state["Pv row tilt"] , 
                            n_pvrows = n_pvrows, 
                            pvrow_width = pvrow_width, 
                            pvrow_pitch = pvrow_pitch, 
                            pvrow_height = pvrow_height, 
                            bifaciality = bifaciality)

        #suma_bruta = st.session_state["pv"].sum()
        #suma_bruta = np.sum(st.session_state["pv"])
        #st.write(suma_bruta)
        gen_mess = round(st.session_state["pv_sum"]/1000,2)
        st.session_state["pv_gen"]  = float("{:.2f}".format(gen_mess))    
        ##-------GUARDA resultado EN LA SESION PARA OCUPAR EN OTRAS PAGINAS------            
        st.session_state["resultado"]  = f"La generación fotovoltaica es: ${st.session_state['pv_gen']}\\frac{{kWh}}{{kWp*year}}$."
        #st.dataframe(st.session_state["pv"])
        #st.write(st.session_state["pv_sum"])                        
    else:
        st.write("Pimero genere un TMY válido")
  

if "resultado" in st.session_state:
    st.success(st.session_state["resultado"])
    fig, ax1=plt.subplots()
    ax1.set_title("Simulated system output")
    ax1.set_ylabel("AC power")
    ax1.set_xlabel("Hour of the year")
    ax1.plot(st.session_state["pv"],label="Generated power")
    ax1.tick_params(axis='y')
    plt.legend()
    fig.tight_layout()
    st.pyplot(fig)
    