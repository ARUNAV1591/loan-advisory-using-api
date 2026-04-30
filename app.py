import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI Personal Loan Advisor",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for a better, more presentable look
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        padding: 10px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏦 AI Personal Loan Advisor")
st.markdown("### Welcome to Your Intelligent Financial Guide")
st.write("Discover the best loan options tailored perfectly to your credit profile using advanced AI analysis.")
st.divider()

# ==========================================
# API KEY SETUP
# ==========================================
# Automatically try to get the API key from the .env file
api_key = os.getenv("GEMINI_API_KEY")

st.sidebar.header("⚙️ Settings")
if not api_key:
    # Fallback to manual entry if .env fails or isn't present
    api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")
else:
    st.sidebar.success("✅ API Key Loaded Securely")

st.sidebar.markdown("---")
st.sidebar.info("This project is designed to strictly act as a Personal Loan Advisor. It will not answer questions outside of its domain.")

if api_key:
    genai.configure(api_key=api_key)
    
    # ==========================================
    # MOCK DATABASE / API
    # ==========================================
    loan_products = [
        {"bank": "Apex Bank", "min_credit_score": 750, "interest_rate": "8.5%", "max_amount": 50000},
        {"bank": "Global Trust", "min_credit_score": 700, "interest_rate": "9.2%", "max_amount": 40000},
        {"bank": "Secure Finance", "min_credit_score": 650, "interest_rate": "10.5%", "max_amount": 25000},
        {"bank": "Quick Loans", "min_credit_score": 600, "interest_rate": "12.0%", "max_amount": 10000},
        {"bank": "Elite Wealth", "min_credit_score": 800, "interest_rate": "7.9%", "max_amount": 100000},
    ]

    # ==========================================
    # USER INPUTS (FRONTEND)
    # ==========================================
    st.subheader("👤 Your Financial Profile")
    
    # Using columns for a cleaner layout
    col1, col2 = st.columns(2)
    with col1:
        credit_score = st.number_input("Credit Score (300-850):", min_value=300, max_value=850, value=720, step=10)
    with col2:
        requested_amount = st.number_input("Requested Amount ($):", min_value=1000, max_value=200000, value=15000, step=1000)

    st.markdown("<br>", unsafe_allow_html=True) # Adding some spacing

    if st.button("🔍 Get Personalized Loan Advice"):
        with st.spinner("🤖 AI is analyzing your profile against market rates..."):
            
            # ==========================================
            # PROMPT ENGINEERING (BACKEND LOGIC)
            # ==========================================
            system_prompt = """
            Role: You are a specialized AI Personal Loan Advisor. Your expertise is limited exclusively to analyzing credit scores and recommending the best available loan options from the provided data.

            Strict Operational Rules:
            1. Domain Restriction: You must NOT respond to any queries outside of personal loan advice. If the user asks about general knowledge, sports, coding, or any unrelated topic, reply: "I am specialized only in personal loan advisory and cannot assist with that request."
            2. Data Integrity: Only suggest loans for which the user meets the minimum credit score requirement.
            3. Personalization: Rank the suggestions by the lowest Interest Rate first. Explain why a specific loan is the best fit for their score.
            4. Tone: Maintain a professional, helpful, and transparent financial tone.

            Output Format:
            - Summary: A brief overview of eligibility.
            - Top Recommendations: A bulleted list of specific loan products.
            - Next Steps: Advice on how to improve their chances of approval.
            """

            user_prompt = f"""
            User Profile:
            - Credit Score: {credit_score}
            - Requested Amount: ${requested_amount}

            Available Loan Products (API Data):
            {loan_products}

            Please provide the loan advice based on the system prompt and operational rules. Use clean Markdown formatting.
            """

            try:
                # We use gemini-flash-latest as it's the fastest and best model for general tasks
                model = genai.GenerativeModel('gemini-flash-latest', system_instruction=system_prompt)
                
                response = model.generate_content(user_prompt)
                
                # ==========================================
                # DISPLAY RESULTS (FRONTEND)
                # ==========================================
                st.success("✅ Analysis Complete!")
                
                # Wrapping results in a visually distinct container
                st.markdown("---")
                st.markdown("### 📊 Advisor's Recommendations")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred while generating advice: {e}")
else:
    st.warning("⚠️ Please provide a Google Gemini API Key to continue.")
