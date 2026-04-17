import streamlit as st
from core.ai_grader import grade_submission
from core.rag_engine import extract_text_from_pdf
from core.privacy import scrub_pii

# 1. Page Config
st.set_page_config(page_title="Teacher Copilot", page_icon="📝", layout="wide")

# 2. Header
st.title("📝 Teacher Copilot: Enterprise Edition")
st.markdown("### Fast, Fair, and *Secure* AI Grading")
st.divider() # Adds a clean horizontal line

# 3. Sidebar for settings
with st.sidebar:
    st.header("⚙️ Configuration")
    rubric_file = st.file_uploader("Upload Grading Rubric (PDF)", type=["pdf"])
    st.info("🔒 All processing is secured with end-to-end PII scrubbing.")

# 4. Create two columns for a professional layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Student Submission")
    submission_text = st.text_area(
        "Paste the student's work below:",
        height=300,
        placeholder="e.g., My name is John and my essay is about..."
    )
    evaluate_btn = st.button("🚀 Evaluate Submission", type="primary", use_container_width=True)

with col2:
    st.subheader("📊 AI Evaluation")
    
    if evaluate_btn:
        if not submission_text:
            st.error("⚠️ Please paste a submission first.")
        else:
            with st.spinner("🔒 Scrubbing PII and analyzing..."):
                # Privacy Layer
                safe_text = scrub_pii(submission_text)
                if safe_text != submission_text:
                    st.toast("🛡️ Student PII successfully removed.")
                
                # Rubric Layer
                rubric_content = extract_text_from_pdf(rubric_file)
                
                # AI Grading
                ai_feedback = grade_submission(safe_text, rubric_text=rubric_content)
                
                st.success("Analysis Complete!")
                # Put the feedback inside a nice visual container
                with st.container(border=True):
                    st.markdown(ai_feedback)