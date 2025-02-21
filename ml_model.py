import os
import pandas as pd
import numpy as np
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine

# Load English NLP model for text preprocessing
nlp = spacy.load("en_core_web_sm")

class JobPredictor:
    def __init__(self, database_uri=None):
        # Set up database connection
        self.database_uri = database_uri or os.getenv('DATABASE_URL', 'mysql+pymysql://root:CakeTown%402024@localhost/careergo')
        self.engine = create_engine(self.database_uri)
        
        # Load and process job data
        self.job_data = self.load_job_data()
        
        # Train TF-IDF model
        self.vectorizer, self.tfidf_matrix = self.train_tfidf()

    def clean_text(self, text):
        """Preprocess text by removing special characters, lemmatizing, and removing stopwords."""
        if not isinstance(text, str):
            return ""

        text = re.sub(r'[^a-zA-Z\s]', '', text).lower().strip()
        doc = nlp(text)
        clean_words = [token.lemma_ for token in doc if not token.is_stop]
        return " ".join(clean_words)

    def load_job_data(self):
        """Load job categories and descriptions from the database, then clean the text."""
        query = "SELECT category, text FROM job_data"
        df = pd.read_sql(query, con=self.engine)
        df["cleaned_text"] = df["text"].apply(self.clean_text)
        return df

    def train_tfidf(self):
        """Train a TF-IDF model on job descriptions."""
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(self.job_data["cleaned_text"])
        return vectorizer, tfidf_matrix

    def match_resume(self, resume_text, top_n=5):
        """Match a resume to the top job categories using TF-IDF cosine similarity."""
        cleaned_resume = self.clean_text(resume_text)
        resume_vector = self.vectorizer.transform([cleaned_resume])
        similarity_scores = cosine_similarity(resume_vector, self.tfidf_matrix)[0]

        top_indices = np.argsort(similarity_scores)[::-1][:top_n]
        top_matches = [{"category": self.job_data.iloc[i]["category"], "score": round(similarity_scores[i], 2)} for i in top_indices]

        return top_matches

# Main Execution (for testing)
if __name__ == "__main__":
    predictor = JobPredictor()
    
    sample_resume = """Experienced data analyst skilled in Python, SQL, and machine learning. 
                       Proficient in data visualization tools like Tableau and Power BI."""

    top_matches = predictor.match_resume(sample_resume)

    print("\nTop 5 Job Category Matches:")
    for match in top_matches:
        print(f"- {match['category']} (Score: {match['score']})")
