from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

class ResumeGenerator():
    def __init__(self):
        self.document = Document()

    def create_basic_template(self):
        # creating basic resume template
        self.document.add_heading('Resume', 0)

    def add_personal_info(self, name, email, phone):
        #add pers info
        self.document.add_paragraph(name)
        self.document.add_paragraph(f"Email: {email}")

    def add_education(self, education_list):
        # add info about education
        self.document.add_heading('Education', 1)
        for edu in education_list:
            p = self.document.add_paragraph()
            p.add_run(f"{edu['degree']} in {edu['field']}").bold = True
            p.add_run(f"\n{edu['institution']}, {edu['year']}")

    def add_experience(self, experience_list):
        #add info about previous experience
        self.document.add_heading('Work Experience', 1)
        for exp in experience_list:
            p = self.document.add_paragraph()
            p.add_run(f"{exp['position']} at {exp['company']}").bold = True
            p.add_run(f"\n{exp['start_date']} - {exp['end_date']}")
            p.add_run(f"\n{exp['description']}")

    def add_skills(self, skills):
        #add list your skills
        self.document.add_heading('Skills', 1)
        skill_para = self.document.add_paragraph()
        skill_para.add_run(', '.join(skills))

    def customize_for_job(self, job_description):
        # personolise resume for specific vacancies
        self.document.add_heading('Job-Specific Qualifications', 1)
        self.document.add_paragraph(job_description)

    def save_resume(self, filename):
        # save resume in file
        self.document.save(filename)

    def create_resume(self, user_info, job_details):
        #create full resume
        self.create_basic_template()
        self.add_personal_info(user_info['name'], user_info['email'], user_info['phone'])
        self.add_education(user_info['education'])
        self.add_experience(user_info['experience'])
        self.add_skills(user_info['skills'])
        self.customize_for_job(job_details['description'])

        filename = f"resume_{user_info['name'].replace(' ', '_')}.docx"
        self.save_resume(filename)
        return filename


#example
if __name__ == "__main__":
    user_info = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '123-456-7890',
        'education': [
            {'degree': 'Bachelor', 'field': 'Computer Science', 'institution': 'XYZ University', 'year': '2020'}
        ],
        'experience': [
            {
                'position': 'Software Developer',
                'company': 'Tech Corp',
                'start_date': 'Jan 2021',
                'end_date': 'Present',
                'description': 'Developed web applications using Python and Django.'
            }
        ],
        'skills': ['Python', 'Django', 'JavaScript', 'SQL']
    }

    job_details = {
        'description': 'Looking for a Python developer with experience in web development.'
    }

    generator = ResumeGenerator()
    resume_file = generator.create_resume(user_info, job_details)
    print(f"Resume created: {resume_file}")
