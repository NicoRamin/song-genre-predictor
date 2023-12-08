import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re


def one_hot_encode(songs_df:pd.DataFrame) -> pd.DataFrame:
    """Implement one-hot encoding for the categorical attributes.

        Categorical attributes = key, mode, time_signature

        Params:
            songs_df: dataframe obtained by reading any of the .csv files
            in the data/ folder.
        
        Returns:
            final_df: songs_df with one-hot encoded categorical attributes
    """

    categorical_col_names = ['mode', 'key', 'time_signature']
    categorical_data = songs_df[categorical_col_names]
    onehot_data = pd.get_dummies(categorical_data, columns=categorical_col_names, prefix=categorical_col_names, dtype=int)
    songs_df = songs_df.drop(columns=categorical_col_names)
    final_df = pd.concat([songs_df, onehot_data.set_axis(songs_df.index)], axis=1)
    return final_df

def add_authors_as_features(songs_df:pd.DataFrame, n_features:int) -> pd.DataFrame:
    # Replace ; for spaces in the artists column (; used to separate multiple artists in the dataset)
    df_copy = songs_df.copy()
    tmp = [artist.replace(";", " ") if artist else None for artist in df_copy['artists']]
    df_copy['artists'] = tmp
    
    # tmp = [_remove_stopwords(artist) for artist in songs_df['artists']]
    # songs_df['artists'] = tmp
    df_copy['artists'] = df_copy['artists'].apply(remove_stopwords)
    artists_vectorizer = TfidfVectorizer(max_features=n_features)
    artists_matrix = artists_vectorizer.fit_transform(df_copy['artists'])
    artists_df = pd.DataFrame(artists_matrix.toarray(), columns=artists_vectorizer.get_feature_names_out())
    df_copy.reset_index(drop=True, inplace=True)
    artists_df.reset_index(drop=True, inplace=True)
    final_df = pd.concat([df_copy, artists_df], axis=1)
    return final_df

def add_album_and_track_name_as_features(songs_df:pd.DataFrame, n_features:int) -> pd.DataFrame:
    pass

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)


def scale_data(df, scaler):
    numerical_data = df.select_dtypes(include='number')
    scaled_numerical_data = pd.DataFrame(scaler.fit_transform(numerical_data), columns=numerical_data.columns)
    return scaled_numerical_data