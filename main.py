import logging
from job_finder import JobFinder
from resume_generator import ResumeGenerator

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def search_and_save_jobs(job_title, location):
    job_finder = JobFinder()

    logger.info(f"Searching for {job_title} jobs in {location}")
    jobs = job_finder.search_jobs(job_title, location)

    if not jobs:
        logger.warning("No jobs found. Exiting.")
        return None

    logger.info(f"Found {len(jobs)} jobs")

    # Saving found vacancies in CSV
    job_finder.save_jobs_to_csv(jobs, "found_jobs.csv")

    return jobs


def get_job_details(job_finder, job):
    # Get detailed information for a specific job
    logger.info(f"Getting details for the job: {job['title']} at {job['company']}")
    job_description = job_finder.parse_job_details(job['url'])

    if not job_description:
        logger.warning("Failed to get job details.")
        return None

    return {
        'title': job['title'],
        'company': job['company'],
        'location': job['location'],
        'description': job_description
    }


def generate_resume(resume_generator, user_info, job_details):
    # Generate a personalized resume
    logger.info("Generating personalized resume")
    resume_filename = resume_generator.create_resume(user_info, job_details)
    if resume_filename:
        logger.info(f"Resume generated and saved as {resume_filename}")
        return resume_filename
    else:
        logger.error("Failed to generate resume")
        return None


def get_user_info():
    # user info
    return {
        'name': 'Example Name',
        'email': 'exampleemail@example.com',
        'phone': '123-456-7890',
        'education': [
            {'degree': 'Bachelor', 'field': 'Computer Science', 'institution': 'XYZ University', 'year': '2021'}
        ],
        'experience': [
            {
                'position': 'Junior Python Developer',
                'company': 'Tech Corp',
                'start_date': 'Jan 2021',
                'end_date': 'Present',
                'description': 'Developed web applications using Python and Django.'
            }
        ],
        'skills': ['Python', 'Django', 'JavaScript', 'SQL']
    }


def main():
    # the job search and resume generation process
    job_title = "Python Developer"
    location = "New York"

    print("=== Searching for Jobs ===")
    jobs = search_and_save_jobs(job_title, location)
    if not jobs:
        return

    job_finder = JobFinder()
    resume_generator = ResumeGenerator()

    print("\n=== Generating Resume ===")
    user_info = get_user_info()

    jobs_details = []
    for job in jobs[:5]:  # limit of 5 vacancies
        job_details = get_job_details(job_finder, job)
        if job_details:
            jobs_details.append(job_details)
        else:
            print(f"Failed to get details for job: {job['title']}")

    if jobs_details:
        resume_filename = resume_generator.create_resume(user_info, jobs_details)
        if resume_filename:
            print(f"Resume successfully created: {resume_filename}")
        else:
            print("Failed to create resume")
    else:
        print("No job details available to create resume")


if __name__ == "__main__":
    main()