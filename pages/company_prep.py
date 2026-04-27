import streamlit as st
import json
import os

st.sidebar.markdown("🏢Company Prep")

def load_company_data():
    # Since this is in the 'pages' folder, we look directly for the file
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "company_questions.json")
    with open(file_path, "r") as f:
        return json.load(f)

def run():
    st.title("🏢 Company-Specific Interview Prep")
    
    # Custom CSS for a better button look
    st.markdown("""
        <style>
        .stLinkButton { text-align: center; }
        </style>
        """, unsafe_allow_html=True)

    data = load_company_data()
    
    # 1. Company Selection Box
    company_name = st.selectbox("Select Target Company", list(data.keys()))
    
    if company_name:
        # Access the company object
        company_details = data[company_name]
        
        # Display Company Header
        st.subheader(f"Preparing for {company_name}")
        
        # 2. Display the main Career Link for the company
        if "career_link" in company_details:
            st.link_button(f"🚀 Visit {company_name} Career Portal", company_details["career_link"], use_container_width=True)
        
        st.info(f"Focus: {company_name} typically emphasizes technical fundamentals and communication skills.")
        st.divider()
        
        st.write("#### Frequently Asked Questions")

        # 3. Display the Questions list
        # Accessing the "questions" list inside the company object
        for item in company_details["questions"]:
            with st.expander(f"📌 {item['question']}"):
                # Check for 'type' (Optional check in case it's missing in some JSON entries)
                if "type" in item:
                    st.write(f"**Category:** {item['type']}")
                
                st.write("**Key Concepts to Mention:**")
                st.code(", ".join(item['keywords']))
                
                # 4. Display the individual 'Learn More' link for the specific question
                if "link" in item:
                    st.link_button("📖 Learn More", item["link"])

if __name__ == "__main__":
    run()