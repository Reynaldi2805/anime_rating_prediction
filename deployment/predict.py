import pickle
import pandas as pd
import streamlit as st

df = pd.read_csv('for_streamlit.csv')

# Load Pipeline
with open('xgb_regressor.pkl', 'rb') as file_3:
    xgb_regressor = pickle.load(file_3)

def prediction_form():

    image_path = "ANIME _ DR_STONE _ NEW WORLD EP 2.jpg"

    # Display the image
    st.image(image_path, use_column_width=True)

    # Streamlit form
    st.write("# Anime Prediction Form")
    name = st.text_input("Name")
    aired = st.text_input("Date Aired")
    status = st.selectbox("Status", df['Status'].unique())
    studios = st.selectbox("Studios", df['Studios'].unique())
    source = st.selectbox("Source", df['Source'].unique())
    rank = st.number_input("MyAnimeList Rank", format="%.0f", placeholder="Enter Rank")
    popularity = st.number_input("MyAnimeList Popularity", format="%.0f", placeholder="Enter Popularity")
    favorites = st.number_input("MyAnimeList Favorites", format="%.0f", placeholder="Enter Favorites")
    scored_by = st.number_input("Scored By (Amount of Members who scored)", format="%.0f", placeholder="Enter Scored By")
    members = st.number_input("Number of members included the anime into their watchlist", format="%.0f", placeholder="Enter Members")
    main_genre = st.selectbox("Main Genre", df['Main Genre'].unique())
    sub_genre = st.selectbox("Sub Genre", df['Sub Genre'].unique())
    year_released = st.number_input("Year Released", format="%.0f", placeholder="Enter Year Released")

    user_input = {
        'Name': [name],
        'Aired': [aired],
        'Status': [status],
        'Studios': [studios],
        'Source': [source],
        'Rank': [rank],
        'Popularity': [popularity],
        'Favorites': [favorites],
        'Scored By': [scored_by],
        'Members': [members],
        'Main Genre': [main_genre],
        'Sub Genre': [sub_genre],
        'Year Released': [year_released]
    }

    user_data = pd.DataFrame(user_input)

    # Submit button
    submit_button = st.button("Predict")

    if submit_button:
        predictions = xgb_regressor.predict(user_data)
        # Create a list of dictionaries to store the results
        results = []
        for anime, prediction in zip(user_data['Name'], predictions):
            result = {'Anime': anime, 'Predicted Score': prediction}
            results.append(result)

        # Create a DataFrame from the list of dictionaries
        results_df = pd.DataFrame(results)

        # Display the DataFrame
        st.write(results_df)
