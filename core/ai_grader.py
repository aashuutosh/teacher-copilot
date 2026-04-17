import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the secret API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. HACKATHON TRICK: Dynamically find an available model
working_model = "gemini-1.5-flash" # Fallback
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            working_model = m.name
            break # Grab the absolute first model that works!
except Exception as e:
    pass

# Initialize the model with whichever one we found
model = genai.GenerativeModel(working_model)

# 3. The Grading Logic
def grade_submission(student_text, rubric_text=""):
    
    rubric_instructions = ""
    if rubric_text != "":
        rubric_instructions = f"\nCRITICAL: You must grade this submission STRICTLY according to the following rubric rules:\n{rubric_text}\n"

    prompt = f"""
    You are an expert teacher. Evaluate the following student submission.
    1. Provide a brief, encouraging critique.
    2. Point out any grammatical or logical mistakes.
    3. Give the submission a score out of 10.
    {rubric_instructions}
    
    Student Submission: 
    {student_text}
    """
    
    response = model.generate_content(prompt)
    return response.text