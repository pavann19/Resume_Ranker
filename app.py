import streamlit as st
from ranker import calculate_similarity, extract_keywords, generate_resume_suggestions
from utils import extract_text_from_pdf, match_skills, draw_pie_chart
from user_auth import login_signup, save_history, get_resume_history

# Must be first Streamlit command
st.set_page_config(page_title="Multi-Resume NLP Ranker", layout="centered")

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# If not logged in, show login/signup and stop app execution
if not st.session_state.logged_in:
    login_signup()
    st.stop()

# Main UI after login
st.title("🎯 Resume Ranking Portal")

selected_page = st.radio(
    "Choose an option:",
    ["📤 Upload New Resumes & Get Scores", "📜 View Resume History"],
    horizontal=True
)

if selected_page == "📤 Upload New Resumes & Get Scores":
    uploaded_resumes = st.file_uploader("📄 Upload Multiple Resumes (PDF)", type=["pdf"], accept_multiple_files=True)
    jd_text = st.text_area("📝 Paste Job Description Text Here", height=250)

    if st.button("📊 Rank All Resumes"):
        if uploaded_resumes and jd_text.strip():
            rankings = []
            jd_keywords = extract_keywords(jd_text)

            for resume in uploaded_resumes:
                resume_text = extract_text_from_pdf(resume)
                score = calculate_similarity(resume_text, jd_text)
                resume_keywords = extract_keywords(resume_text)
                matched, _ = match_skills(resume_keywords, jd_keywords)
                suggestions = generate_resume_suggestions(resume_text, jd_text)

                rankings.append({
                    "name": resume.name,
                    "score": score,
                    "matched_skills": matched,
                    "matched_count": len(matched),
                    "suggestions": suggestions
                })

                resume_data = {
                    "resume_name": resume.name,
                    "score": score,
                    "matched_skills": matched,
                    "suggestions": suggestions
                }
                save_history(st.session_state.username, resume_data)

            rankings.sort(key=lambda x: x["score"], reverse=True)

            st.subheader("🏆 Resume Ranking Results")
            for idx, res in enumerate(rankings):
                st.markdown(f"### {idx+1}. {res['name']}")
                st.write(f"🔢 **Match Score:** {res['score']}%")
                st.write(f"✅ **Matched Skills:** {res['matched_skills']}")
                st.write(f"📝 **Suggestions:** {res['suggestions']}")
                draw_pie_chart(len(res['matched_skills']), len(jd_keywords) - len(res['matched_skills']))
                st.markdown("---")
        else:
            st.warning("Please upload resumes and paste a job description.")

elif selected_page == "📜 View Resume History":
    st.subheader("Your Resume History")
    history = get_resume_history(st.session_state.username)
    if history:
        for entry in history:
            st.write(f"**{entry['resume_name']}**: Match Score - {entry['score']}%")
            st.write(f"Suggestions: {entry['suggestions']}")
            st.write(f"Matched Skills: {entry['matched_skills']}")
            st.markdown("---")
    else:
        st.info("No resume history found.")
