# train_recommendation_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

dirname = os.path.dirname(os.path.abspath(__file__))
os.chdir(dirname)

# Load the synthetic dataset
data = pd.read_csv("../data/books_dataset.csv")

# For simplicity, let's use genre and average_rating for recommendation
# Convert categorical genre to numerical
data['genre'] = data['genre'].astype('category').cat.codes

# Features and target variable
X = data[['genre', 'average_rating']]
y = data['book_id']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "../model/recommendation_model.pkl")

