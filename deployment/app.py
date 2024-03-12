import streamlit as st
import predict
import eda

st.title("Welcome to my Anime Prediction App")

# Assuming you have an image file named "example_image.jpg" in the same directory as your script
image_path = "𝘩𝘪𝘴𝘶𝘪 𝘩𝘦𝘢𝘥𝘦𝘳𝘴 • 𝘵𝘦𝘯𝘴𝘶𝘳𝘢.jpg"
# Display the image
st.image(image_path, use_column_width=True)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.subheader("Please Choose the menu you would like to see!")
# Main tab selection dropdown
nav = st.selectbox('Choose Menu:', ('Main Interface','EDA', 'Anime Score Prediction'))

# Display content based on selection
if nav == 'Anime Score Prediction':
    predict.prediction_form()
elif nav == 'EDA':
    eda.graph()
else:
    st.subheader("This is the main Interface! You can select which menu you would like to see from the navigation bar ^.^")
