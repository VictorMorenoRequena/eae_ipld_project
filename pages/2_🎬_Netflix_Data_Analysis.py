# The libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries to build the webapp
import streamlit as st


# ----- Page configs -----
st.set_page_config(
    page_title="<Your Name> Portfolio",
    page_icon="📊",
)


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about Netflix Movies and Series, extract some insights usign Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/shivamb/netflix-shows (with some cleaning and modifications)")


# ----- Title of the page -----
st.title("🎬 Netflix Data Analysis")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "data/netflix_titles.csv"

    movies_df = pd.read_csv(data_path, index_col='show_id')  # TODO: Ex 2.1: Load the dataset using Pandas, use the data_path variable and set the index column to "show_id"
    return movies_df
import pandas as pd
import matplotlib.pyplot as plt
       # a Pandas DataFrame


movies_df = load_data()

# Displaying the dataset in a expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(movies_df)


# ----- Extracting some basic information from the dataset -----

# TODO: Ex 2.2: What is the min and max release years?
min_year = movies_df['release_year'].min()
max_year = movies_df['release_year'].max()

# TODO: Ex 2.3: How many director names are missing values (NaN)?
num_missing_directors = movies_df['director'].isna().sum()
# TODO: Ex 2.4: How many different countries are there in the data?

all_countries = [country.strip() for countries in movies_df['country'].dropna() for country in countries.split(',')]
unique_countries = set(all_countries)
n_countries = len(unique_countries)


def extract_duration_minutes(duration):
    try:
        # Extract numeric part from the string (e.g., '90 min' -> 90)
        return int(''.join(filter(str.isdigit, str(duration))))
    except ValueError:
        return None

# Apply the function to create a new 'duration_minutes' column
movies_df['duration_minutes'] = movies_df['duration'].apply(extract_duration_minutes)

# Calculate the average duration in minutes






# TODO: Ex 2.5: How many characters long are on average the title names?
avg_title_length = movies_df['duration_minutes'].mean()

st.write("Avg Title Length:", str(round(avg_title_length, 2)) if avg_title_length is not None else None)

# ----- Displaying the extracted information metrics -----

st.write("##")
st.header("Basic Information")

cols1 = st.columns(5)
cols1[0].metric("Min Release Year", min_year)
cols1[1].metric("Max Release Year", max_year)
cols1[2].metric("Missing Dir. Names", num_missing_directors)
cols1[3].metric("Countries", n_countries)
cols1[4].metric("Avg Title Length", str(round(avg_title_length, 2)) if avg_title_length is not None else None)


# ----- Pie Chart: Top year producer countries -----

st.write("##")
st.header("Top Year Producer Countries")

cols2 = st.columns(2)
year = cols2[0].number_input("Select a year:", min_year, max_year, 2005)

# TODO: Ex 2.6: For a given year, get the Pandas Series of how many movies and series 
# combined were made by every country, limit it to the top 10 countries.
data_for_year = movies_df.loc[movies_df['release_year'] == year]
combined_ = data_for_year['country'].value_counts()
top_10_countries = combined_.head(10)

# print(top_10_countries)
if top_10_countries is not None:
    fig = plt.figure(figsize=(8, 8))
    plt.pie(top_10_countries, labels=top_10_countries.index, autopct="%.2f%%")
    plt.title(f"Top 10 Countries in {year}")

    st.pyplot(fig)

else:
    st.subheader("⚠️ You still need to develop the Ex 2.6.")


# ----- Line Chart: Avg duration of movies by year -----

st.write("##")
st.header("Avg Duration of Movies by Year")

# TODO: Ex 2.7: Make a line chart of the average duration of movies (not TV shows) in minutes for every year across all the years.
movies_avg_duration_per_year = movies_df.loc[movies_df['type'] == 'Movie'].groupby('release_year')['duration_minutes'].mean()

if movies_avg_duration_per_year is not None:
    fig = plt.figure(figsize=(9, 6))

    plt.plot(movies_avg_duration_per_year.index, movies_avg_duration_per_year, marker='o', linestyle='-')  # Add this line

    plt.title("Average Duration of Movies Across Years")
    plt.xlabel("Year")
    plt.ylabel("Average Duration (minutes)")

    st.pyplot(fig)

else:
    st.subheader("⚠️ You still need to develop the Ex 2.7.")