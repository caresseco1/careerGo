from models import JobData  # Import only JobData
from database import db
from careergo.app import app

def check_data():
    with app.app_context():
        job_data_count = JobData.query.count()  # Query job_data table
        
        print(f"Number of job data entries: {job_data_count}")

if __name__ == "__main__":
    check_data()
