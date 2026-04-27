import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
from utils import get_sentiment_score, calculate_skill_impact

# --- PAGE CONFIG ---
st.set_page_config(page_title="Smart Interview Analyzer", page_icon="🎯", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00dbde, #fc00ff);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #00dbde;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ASSETS ---
#def load_lottieurl(url):
 #   try:
  #      r = requests.get(url)
   #     if r.status_code != 200: return None
    #    return r.json()
    #except:
     #6   return None

#lottie_ai = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_m9p9i62y.json")

# --- APP HEADER ---
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🎯Smart Interview Performance Analyzer")
        st.subheader("Predicting your success with Machine Learning & NLP")
        st.write("Enter your credentials below to get a data-driven placement report.")
    with col2:
       # if lottie_ai:
            #st_lottie(lottie_ai, height=200, key="coding")
        #else:
            st.write("🚀")

st.divider()

# --- INPUT SECTION ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🎓 Academics")
    ssc = st.number_input("SSC CGPA", 0.0, 10.0, 8.5)
    hsc = st.number_input("12th CGPA", 0.0, 10.0, 8.0)
    btech = st.number_input("B.Tech CGPA", 0.0, 10.0, 7.5)

with col2:
    st.markdown("### 💻 Technical")
    dsa = st.slider("DSA Proficiency", 1, 10, 5)
    apti = st.slider("Aptitude Score", 1, 10, 5)
    coding = st.select_slider("Coding Platform Rating", options=[1, 2, 3, 4, 5])

with col3:
    st.markdown("### 💼 Experience")
    work_exp = st.selectbox("Internship / Work Exp?", ["No", "Yes"])
    work_exp = 1 if work_exp == "Yes" else 0
    user_bio = st.text_area("Tell us about your skills & confidence...", placeholder="I am proficient in Python and very confident...")

st.markdown('</div>', unsafe_allow_html=True)

# --- ANALYSIS LOGIC ---
if st.button("🚀 GENERATE PERFORMANCE REPORT"):
    with st.spinner("AI is analyzing your profile..."):
        time.sleep(2) 

        # 1. NLP Extraction
        sentiment = get_sentiment_score(user_bio)
        skill_impact, found_skills = calculate_skill_impact(user_bio)

        # 2. Load Model snd Predict
        try:
            with open("model.pkl", "rb") as f:
                model = pickle.load(f)
            features = np.array([[ssc, hsc, btech, work_exp, dsa, apti, coding, sentiment, skill_impact]])
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0][1]
        except Exception as e:
            st.error(f"Error: {e}. Please ensure model.pkl exists.")
            st.stop()

        # --- RESULTS DISPLAYINg ---
        st.divider()
        res_col1, res_col2 = st.columns([1, 1])

        with res_col1:
            st.markdown("## 📊 Readiness Score")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = probability * 100,
                title = {'text': "Placement Probability %"},
                gauge = {'axis': {'range': [None, 100]},
                         'bar': {'color': "#00dbde"},
                         'steps' : [
                             {'range': [0, 50], 'color': "#ff4b4b"},
                             {'range': [50, 80], 'color': "#ffa500"},
                             {'range': [80, 100], 'color': "#00ff00"}]}))
            st.plotly_chart(fig, use_container_width=True)

        with res_col2:
            st.markdown("## Insights")
            if prediction == 1:
                st.success("🔥 **HIGH CHANCE:** You are likely to clear the interview!")
            else:
                st.warning("⚠️ **IMPROVEMENT NEEDED:** Work on the suggested areas.")

            st.write(f"**Confidence Level:** {sentiment}")
            st.write(f"**Identified Skills:** {', '.join(found_skills) if found_skills else 'None detected, you might need some other than DSA for some roles'}")

            categories = ['Academics', 'DSA', 'Aptitude', 'Coding', 'Soft Skills']
            values = [btech, dsa, apti, coding*2, (sentiment+1)*5]

            fig_radar = px.line_polar(r=values, theta=categories, line_close=True)
            fig_radar.update_traces(fill='toself')
            st.plotly_chart(fig_radar, use_container_width=True)

        # --- RECOMMENDATION ENGINE ---
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📌 Personalized Suggestions")
        if btech < 7.5: st.write("- 📘 **Academia:** Your B.Tech CGPA is slightly low. Focus on core subjects.")
        if dsa < 6: st.write("- 💻 **Technical:** Practice LeetCode Easy/Medium problems daily.")
        if sentiment < 0.2: st.write("- 🗣️ **Soft Skills:** Use more positive and assertive words in your bio.")
        if skill_impact < 5: st.write("- 🛠️ **Skills:** Learn a high-demand tech like AWS or React.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- DOWNLOAD REPORT ---
        report_text = f"""
        Smart Interview Performance Report
        ----------------------------------
        Placement Probability: {probability * 100:.2f}%
        Sentiment Score: {sentiment}
        Skills Found: {', '.join(found_skills)}
        Result: {'Selected' if prediction == 1 else 'Needs Improvement'}
        """

        st.download_button(
            label="📥 Download Performance Report",
            data=report_text,
            file_name="Interview_Report.txt",
            mime="text/plain"
        )