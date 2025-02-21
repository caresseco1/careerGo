from flask import Blueprint, jsonify, render_template, request
from ml_model import JobPredictor
import PyPDF2
import io

routes_bp = Blueprint("routes", __name__, url_prefix="/")

# Initialize Job Predictor globally
predictor = JobPredictor()

@routes_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@routes_bp.route("/assessment", methods=["GET"])
def assessment():
    return render_template("assessment.html")

@routes_bp.route("/job_market_analysis", methods=["GET"])
def job_market_analysis():
    return render_template("job_market_analysis.html")

@routes_bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@routes_bp.route("/resume_review", methods=["GET", "POST"])
def resume_review():
    if request.method == "POST":
        resume_file = request.files.get("resume")
        if resume_file:
            try:
                resume_text = ""
                
                # Extract text from PDF
                if resume_file.filename.endswith(".pdf"):
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(resume_file.read()))
                    resume_text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
                else:
                    # Handle .txt or .docx files if needed
                    resume_text = resume_file.read().decode("utf-8")
                
                if not resume_text.strip():
                    return jsonify({"error": "Failed to extract text from resume"}), 400

                # Get job matches
                matches = predictor.match_resume(resume_text)
                
                return jsonify({
                    "message": "Resume processed successfully",
                    "matches": matches
                }), 200
            except Exception as e:
                return jsonify({"error": f"Error processing resume: {str(e)}"}), 500
        
        return jsonify({"error": "No resume file provided"}), 400
    
    return render_template("resume_review.html")

@routes_bp.route("/match-jobs", methods=["POST"])
def match_jobs():
    """
    API endpoint to match job categories based on resume text (TF-IDF + Cosine Similarity).
    Expected Input (JSON): { "resume": "Resume text here..." }
    Response: { "top_matches": [("Category1", score), ("Category2", score), ...] }
    """
    data = request.json
    resume_text = data.get("resume", "")
    
    if not resume_text:
        return jsonify({"error": "Resume text is required"}), 400
    
    top_matches = predictor.match_resume(resume_text)
    return jsonify({"top_matches": top_matches})

@routes_bp.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    
    if not all([name, email, message]):
        return jsonify({"error": "All fields are required"}), 400
        
    # Process the contact form data here
    return jsonify({"message": "Message received successfully"}), 200
