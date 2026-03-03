import asyncio
from fpdf import FPDF
from app.pipeline.executor import process_resume
import json

def create_mock_resume():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Write a mock resume
    text = """
    JOHN DOE
    john.doe@email.com | +1234567890
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology | 2020 - 2024
    CGPA: 3.8/4.0
    
    TECHNICAL SKILLS
    Programming Languages: Python, JavaScript, C++
    Web Technologies: React.js, Node.js, HTML/CSS
    Databases: PostgreSQL, MongoDB, Redis
    Tools: Docker, Kubernetes, Git, AWS
    Machine Learning: TensorFlow, PyTorch
    
    EXPERIENCE
    Software Engineering Intern
    Tech Innovations Inc | June 2023 - August 2023
    - Developed a scalable REST API using FastAPI and Python.
    - Containerized applications using Docker and orchestrated with Kubernetes.
    - Improved database query performance in PostgreSQL by 30%.
    
    PROJECTS
    E-Commerce Web Application
    - Built a full-stack e-commerce site using React and Node.js.
    - Integrated Stripe for payments and maintained a MongoDB backend.
    
    CERTIFICATIONS
    AWS Certified Cloud Practitioner
    """
    
    pdf.multi_cell(0, 10, txt=text)
    pdf.output("tests/mock_resume.pdf")

def run_test():
    create_mock_resume()
    print("Mock resume generated at tests/mock_resume.pdf")
    
    # Read the file bytes
    with open("tests/mock_resume.pdf", "rb") as f:
        content = f.read()
        
    print("Executing pipeline (normal mode)...")
    result = process_resume(content, "mock_resume.pdf", anonymize=False)
    print(f"Name: {result.student_name}, Email: {result.email}")
    print(f"Skills Found: {[s.name for s in result.skills]}")
    print(f"Unknown Skills: {result.unknown_skills}")
    
    print("\nExecuting pipeline (anonymized mode)...")
    result_anon = process_resume(content, "mock_resume.pdf", anonymize=True)
    print(f"Anonymized Name: {result_anon.student_name}, Anonymized Email: {result_anon.email}")
    
    print("\n--- PIPELINE RESULT ---")
    print(f"Status: {result.parse_status}")
    
    print("\nEmbeddings:")
    if result.skills_embedding:
        print(f"Skills Vector length: {len(result.skills_embedding)} (first 3: {result.skills_embedding[:3]})")
    if result.overall_embedding:
        print(f"Overall Vector length: {len(result.overall_embedding)} (first 3: {result.overall_embedding[:3]})")
        
    print("\nFull JSON structure saved to tests/output.json")
    with open("tests/output.json", "w") as f:
        f.write(result.model_dump_json(indent=2))

if __name__ == "__main__":
    run_test()
