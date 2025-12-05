# build_recs.py
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

print("Loading Data...")
# Ensure AppID is treated as int
df = pd.read_csv('cleaned_games.csv', index_col=False)

# --- CLEANING STEP ---
# 1. Fill NaNs so we don't crash on empty cells
df['Genres'] = df['Genres'].fillna('')
df['Tags'] = df['Tags'].fillna('')

# 2. Replace commas with spaces
# This turns "Action, Adventure, RPG" -> "Action  Adventure  RPG"
clean_pattern = r'[,\\[\\]]' 

df['Genres'] = df['Genres'].astype(str).str.replace(clean_pattern, ' ', regex=True)
df['Tags'] = df['Tags'].astype(str).str.replace(clean_pattern, ' ', regex=True)

# 3. Create the "soup"
print("Creating tag soup...")
df['soup'] = df['Genres'] + " " + df['Tags']

# --- VECTORIZATION ---
# min_df=5: The tag must appear in at least 5 games to count (removes typos/rare noise)
# stop_words='english': Removes words like "the", "and", "is"
tfidf = TfidfVectorizer(stop_words='english', min_df=5, dtype='float32')

# Create the sparse matrix
tfidf_matrix = tfidf.fit_transform(df['soup'])

# --- SAVING ---
print("Saving model to 'recommendation_model.pkl'...")
model_data = {
    'matrix': tfidf_matrix,
    'indices': pd.Series(df.index, index=df['AppID']).to_dict(),
    'app_ids': df['AppID'].values
}

with open('recommendation_model.pkl', 'wb') as f:
    pickle.dump(model_data, f)

print("Done! Model built successfully.")