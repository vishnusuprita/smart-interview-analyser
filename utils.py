from textblob import TextBlob
import re

def get_sentiment_score(user_text):
    if not user_text.strip(): return 0.0
    return round(TextBlob(user_text).sentiment.polarity, 2)

def calculate_skill_impact(user_text):
    skills_library = {
        "High Impact": ["python", "machine learning","java", "dsa", "react", "aws", "docker", "sql","cloud","flutter"],
        "Medium Impact": [ "c++", "html", "css", "javascript", "php", "excel"],
    }
    score, found_skills = 0, []
    text_lower = user_text.lower()
    for category, skills in skills_library.items():
        for skill in skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill)
                score += 2 if category == "High Impact" else 1
    return min(score, 10), found_skills