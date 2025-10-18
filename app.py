import streamlit as st
import pandas as pd
import google.generativeai as genai
import matplotlib.pyplot as plt

# --- DATA PROCESSING FUNCTIONS ---

def load_data(file):
    df = pd.read_csv(file, parse_dates=['Date'])
    df.sort_values('Date', inplace=True)
    return df

def calculate_averages(df):
    daily_avg = df[['Steps', 'SleepHours', 'WorkoutMinutes']].mean()
    return daily_avg

def best_and_worst_days(df):
    best_steps = df.loc[df['Steps'].idxmax()]
    worst_steps = df.loc[df['Steps'].idxmin()]
    best_sleep = df.loc[df['SleepHours'].idxmax()]
    worst_sleep = df.loc[df['SleepHours'].idxmin()]
    return best_steps, worst_steps, best_sleep, worst_sleep

def find_trends(df):
    weekly_avg = df.resample('W', on='Date')[['Steps', 'SleepHours', 'WorkoutMinutes']].mean()
    trend = weekly_avg.diff().mean()
    return trend

# --- AI REPORT GENERATION ---

def generate_ai_report(df, gemini_api_key):
    try:
        genai.configure(api_key = gemini_api_key)
    except Exception as e:
        return "API Key Error", f"There was an issue configuring the API key: {e}"

    daily_avg = calculate_averages(df)
    best_steps, worst_steps, best_sleep, worst_sleep = best_and_worst_days(df)
    trend = find_trends(df)

    summary = f"""
    **Average Daily Performance:**
    - Steps: {daily_avg['Steps']:.0f}
    - Sleep: {daily_avg['SleepHours']:.1f} hrs
    - Workout: {daily_avg['WorkoutMinutes']:.1f} mins
    **Best Days:**
    - Steps: {best_steps['Date'].date()} ({best_steps['Steps']} steps)
    - Sleep: {best_sleep['Date'].date()} ({best_sleep['SleepHours']} hrs)
    **Worst Days:**
    - Steps: {worst_steps['Date'].date()} ({worst_steps['Steps']} steps)
    - Sleep: {worst_sleep['Date'].date()} ({worst_sleep['SleepHours']} hrs)
    **Trends (weekly average change):**
    - Steps trend: {trend['Steps']:.2f}
    - Sleep trend: {trend['SleepHours']:.2f}
    - Workout trend: {trend['WorkoutMinutes']:.2f}
    """

    prompt = f"You are a fitness coach. Analyze this summary and provide actionable recommendations:\n\n{summary}"

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # Updated model
        response = model.generate_content(prompt)
        ai_recommendations = response.candidates[0].content.parts[0].text

    except Exception as e:
        ai_recommendations = f"⚠️ **Error generating AI insights:** {e}"

    return summary, ai_recommendations

# --- STREAMLIT UI ---

st.set_page_config(page_title="AI Fitness Analyzer", page_icon="🏋️", layout="wide")
st.title("🏋️ AI Fitness Data Analyzer")

with st.sidebar:
    st.header("⚙️ Your Inputs")
    uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    daily_avg = calculate_averages(df)

    st.subheader("🚀 At-a-Glance")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg. Steps", f"{daily_avg['Steps']:.0f}")
    col2.metric("Avg. Sleep", f"{daily_avg['SleepHours']:.1f} hrs")
    col3.metric("Avg. Workout", f"{daily_avg['WorkoutMinutes']:.1f} mins")
    st.divider()

    with st.spinner("🤖 AI is analyzing..."):
        summary, recommendations = generate_ai_report(df, st.secrets["GOOGLE_API_KEY"])

    tab1, tab2, tab3 = st.tabs(["💡 AI Analysis", "📊 Visualizations", "📄 Raw Data"])
    with tab1:
        st.markdown(recommendations)
    with tab2:
        st.subheader("📈 Trends Over Time")
        st.line_chart(df.set_index('Date')[['Steps', 'SleepHours']])
        st.bar_chart(df.set_index('Date')['WorkoutMinutes'])
    with tab3:
        st.dataframe(df)
else:
    st.info("👋 Welcome! Please upload a CSV file to begin.")