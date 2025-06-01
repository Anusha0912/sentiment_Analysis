# model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Load and clean dataset
data = pd.read_csv("sentiment_dataset.csv")
data.dropna(inplace=True)

# Fix label mapping: 1 = Positive, 0 = Negative
data['label'] = data['label'].apply(lambda x: 1 if x == 1 else 0)

# Features and labels
texts = data['sentence'].astype(str).tolist()
labels = data['label'].astype(int).tolist()

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(texts)

# Train model
model = MultinomialNB()
model.fit(X, labels)

# Save model and vectorizer
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model and vectorizer saved with TF-IDF!")
