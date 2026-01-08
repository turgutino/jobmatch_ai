import re

def extract_tech_stack(text):
    keywords = [
        "Python", "Java", "C++", "C#", "JavaScript", "TypeScript",
        "Django", "Flask", "React", "Node.js",
        "SQL", "MySQL", "PostgreSQL", "MongoDB",
        "Docker", "Kubernetes",
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "AWS", "Azure", "GCP"
    ]

    found = set()

    for kw in keywords:
        if kw.lower() in text.lower():
            found.add(kw)

    return list(found)


def extract_projects(text):
    lines = text.split("\n")
    projects = []

    for line in lines:
        if "project" in line.lower() or "developed" in line.lower() or "built" in line.lower():
            projects.append(line.strip())

    return projects


def analyze_resume(text):
    tech_stack = extract_tech_stack(text)
    projects = extract_projects(text)

    summary = {
        "tech_stack": tech_stack,
        "projects": projects,
        "summary_text": f"The candidate has experience in: {', '.join(tech_stack)}."
    }

    return summary
