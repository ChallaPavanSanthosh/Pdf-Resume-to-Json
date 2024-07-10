import json
import re
from pdfminer.high_level import extract_text

def extract_resume_text(pdf_path):
    """Extract text from a PDF file."""
    return extract_text(pdf_path)

def parse_resume(text):
    """Parse the extracted text and convert it to a structured JSON format."""
    resume = {}
    
    # Personal Details
    personal_details_pattern = re.compile(r"Name\s*:\s*(.*)\nPhone\s*:\s*(.*)\nEmail\s*:\s*(.*)\nAddress\s*:\s*(.*)\nDate of Birth\s*:\s*(.*)\nLanguages\s*:\s*(.*)\nGender\s*:\s*(.*)\nMarital Status\s*:\s*(.*)", re.MULTILINE)
    personal_details_match = personal_details_pattern.search(text)
    if personal_details_match:
        resume["personal_details"] = {
            "name": personal_details_match.group(1).strip(),
            "phone_numbers": [phone.strip() for phone in personal_details_match.group(2).split(',')],
            "emails": [email.strip() for email in personal_details_match.group(3).split(',')],
            "address": personal_details_match.group(4).strip(),
            "date_of_birth": personal_details_match.group(5).strip(),
            "languages": [language.strip() for language in personal_details_match.group(6).split(',')],
            "gender": personal_details_match.group(7).strip(),
            "marital_status": personal_details_match.group(8).strip()
        }
    
    # Education
    education_pattern = re.compile(r"Education\n(.*?)(?:Skills|Experience|Projects|Certifications|Awards)", re.DOTALL)
    education_match = education_pattern.search(text)
    if education_match:
        education_text = education_match.group(1).strip()
        education_entries = re.findall(r"Degree\s*:\s*(.*?)\nInstitution\s*:\s*(.*?)\nYear\s*:\s*(.*?)\n(?:CGPA|Percentage)\s*:\s*(.*?)\n", education_text)
        resume["education"] = [
            {
                "degree": entry[0].strip(),
                "institution": entry[1].strip(),
                "year": entry[2].strip(),
                "cgpa_or_percentage": entry[3].strip()
            }
            for entry in education_entries
        ]
    
    # Skills
    skills_pattern = re.compile(r"Skills\n(.*?)(?:Experience|Projects|Certifications|Awards)", re.DOTALL)
    skills_match = skills_pattern.search(text)
    if skills_match:
        skills_text = skills_match.group(1).strip()
        resume["skills"] = [skill.strip() for skill in skills_text.split('\n')]
    
    # Experience
    experience_pattern = re.compile(r"Experience\n(.*?)(?:Projects|Certifications|Awards)", re.DOTALL)
    experience_match = experience_pattern.search(text)
    if experience_match:
        experience_text = experience_match.group(1).strip()
        experience_entries = re.findall(r"Title\s*:\s*(.*?)\nCompany\s*:\s*(.*?)\nDuration\s*:\s*(.*?)\nKey Skills\s*:\s*(.*?)\nDescription\s*:\s*(.*?)\n", experience_text, re.DOTALL)
        resume["experience"] = [
            {
                "title": entry[0].strip(),
                "company": entry[1].strip(),
                "duration": entry[2].strip(),
                "key_skills": [skill.strip() for skill in entry[3].split(',')],
                "description": entry[4].strip()
            }
            for entry in experience_entries
        ]
    
    # Projects
    projects_pattern = re.compile(r"Projects\n(.*?)(?:Certifications|Awards)", re.DOTALL)
    projects_match = projects_pattern.search(text)
    if projects_match:
        projects_text = projects_match.group(1).strip()
        project_entries = re.findall(r"Title\s*:\s*(.*?)\nTeam Size\s*:\s*(.*?)\nDuration\s*:\s*(.*?)\nKey Skills\s*:\s*(.*?)\nProject Link\s*:\s*(.*?)\nDescription\s*:\s*(.*?)\n", projects_text, re.DOTALL)
        resume["projects"] = [
            {
                "title": entry[0].strip(),
                "team_size": entry[1].strip(),
                "duration": entry[2].strip(),
                "key_skills": [skill.strip() for skill in entry[3].split(',')],
                "project_link": entry[4].strip(),
                "description": entry[5].strip()
            }
            for entry in project_entries
        ]
    
    # Certifications
    certifications_pattern = re.compile(r"Certifications\n(.*?)(?:Awards)", re.DOTALL)
    certifications_match = certifications_pattern.search(text)
    if certifications_match:
        certifications_text = certifications_match.group(1).strip()
        certification_entries = re.findall(r"Title\s*:\s*(.*?)\nKey Skills\s*:\s*(.*?)\n", certifications_text)
        resume["certifications"] = [
            {
                "title": entry[0].strip(),
                "key_skills": [skill.strip() for skill in entry[1].split(',')]
            }
            for entry in certification_entries
        ]
    
    return resume

def save_json(data, json_path):
    """Save the data to a JSON file."""
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python convert_resume.py input/your_resume.pdf output/resume.json")
        sys.exit(1)

    pdf_path = sys.argv[1]
    json_path = sys.argv[2]

    text = extract_resume_text(pdf_path)
    print("Extracted Text:\n", text)  # Add this line to check extracted text

    resume_json = parse_resume(text)
    print("Parsed Resume JSON:\n", json.dumps(resume_json, indent=4))  # Print parsed JSON for debugging

    save_json(resume_json, json_path)

    print(f"Resume has been successfully converted to JSON format and saved to {json_path}")

