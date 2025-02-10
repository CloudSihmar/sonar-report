import requests
from fpdf import FPDF

# SonarQube Configuration
SONARQUBE_URL = "http://172.30.4.180:9000"
PROJECT_KEY = "genebank-frontend"
SONARQUBE_TOKEN = "sqa_c3a1f251c92e57ce5162fdbd782983de90741cd1"

# API Endpoint for Issues
API_URL = f"{SONARQUBE_URL}/api/issues/search?componentKeys={PROJECT_KEY}&types=BUG,VULNERABILITY,CODE_SMELL&ps=500"

# Fetching Issues
response = requests.get(API_URL, auth=(SONARQUBE_TOKEN, ""))
data = response.json()

# Check if request was successful
if "issues" not in data:
    print("Error fetching data from SonarQube")
    exit()

issues = data["issues"]

# Creating a PDF Report
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", style='B', size=16)
pdf.cell(200, 10, "SonarQube Issues Report", ln=True, align="C")
pdf.ln(10)

# Summary Section
pdf.set_font("Arial", style='B', size=12)
pdf.cell(200, 10, f"Total Issues Found: {len(issues)}", ln=True)
pdf.ln(5)

# Categorize Issues
severities = {"BLOCKER": [], "CRITICAL": [], "MAJOR": [], "MINOR": [], "INFO": []}
for issue in issues:
    severity = issue.get("severity", "INFO")
    severities[severity].append(issue)

# Print summary
for severity, issues_list in severities.items():
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, f"{severity}: {len(issues_list)}", ln=True)
pdf.ln(10)

# Add Issue Details
for severity, issues_list in severities.items():
    if len(issues_list) > 0:
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(200, 10, f"{severity} Issues", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", size=10)
        for issue in issues_list:
            file_path = issue.get("component", "Unknown File")
            message = issue.get("message", "No description")
            line = issue.get("line", "Unknown")
            pdf.multi_cell(0, 6, f"- {message} (File: {file_path}, Line: {line})")
            pdf.ln(2)

        pdf.ln(5)  # Space between sections

# Save PDF
pdf.output("SonarQube_Report.pdf")

print("PDF report generated: SonarQube_Report.pdf")

