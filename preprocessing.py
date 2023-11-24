import pandas as pd

data_file = r'C:\Users\julia\OneDrive\Dokumente\Uni Mannheim\Erstes Semester\Data Mining I\Spotify Project\song-genre-predictor\data\spotify_data.csv'

df = pd.read_csv(data_file, index_col=[0])
print(len(df))

# Drop exact duplicates     
df.drop_duplicates(inplace=True, keep='first')
print(len(df))

# Find duplicates based on same track id
same_trackid = df[df.duplicated(subset='track_id', keep=False)].sort_values(by='track_id')
print(same_trackid)

