import streamlit as st
import json
import os
import random
st.sidebar.markdown("📚Subject prep")


def load_questions():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "questions.json")
    
    with open(file_path, "r") as f:
        return json.load(f)

def run_mock():
    st.title("Technical Mock Interview")
    
    # Load data from JSON
    data = load_questions()
    
    # Subject Selection
    subject = st.selectbox("Select Subject", list(data.keys()))
    
    # Get the list of questions for the selected subject
    question_list = data[subject]
    
    # Use Session State to keep the question consistent across re-renders 
    # unless the user wants a new one
    if 'current_q_obj' not in st.session_state or st.button("🔄 Get Different Question"):
        st.session_state.current_q_obj = random.choice(question_list)
    
    q_obj = st.session_state.current_q_obj
    current_q = q_obj["question"]
    keywords = q_obj["keywords"]
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #00dbde;">
        <h4 style="margin:0;">Current Question:</h4>
        <p style="font-size: 18px;">{current_q}</p>
    </div>
    """, unsafe_allow_html=True)

    # User Input
    user_answer = st.text_area("Your Response:", height=200, placeholder="Explain the concept using technical terms...")

    if st.button("Submit for Evaluation"):
        if user_answer.strip() == "":
            st.warning("Please provide an answer before submitting.")
        else:
            with st.spinner("Analyzing your technical response..."):
                # Evaluation Logic
                found_keywords = [k for k in keywords if k.lower() in user_answer.lower()]
                score_pct = len(found_keywords) / len(keywords)

                st.divider()
                st.subheader("Analysis Result")
                
                if score_pct >= 0.7:
                    st.success("🎯 **Verdict: Excellent**")
                    st.write("Your answer covers almost all core technical aspects. Great depth!")
                elif score_pct >= 0.2:
                    st.warning("⚖️ **Verdict: Good / Average**")
                    st.write("You have a decent grasp of the concept, but try to include more specific technical terminology.")
                else:
                    st.error("⚠️ **Verdict: Needs Improvement**")
                    st.write("Your answer is missing critical technical keywords. Review the fundamental concepts.")

                with st.expander("View Identified Keywords"):
                    st.write(f"Keywords detected: {', '.join(found_keywords) if found_keywords else 'None'}")
                    st.write(f"Keywords missed: {', '.join([k for k in keywords if k not in found_keywords])}")

if __name__ == "__main__":
    run_mock()