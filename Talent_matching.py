import os
from agno.agent import Agent
from agno.team.team import Team
from agno.tools.reasoning import ReasoningTools
from agno.models.openai import OpenAIChat
import fitz
from pydantic import BaseModel, Field
from textwrap import dedent
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CVProcessor(BaseModel):
    """Structured CV processing with specific requirements"""

    job_requirements: str = Field(description="Job requirements")
    candidate_cv: str = Field(description="Candidate resume")
    instructions: str = Field(description="Instructions for the agent")


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

# CV Parser Agent
cv_parser_agent = Agent(
    name="CVParser",
    role="Extract skills, experiences, education, and other relevant information from CVs in PDF/text/JSON format.",
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    tools=[ReasoningTools()],
    instructions=dedent("""
        From the candidate CV, extract:
        - Skills and competencies
        - Work experience (roles and duration)
        - Education history
        - Certifications or achievements
        Output a structured JSON summarizing the candidate profile.
    """).strip(),
    markdown=True,
)

# Job Matcher Agent
job_matcher_agent = Agent(
    name="JobMatcher",
    role="Compare candidate profile with job description and calculate a matching score.",
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    tools=[ReasoningTools()],
    instructions=dedent("""
        Using the candidate profile and the job description, analyze:
        - Skill fit (technical and soft skills)
        - Experience relevance
        - Education requirements
        - Certifications or achievements
        Provide a matching score (1-10) with rationale for each component.
    """).strip(),
    markdown=True,
)

# Report Writer Agent
report_writer_agent = Agent(
    name="ReportWriter",
    role="Write a recruiter-friendly summary report highlighting candidate fit for the job. Display the report in a table format.",
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    instructions=dedent("""
        Create a professional report including:
        1. Summary: Overall fit and key highlights
        2. Strengths: Skills and experiences matching the job
        3. Weaknesses: Gaps or missing competencies
        4. Recommendations: Suitability, potential training, or interview focus
        Format clearly with headers and bullet points.
    """).strip(),
    markdown=True,
)

# HR Team
hr_team = Team(
    name="HR Recruitment Team",
    delegate_task_to_all_members=True,
    members=[cv_parser_agent, job_matcher_agent, report_writer_agent],
    model=OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY),
    instructions=dedent("""
        Execute a coordinated workflow for candidate evaluation:

        Phase 1 - CV Parsing:
        - CVParser extracts candidate data into a structured profile

        Phase 2 - Job Matching:
        - JobMatcher compares profile with job description
        - Calculate matching score and rationale

        Phase 3 - Reporting:
        - ReportWriter generates a clear recruiter report
        - Highlight strengths, weaknesses, and recommendations

        Ensure smooth information flow between agents. Use tables to display the report.
    """).strip(),
    markdown=True,
)


JOB_DESCRIPTION = dedent("""
Position: Fullstack Developer
Requirements:
- Strong Python and React skills
- Experience with SQL databases
- Bachelor's degree in Computer Science or related
""").strip()


if __name__ == "__main__":
    cv_folder = os.path.join("AGNO_TEAMS_BAH_IBRAHIM")

    for filename in os.listdir(cv_folder):
        if filename.lower().endswith(".pdf"):
            cv_path = os.path.join(cv_folder, filename)
            cv_text = extract_text_from_pdf(cv_path)

            print(f"\n--- Processing {filename} ---\n")

            hr_team.print_response(
                input=CVProcessor(
                    candidate_cv=cv_text,
                    job_requirements=JOB_DESCRIPTION,
                    instructions="Be concise"
                ),
                stream=True
            )
