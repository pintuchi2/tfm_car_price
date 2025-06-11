import streamlit as st
import numpy as np
import pandas as pd
import datetime
import xgboost as xgb
import pickle
from PIL import Image
import sklearn
from scipy.special import inv_boxcox


# Para lanzar la web en local ejecutar el comando: "streamlit run streamlit_app.py". Después se actualiza en la web en un botón cada vez que guardamos el .py

# Función para cargar modelos y datos
def cargar_modelos_datos():
    loaded_model = pickle.load(open("./streamlit/utils/modelo_final.pkl", 'rb'))
    marca_model_set = pickle.load(open("./streamlit/utils/marca_modelo_set.pkl", 'rb'))
    encoder_marca = pickle.load(open("./streamlit/utils/label_encoder_marca.pkl", 'rb'))
    encoder_model = pickle.load(open("./streamlit/utils/label_encoder_modelo.pkl", 'rb'))
    scaler = pickle.load(open("./streamlit/utils/scaler.pkl", 'rb'))

    return loaded_model, marca_model_set, encoder_marca, encoder_model, scaler

# Función principal para la calculadora de precios
def calculadora_precios():

    lambda_box = 0.2805938549051249

    marca = st.selectbox('Marca del coche:', sorted(list(marca_model_set.keys())))
    modelo = st.selectbox('Modelo del coche:', sorted([m for m in marca_model_set[marca]]))

    combustible = st.radio('Combustible:', options=['Diésel', 'Gasolina', 'Híbrido', 'Eléctrico', 'Híbrido Enchufable', 'Gas licuado (GLP)', 'Gas natural (CNG)'], 
          horizontal=True)
    anyo_vehiculo = st.number_input('Año de primera matriculación:', 2015, date_time.year,  step=1)
    kilometraje = st.number_input('Número de kilómetros:', 0, 500000, step=1000)
    potencia = st.number_input('Potencia (CV):', 90, 500, step=10)
    num_puertas = st.selectbox('Nº de puertas (incluyendo maletero)', (3, 5))
    tipo_cambio = st.selectbox('Tipo de cambio:', ('Manual', 'Automático'))

    data_new = pd.DataFrame({
        'marca': marca,
        'modelo': modelo,
        'combustible': combustible,
        'anyo_vehiculo': anyo_vehiculo,
        'kilometraje': kilometraje,
        'potencia': potencia,
        'num_puertas': num_puertas,
        'tipo_cambio': tipo_cambio,
    }, index=[0])

    
    # Aplicar las transformaciones a data_new

    data_new["marca"] = encoder_marca.transform(data_new["marca"])
    data_new["modelo"] = encoder_model.transform(data_new["modelo"])

    
    fuel_types = {"Diésel" : 0,
            "Gasolina" : 1,
            "Híbrido" : 2,
            "Eléctrico" : 3,
            "Híbrido Enchufable" : 4, 
            "Gas licuado (GLP)" : 5,
            "Gas natural (CNG)" : 6}
                        
    data_new["combustible"] = data_new["combustible"].map(fuel_types)
    print(data_new["combustible"])

    num_puertas = {5: 5,
            4 : 5,
            3 : 3,
            2 : 3}

    data_new["num_puertas"] = data_new["num_puertas"].map(num_puertas)

    data_new["tipo_cambio"] = data_new["tipo_cambio"].apply(lambda x: 0 if x == "Manual" else 1)

    data_new["marca"] = data_new["marca"].astype("int")
    data_new["modelo"] = data_new["modelo"].astype("int")
    data_new["combustible"] = data_new["combustible"].astype("int")
    data_new["anyo_vehiculo"] = data_new["anyo_vehiculo"].astype("float")
    data_new["kilometraje"] = data_new["kilometraje"].astype("float")
    data_new["potencia"] = data_new["potencia"].astype("float")
    data_new["num_puertas"] = data_new["num_puertas"].astype("int")
    data_new["tipo_cambio"] = data_new["tipo_cambio"].astype("int")

    # Realizar la predicción

    try: 
        if st.button('Predecir precio'):
            data_new = scaler.transform(data_new)
            prediction = loaded_model.predict(data_new)
            if prediction>0:
                st.balloons()
                # st.snow()
                # prediction = np.exp(prediction)
                prediction = inv_boxcox(prediction, lambda_box)
                st.success(f'El precio estimado del coche es de {round(prediction[0])} euros.')
            else:
                st.warning("No puedes vender este coche.")
    except:
        st.warning("Ups!! Algo ha salido mal.\nPrueba de nuevo.")


# Streamlit app
date_time = datetime.datetime.now()

st.set_page_config(
    page_title="App predicción precios",
    page_icon=":car:",
    layout="wide",
    initial_sidebar_state="expanded",
)

image_path = Image.open("./streamlit/utils/autos_pintos_logo_red.png")
st.image(image_path, width=300)

st.header("Bienvenid@ a la App de predicción de precios de vehículos")

st.subheader("Introduce las características del coche para predecir su precio:")



loaded_model, marca_model_set, encoder_marca, encoder_model, scaler = cargar_modelos_datos()
calculadora_precios()  # Llamada a la función


