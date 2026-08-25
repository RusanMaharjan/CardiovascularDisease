import streamlit as st
from models.model import logistic_Cardio_Predict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests


st.header('Cardiovascular Disease Prediction')
st.subheader('Using Logisic Regression')

# 'age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active'

# age = st.text_input('Age', placeholder='Enter your age')

features, scaler, model, Y_pred, cr, cm = logistic_Cardio_Predict()

API_URL = 'https://cardiovasculardisease.onrender.com/predict-cardio-logistic'

st.sidebar.header(
    'Cardio Features'
)

age = st.sidebar.slider(
    'Age',
    max_value = 70,
    min_value = 26,
    value = 30,
    step=1
)

# gender = st.sidebar.slider(
#     'Gender [1: Female, 2: Male]',
#     1, 2
# )

# gender = st.sidebar.selectbox(
#     'Gender',
#     options = list(gender_dict.keys()),
#     format_func = lambda x : gender_dict.get(x)
# )

gender_dict = {1: 'Female', 2: 'Male'}
gender = st.sidebar.radio(
    'Gender',
    # get key
    options = list(gender_dict.keys()),
    # get values
    format_func = lambda x : gender_dict.get(x)
)

height = st.sidebar.slider(
    'Height',
    max_value = 200,
    min_value = 136,
    value = 145,
    step=1
)

weight = st.sidebar.slider(
    'Weight',
    max_value = 120,
    min_value = 35,
    value = 60,
    step=1
)

ap_hi = st.sidebar.slider(
    'Systolic Pressure',
    max_value = 200,
    min_value = 90,
    value = 120,
    step=1
)

ap_lo = st.sidebar.slider(
    'Disystolic Pressure',
    max_value = 100,
    min_value = 50,
    value = 80,
    step=1
)

cholesterol_dict = {
    1: 'Low Cholesterol',
    2: 'Mild Cholesterol',
    3: 'High Cholesterol'
}
cholesterol = st.sidebar.selectbox(
    'Cholesterol',
    options = list(cholesterol_dict.keys()),
    format_func = lambda x : cholesterol_dict.get(x)
)

gluc_dict = {
    1: 'Low Glucose',
    2: 'Mild Glucose',
    3: 'High Glucose'
}
gluc = st.sidebar.selectbox(
    'Glucose',
    options = list(gluc_dict.keys()),
    format_func = lambda x : gluc_dict.get(x)
)

smoke_dict = {0: 'Doesnot Smoke', 1: 'Does Smoke'}
smoke = st.sidebar.selectbox(
    'Smoke',
    # get key
    options = list(smoke_dict.keys()),
    # get values
    format_func = lambda x : smoke_dict.get(x)
)

alco_dict = {0: 'Doesnot Drink Alcohol', 
             1: 'Does Drink Alcohol'}
alco = st.sidebar.selectbox(
    'Alcohol',
    # get key
    options = list(alco_dict.keys()),
    # get values
    format_func = lambda x : alco_dict.get(x)
)

active_dict = {0: 'Doesnot do PA', 
             1: 'Does do PA'}
active = st.sidebar.selectbox(
    'Physical Activities (PA)',
    # get key
    options = list(active_dict.keys()),
    # get values
    format_func = lambda x : active_dict.get(x)
)

# if st.button('Predict Cardio'):
#     # Convert User input data to Dataframe
#     input_data = pd.DataFrame([[
#         age, gender, height, weight, ap_hi, ap_lo, 
#         cholesterol, gluc, smoke, alco, active
#     ]], columns = features)
    
#     # Data scaling
#     input_scaler = scaler.transform(input_data)
    
#     # Predict using model
#     prediction = model.predict(input_scaler)[0] # 0th index
    
#     # Show Answer
#     if prediction == 0:
#         st.write('Likely not to have cardiovascular disease.')
#         st.success('No cardiovascular disease found.')
#     else: 
#         st.write('Likely to have cardiovascular disease.')
#         st.warning('Cardiovascular disease found.')


if st.button('Predict Cardio'):
    payload = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "ap_hi": ap_hi,
        "ap_lo": ap_lo,
        "cholesterol": cholesterol,
        "gluc": gluc,
        "smoke": smoke,
        "alco": alco,
        "active": active
    }
    try:
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            if result['Prediction Status'] == 0:
                st.write('Likely to be healthy.')
                st.success('No cardiovascular disease found😌.')
            else:
                st.write('Likely to be unhealthy.')
                st.warning('Cardiovascular disease found😭.')
        else:
            st.error(f'API Status Code Error: {response.status_code}')
    except requests.exceptions.RequestException as e:
        st.error(f'API Server Error: {e}')



# Visualization
st.subheader('Visualization')

fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='1.0f', xticklabels = ['Predicted Healthy [0]', 'Predicted UnHealthy[1]'],
           yticklabels = ['Actual Healthy[0]', 'Actual UnHealthy[1]'])
plt.title('Actual Cardio vs. Predicted Cardio')
st.pyplot(fig)