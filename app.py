# career_advisor_app/app.py
from flask import Flask, render_template, request, jsonify
import json
import os
import pdfplumber
import re
import logging

app = Flask(__name__)
# Remove UPLOAD_FOLDER config and its usage
# app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DATA_FOLDER'] = 'data'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure folders exist
os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)

career_data = None

def load_career_data():
    global career_data
    try:
        data_file_path = os.path.join(app.config['DATA_FOLDER'], 'career_data.json')
        if not os.path.exists(data_file_path):
            logger.error(f"Career data file not found at: {data_file_path}")
            return create_default_career_data()
        if not os.access(data_file_path, os.R_OK):
            logger.error(f"Career data file is not readable: {data_file_path}")
            return create_default_career_data()
        with open(data_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict) or 'career_roles' not in data:
            logger.error("Invalid career data structure - missing 'career_roles' key")
            return create_default_career_data()
        if not isinstance(data['career_roles'], list):
            logger.error("Invalid career data structure - 'career_roles' should be a list")
            return create_default_career_data()
        if len(data['career_roles']) == 0:
            logger.warning("Career data contains no roles")
            return create_default_career_data()
        required_fields = ['role', 'category', 'required_skills', 'preferred_skills', 'average_salary', 'growth_trend', 'recommended_courses']
        valid_roles = []
        for i, role in enumerate(data['career_roles']):
            if not isinstance(role, dict):
                logger.warning(f"Role at index {i} is not a dictionary, skipping")
                continue
            missing_fields = [field for field in required_fields if field not in role]
            if missing_fields:
                logger.warning(f"Role '{role.get('role', f'index_{i}')}' missing fields: {missing_fields}, skipping")
                continue
            valid_roles.append(role)
        if not valid_roles:
            logger.error("No valid roles found in career data")
            return create_default_career_data()
        data['career_roles'] = valid_roles
        logger.info(f"Successfully loaded {len(valid_roles)} career roles")
        return data
    except Exception as e:
        logger.error(f"Unexpected error loading career data: {e}")
        return create_default_career_data()

def create_default_career_data():
    logger.info("Creating default career data")
    return {
        "career_roles": [
            {
                "role": "Software Engineer",
                "category": "Technology",
                "required_skills": ["Python", "JavaScript", "Git", "SQL"],
                "preferred_skills": ["React", "Node.js", "Docker", "AWS"],
                "average_salary": {
                    "entry": 75000,
                    "mid": 110000,
                    "senior": 150000,
                    "lead": 200000
                },
                "growth_trend": {
                    "years": [2020, 2021, 2022, 2023, 2024],
                    "demand_index": [85, 90, 95, 100, 105]
                },
                "recommended_courses": [
                    {
                        "title": "Complete Python Bootcamp",
                        "platform": "Udemy",
                        "duration": "40 hours",
                        "rating": 4.6
                    }
                ],
                "job_outlook": "Excellent",
                "remote_friendly": True,
                "experience_level": "Entry to Senior",
                "top_companies": ["Google", "Microsoft", "Amazon"],
                "career_paths": ["Senior Engineer", "Tech Lead", "Engineering Manager"]
            },
            {
                "role": "Data Scientist",
                "category": "Data & Analytics",
                "required_skills": ["Python", "Statistics", "Machine Learning", "SQL"],
                "preferred_skills": ["R", "TensorFlow", "Tableau", "AWS"],
                "average_salary": {
                    "entry": 80000,
                    "mid": 120000,
                    "senior": 160000,
                    "lead": 220000
                },
                "growth_trend": {
                    "years": [2020, 2021, 2022, 2023, 2024],
                    "demand_index": [80, 85, 92, 98, 103]
                },
                "recommended_courses": [
                    {
                        "title": "Data Science Specialization",
                        "platform": "Coursera",
                        "duration": "60 hours",
                        "rating": 4.5
                    }
                ],
                "job_outlook": "Very Good",
                "remote_friendly": True,
                "experience_level": "Entry to Senior",
                "top_companies": ["Netflix", "Airbnb", "Uber"],
                "career_paths": ["Senior Data Scientist", "ML Engineer", "Data Science Manager"]
            }
        ]
    }

def get_career_data():
    global career_data
    if career_data is None:
        career_data = load_career_data()
    return career_data

@app.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        target_role = request.form.get('target_role', '').strip()
        if not target_role:
            return jsonify({'error': 'Target role must be selected before analysis'}), 400
        # Ensure file is not None and has a filename
        if file and hasattr(file, 'filename') and file.filename.endswith('.pdf'):
            # Read PDF directly from memory without saving to disk
            import io
            text = ""
            with pdfplumber.open(io.BytesIO(file.read())) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            resume_skills = extract_skills(text)
            return analyze_resume(resume_skills, target_role)
        return jsonify({'error': 'Invalid file format'}), 400
    except Exception as e:
        logger.error(f"Error in upload_resume: {e}")
        return jsonify({'error': 'Failed to process resume'}), 500

@app.route('/api/roles', methods=['GET'])
def get_roles():
    try:
        data = get_career_data()
        roles = [role['role'] for role in data['career_roles']]
        return jsonify({'roles': roles})
    except Exception as e:
        logger.error(f"Error fetching roles: {e}")
        return jsonify({'roles': []}), 500

def extract_skills(text):
    try:
        data = get_career_data()
        all_skills = set()
        for role in data['career_roles']:
            all_skills.update(role.get('required_skills', []))
            all_skills.update(role.get('preferred_skills', []))
        found_skills = set()
        for skill in all_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                found_skills.add(skill)
        return list(found_skills)
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        return []

def analyze_resume(resume_skills, target_role):
    try:
        data = get_career_data()
        role_data = None
        for role in data['career_roles']:
            if role.get('role', '').lower() == target_role.lower():
                role_data = role
                break
        if not role_data:
            available_roles = [role.get('role', 'Unknown') for role in data['career_roles']]
            return jsonify({
                'error': f'Target role "{target_role}" not found.',
                'available_roles': available_roles,
                'suggestion': 'Please select a role from the available options.'
            }), 404
        required_skills = role_data.get('required_skills', [])
        preferred_skills = role_data.get('preferred_skills', [])
        missing_required = [s for s in required_skills if s not in resume_skills]
        missing_preferred = [s for s in preferred_skills if s not in resume_skills]
        matched_skills = [s for s in required_skills + preferred_skills if s in resume_skills]
        total_skills = len(required_skills) + len(preferred_skills)
        match_percentage = int((len(matched_skills) / total_skills) * 100) if total_skills else 0
        improvement_plan = []
        all_role_courses = role_data.get('recommended_courses', [])
        for skill in missing_required[:3]:
            improvement_plan.append({
                'skill': skill,
                'priority': 'High',
                'resources': find_courses(skill) + all_role_courses
            })
        for skill in missing_preferred[:2]:
            improvement_plan.append({
                'skill': skill,
                'priority': 'Medium',
                'resources': find_courses(skill) + all_role_courses
            })
        return jsonify({
            'role': role_data.get('role', 'Unknown'),
            'match_percentage': match_percentage,
            'matched_skills': matched_skills,
            'missing_required': missing_required,
            'missing_preferred': missing_preferred,
            'improvement_plan': improvement_plan,
            'salary_range': role_data.get('average_salary', {}),
            'career_paths': role_data.get('career_paths', [])
        })
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        return jsonify({'error': 'Failed to analyze resume'}), 500

def find_courses(skill):
    try:
        data = get_career_data()
        courses = []
        for role in data['career_roles']:
            for course in role.get('recommended_courses', []):
                if skill.lower() in course.get('title', '').lower():
                    courses.append(course)
        return courses[:3]
    except Exception as e:
        logger.error(f"Error finding courses for skill {skill}: {e}")
        return []

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        career_data = load_career_data()
        logger.info(f"Application started with {len(career_data['career_roles'])} career roles")
    except Exception as e:
        logger.error(f"Failed to initialize career data: {e}")
    app.run(debug=True)