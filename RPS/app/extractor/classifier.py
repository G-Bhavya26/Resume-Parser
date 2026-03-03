import re
from typing import Dict, List, Tuple

SECTION_PATTERNS = {
    "education": [
        r"education",
        r"academic\s+background",
        r"qualifications",
        r"academic\s+details"
    ],
    "skills": [
        r"technical\s+skills",
        r"skills",
        r"technologies",
        r"tools\s+&\s+technologies",
        r"competencies"
    ],
    "projects": [
        r"projects",
        r"academic\s+projects",
        r"personal\s+projects",
        r"key\s+projects"
    ],
    "experience": [
        r"experience",
        r"internships?",
        r"work\s+experience",
        r"industrial\s+training",
        r"professional\s+experience",
        r"employment\s+history"
    ],
    "certifications": [
        r"certifications?",
        r"courses?",
        r"online\s+courses",
        r"professional\s+development"
    ],
    "achievements": [
        r"achievements?",
        r"awards?",
        r"honors?",
        r"extracurricular",
        r"co-curricular"
    ]
}

def classify_sections(text: str) -> Dict[str, str]:
    """
    Parses resume text into logical sections based on common headings.
    Returns a dictionary mapping section names to their corresponding text content.
    """
    lines = text.split("\n")
    sections = {k: [] for k in SECTION_PATTERNS.keys()}
    sections["unknown"] = []
    
    current_section = "unknown"
    
    # Compile regexes for performance
    compiled_patterns = {}
    for section, patterns in SECTION_PATTERNS.items():
        # Match only if the line is relatively short (headers usually are)
        # and starts with the pattern (ignoring leading whitespace/punctuation)
        regex_str = r"^\s*[^a-zA-Z]*(" + "|".join(patterns) + r")\b.*$"
        compiled_patterns[section] = re.compile(regex_str, re.IGNORECASE)

    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
            
        # Check if the line is a header
        is_header = False
        if len(cleaned_line.split()) <= 5: # Headers are usually short
            for section, pattern in compiled_patterns.items():
                if pattern.match(cleaned_line):
                    current_section = section
                    is_header = True
                    break
        
        # If it's a header, we don't necessarily need to add it to the content
        # But if it's not, append the line to the current active section
        if not is_header:
            sections[current_section].append(line)
            
    # Join the lists back into strings
    return {k: "\n".join(v) for k, v in sections.items() if v}
