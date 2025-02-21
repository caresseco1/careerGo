import pandas as pd
from models import JobData
from database import db
from careergo.app import app

def load_resume_data():
    # Load the CSV data
    df = pd.read_csv("hf://datasets/ahmedheakl/resume-atlas/train.csv")

    # Strip any spaces in column names
    df.columns = df.columns.str.strip().str.lower()  # Normalize column names
    
    # Debug: Print column names to verify correct headers
    print("CSV Columns:", df.columns)

    # Ensure the required columns exist
    required_columns = {"category", "text"}
    if not required_columns.issubset(set(df.columns)):
        raise KeyError(f"Missing columns in CSV file. Found: {df.columns}, Expected: {required_columns}")

    with app.app_context():
        # Process and load data into job_data table
        for _, row in df.iterrows():
            new_job_data = JobData(
                category=row['category'],
                text=row['text']
            )
            db.session.add(new_job_data)
        
        db.session.commit()

if __name__ == "__main__":
    load_resume_data()
    print("Resume data loaded successfully!")
