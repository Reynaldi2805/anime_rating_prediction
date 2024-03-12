import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import calendar


df = pd.read_csv('anime-dataset-2023.csv')

# Create a dictionary to store the counts
value_counts = {'NaN': 0, 'null': 0, 'UNKNOWN': 0, 'unknown' : 0}

# Check for NaN, null, and 'Unknown' values in all columns
for column in df.columns:
    nan_values_1 = df[df[column].isna()]
    value_counts['NaN'] += nan_values_1.shape[0]

    null_values = df[df[column].isnull()]
    value_counts['null'] += null_values.shape[0]

    unknown_values = df[df[column] == 'UNKNOWN']
    value_counts['UNKNOWN'] += unknown_values.shape[0]
    
    nan_values = df[df[column] == 'nan']
    value_counts['unknown'] += nan_values.shape[0]

# Calculate the total count of missing values
total_missing_count = sum(value_counts.values())

# Calculate the percentage of missing values relative to the total data
percentage_missing = (total_missing_count / df.size) * 100

### change all nan null unknown to missing values

missing_value_placeholder = 'YOW MISSING MAS BRO'

# Replace NaN, null, and 'Unknown' values with the common placeholder
df.fillna(missing_value_placeholder, inplace=True)
df.replace(['UNKNOWN', 'null', 'nan'], missing_value_placeholder, inplace=True)

missing_rows_count = (df == 'YOW MISSING MAS BRO').any(axis=1).sum()

# Calculate the percentage of rows with 'YOW MISSING MAS BRO' values relative to the total rows
percentage_missing_rows = (missing_rows_count / df.shape[0]) * 100

df.drop(['anime_id', 'Duration', 'Synopsis', 'Licensors', 'Premiered', 'English name', 'Producers', 'Rating', 'Episodes', 'Other name', 'Type', 'Image URL'], axis=1, inplace=True)

df_eda = df.copy()

# Split the 'Genres' column on commas and expand it into separate columns
genres_df = df_eda['Genres'].str.split(', ', expand=True)

# Rename the columns to Main Genre, Sub-genre1, Sub-genre2, etc.
genres_df.columns = [f'Main Genre' if i == 0 else f'Sub-genre{i}' for i in range(genres_df.shape[1])]

# Concatenate the genres DataFrame with the original DataFrame
normalized_df = pd.concat([df_eda, genres_df], axis=1)

# Drop the original 'Genres' column
normalized_df.drop(columns=['Genres'], inplace=True)
normalized_df.fillna("No Sub-Genre",inplace=True)
normalized_df

# Define the list of inappropriate genres
inappropriate_genres = ['YOW MISSING MAS BRO', 'Hentai', 'Boys Love', 'Ecchi', 'Girls Love', 'Erotica']
# Drop rows containing inappropriate genres
filtered_df = normalized_df[~normalized_df['Main Genre'].str.contains('|'.join(inappropriate_genres))]
# Display the value counts after filtering
filtered_df['Main Genre'].value_counts()

filtered_df['Score'] = filtered_df['Score'].replace('YOW MISSING MAS BRO', 0.0)
filtered_df['Scored By'] = filtered_df['Scored By'].replace('YOW MISSING MAS BRO', 0.0)

filtered_df.tail()

filtered_df['Score'] = filtered_df['Score'].astype(float)
filtered_df['Scored By'] = filtered_df['Scored By'].astype(float)

filtered_df.info()

grade = []

for score in filtered_df['Score']:
    if score == 0:
        grade.append("Not rated yet")
    elif score >= 8.0:
        grade.append("Highly Rated")
    elif 7.0 <= score < 8.0:
        grade.append("Well Received")
    elif 6.0 <= score < 7.0:
        grade.append("Average")
    else:
        grade.append("Poorly Rated")


score_df = pd.DataFrame({
    'Anime Score': filtered_df['Score'],
    'Score Group' : grade
})

score_df

# Parse the 'Aired' column to extract the release year and month
filtered_df['Year Released'] = filtered_df['Aired'].apply(lambda x: pd.to_datetime(x.split(' to ')[0], errors='coerce').year 
                                        if 'to' in x else pd.to_datetime(x, format='%b %Y', errors='coerce').year)
filtered_df['Month Released'] = filtered_df['Aired'].apply(lambda x: pd.to_datetime(x.split(' to ')[0], errors='coerce').month 
                                        if 'to' in x else pd.to_datetime(x, format='%b %Y', errors='coerce').month)

filtered_df

genre_frequency = {
    'Comedy': 1,
    'Action': 2,
    'Adventure': 3,
    'Fantasy': 4,
    'Drama': 5,
    'Avant Garde': 6,
    'Slice of Life': 7,
    'Sci-Fi': 8,
    'Sports': 9,
    'Romance': 10,
    'Horror': 11,
    'Mystery': 12,
    'Supernatural': 13,
    'Award Winning': 14,
    'Gourmet': 15,
    'Suspense': 16
}

# Apply ordinal encoding to the 'Genres' column
encoded_df = filtered_df.copy()  # Create a copy of the original DataFrame to avoid modifying it directly
encoded_df['Main Genre'] = encoded_df['Main Genre'].replace(genre_frequency)


def plot1():
  st.title('Anime Genre Frequency Counts')
   # Count the occurrences of each main genre
  genre_counts = filtered_df['Main Genre'].value_counts()

  # Create a bar plot
  plt.figure(figsize=(10, 6))
  plt.bar_plot = genre_counts.plot(kind='bar', color='skyblue')
  plt.title('Anime Genre Counts')
  plt.xlabel('Genre')
  plt.ylabel('Count')
  plt.xticks(rotation=45, ha='right')

  # Add labels to the bars
  for i, v in enumerate(genre_counts):
      plt.text(i, v + 0.1, str(v), ha='center', va='bottom')

  plt.tight_layout()
  st.pyplot()

def plot2():
    st.title('Distribution Of Anime Ratings')
    satisfaction_count = score_df['Score Group'].value_counts()

    # Filter out the "Not rated yet" category
    satisfaction_count_filtered = satisfaction_count[~satisfaction_count.index.str.contains('Not rated yet')]

    # Generate a color palette for the remaining categories
    color_palette = sns.color_palette("Blues_r", len(satisfaction_count_filtered))

    # Plot the pie chart with filtered data
    plt.figure(figsize=(5, 5))
    plt.pie(satisfaction_count_filtered, labels=satisfaction_count_filtered.index, autopct='%1.1f%%', startangle=140, colors=color_palette)
    plt.title('Distribution of Anime Ratings', pad=20)
    plt.axis('equal')
    st.pyplot()

def plot3():
    st.title("Correlation of Anime Scores with Number of Members")
        # Filter out data points with score of 0 or 0 members
    filtered_scores = filtered_df[(filtered_df['Score'] != 0) & (filtered_df['Members'] != 0)]['Score']
    filtered_members = filtered_df[(filtered_df['Score'] != 0) & (filtered_df['Members'] != 0)]['Members']

    # Create a scatter plot with filtered data
    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_scores, filtered_members, color='blue', alpha=0.5)
    plt.title('Anime Scores vs. Number of Members')
    plt.xlabel('Score')
    plt.ylabel('Members')
    plt.grid(True)
    st.pyplot()

def plot4():

    st.title("Average Anime Scores per Month in 2020")
    # Filter out entries with unknown release years
    new_df = filtered_df[filtered_df['Year Released'].notna()]
    # Filter out entries with release years outside the range from 2022 to 2022
    new_df = new_df[(new_df['Year Released'] >= 2020) & (new_df['Year Released'] <= 2020)]

    # Group the DataFrame by month and calculate the average score for each month
    monthly_avg_score = new_df.groupby('Month Released')['Score'].mean()
    # Create a horizontal bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(monthly_avg_score.index, monthly_avg_score.values, color='skyblue')
    plt.title('Average Anime Score by Month in 2020')
    plt.xlabel('Average Score')
    plt.ylabel('Month Released')
    plt.yticks(range(1, 13), [calendar.month_abbr[i] for i in range(1, 13)])
    plt.grid(axis='x')
    st.pyplot()


def plot5():
    st.title("Heatmap Correlation for Numerical Columns")
    numeric_df = encoded_df.select_dtypes(include=['float64', 'int64'])
    # Calculate the correlation matrix using Kendall's tau
    correlation_matrix = numeric_df.corr(method='kendall')

    # Plot heatmap using Seaborn
    plt.figure(figsize=(6, 4))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', square=True)
    plt.title("Kendall's Tau Correlation Heatmap")
    st.pyplot()


def graph():
    st.title('Exploratory Data Analysis')
    image_path = "De hecho.jpg"
    # Display the image
    st.image(image_path, use_column_width=True)
    st.write("The dataset:")
    st.write(filtered_df.iloc[:, :5])
    st.write("Data Source:")
    st.write("https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset")
    plot1()
    plot2()
    plot3()
    plot4()
    plot5()