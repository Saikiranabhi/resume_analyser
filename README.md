# 🧠 Resume Analyzer

Resume Analyzer is an AI-powered web application that helps users analyze their resumes, identify skill gaps, and receive actionable suggestions to improve their chances in the job market. Upload your PDF resume, select a target job role, and get instant feedback on your skills, missing competencies, and recommended learning resources.

## 🚀 Features

- Upload your resume (PDF format)
- Select a target job role from a comprehensive list
- Analyze your skill set and receive improvement suggestions
- Detect missing skills based on current job market needs
- Get recommended courses and resources for upskilling
- Visual insights into job market trends and salary data

## 🛠️ Tech Stack

| Category           | Tools Used                        |
|--------------------|-----------------------------------|
| **Frontend**       | HTML, CSS, Bootstrap              |
| **Backend**        | Python, Flask                     |
| **Resume Parsing** | pdfplumber                        |
| **Visualization**  | Plotly, Wordcloud                 |
| **Data Handling**  | Pandas, Numpy                     |
| **Image Processing**| Pillow                           |
| **Deployment**     | Gunicorn                          |

## 📁 Project Structure

```
Resume_analyser/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── improvement_plan_resources.json # Resources for improvement plans
├── data/
│   └── career_data.json        # Job roles and skills data
├── static/
│   └── dashboard.css           # Stylesheets
├── templates/
│   └── dashboard.html          # Main HTML template
```

## ⚡ Getting Started

1. **Clone the repository:**
   ```bash
   git clone <your-git-repo-link>
   cd Resume_analyser
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   python app.py
   ```
4. **Open your browser:**
   Go to [http://localhost:5000](http://localhost:5000)
5. **Upload your resume and select a target role to get your analysis.**

## 📊 Data

- The app uses `data/career_data.json` for job roles, required/preferred skills, salary, and trends.
- Improvement resources are in `improvement_plan_resources.json`.

## 🌐 Links

- **GitHub Repository:** [https://github.com/Saikiranabhi/resume_analyser.git]
- **Live Demo:** [https://resume-analyser-2baz.onrender.com/]

## 📝 License

MIT

