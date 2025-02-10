import requests
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from requests.auth import HTTPBasicAuth  # Import for basic auth

def fetch_sonarqube_issues(sonarqube_url, project_key, token):
    url = f"{sonarqube_url}/api/issues/search?componentKeys={project_key}&resolved=false"

    # Use Basic Authentication
    response = requests.get(url, auth=HTTPBasicAuth(token, ""))  

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching issues: {response.status_code} - {response.text}")
        return None

def generate_pdf_report(issues, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 40, "SonarQube Issues Report")

    c.setFont("Helvetica", 12)
    y_position = height - 80

    for issue in issues.get("issues", []):
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50

        issue_text = f"[{issue['severity']}] {issue['message']} (File: {issue.get('component', 'N/A')})"
        c.drawString(50, y_position, issue_text[:100])  # Truncate if too long
        y_position -= 20

    c.save()
    print(f"PDF report generated: {output_file}")

if __name__ == "__main__":
    SONARQUBE_URL = "http://172.30.4.180:9000"  # Change as needed
    PROJECT_KEY = "genebank-frontend"
    TOKEN = "sqa_c3a1f251c92e57ce5162fdbd782983de90741cd1"  # Replace with your token
    OUTPUT_FILE = "sonarqube_issues_report.pdf"

    issues_data = fetch_sonarqube_issues(SONARQUBE_URL, PROJECT_KEY, TOKEN)
    if issues_data:
        generate_pdf_report(issues_data, OUTPUT_FILE)

