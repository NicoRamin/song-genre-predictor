import pandas as pd

data_file = r'C:\Users\julia\OneDrive\Dokumente\Uni Mannheim\Erstes Semester\Data Mining I\Spotify Project\song-genre-predictor\data\spotify_data.csv'

df = pd.read_csv(data_file, index_col=[0])
#print(len(df))

# Drop exact duplicates     
df.drop_duplicates(inplace=True, keep='first')
#print(len(df))

# Find duplicates based on same track id
same_trackid = df[df.duplicated(subset='track_id', keep=False)].sort_values(by='track_id')
#print(same_trackid)

# Make dicitonary containing the genre as key and the occurence as value
genre_dict = {}
for i in df['track_genre']:
    if i in genre_dict:
        genre_dict[i] += 1
    else:
        genre_dict[i] = 1

#print(genre_dict)

# Use the dictionary to filter out the same track_id with different genre by only keeping the genre with the highest occurence
# for i in same_trackid:
#     if i == same_trackid['track_id']:
#         if genre_dict.value(same_trackid['track_genre']) < i:
#             continue
#         else:
#             df.drop(i)
for index, row in same_trackid.iterrows():
    track_id = row['track_id']
    track_genre = row['track_genre']
    
    if genre_dict.get(track_genre, 0) < genre_dict.get(track_id, 0):
        continue
    else:
        df.drop(index, inplace=True)



print(len(df))