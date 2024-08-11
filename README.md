This project combines job searching capabilities with an automated resume generator. It's designed to streamline the job application process by finding relevant job listings and creating tailored resumes.
Components
Project files : job_finder.py , resume_generator.py  , main.py

1. job_finder.py
A web scraping tool that searches for job listings on Indeed.com.
Features:
- Automated job searching based on keywords and location
- Web scraping with Selenium and BeautifulSoup
- Handling of CAPTCHAs and page loading
- Extraction of job details including title, company, location, and description
- Saving job listings to a CSV file

2. resume_generator.py
An automated tool for creating personalized resumes.
Features:
- Generation of a basic resume template
- Adding personal information, education, work experience, and skills
- Saving the resume as a Word document

3. main.py
Features:
- Searches for jobs based on user-specified criteria
- Retrieves detailed information for found jobs
- Generates a personalized resume incorporating user information and job details

How to use:
Set up your Python environment and install required dependencies.
Run main.py to start the job search and resume generation process.
The script will search for jobs, save them to a CSV file, and generate a personalized resume with relevant job listings.

Requirements:
Python 3.x
Selenium WebDriver
BeautifulSoup4
python-docx

Note
This project is for educational purposes and demonstrates web scraping, document generation, and process automation in Python. 
Please use responsibly and in accordance with the terms of service of any websites you interact with.
