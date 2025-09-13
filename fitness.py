import pandas as pd

def analyze_fitness_data(filepath):
    """
    Loads fitness data from a CSV, analyzes it, and generates a report.
    """
    try:
       
        df = pd.read_csv(filepath)

      
        df['Date'] = pd.to_datetime(df['Date'])
       
        df.set_index('Date', inplace=True)
        

    except FileNotFoundError:
        return "Error: The file was not found. Make sure 'fitness_data.csv' is in the same folder."
    except Exception as e:
        return f"An error occurred: {e}"

  

def analyze_fitness_data(filepath):
    """
    Loads fitness data from a CSV, analyzes it, and generates a report.
    """
    try:
      
        df = pd.read_csv(filepath, parse_dates=['Date'])
       
        df.set_index('Date', inplace=True)
    except FileNotFoundError:
        return "Error: The file was not found. Make sure 'fitness_data.csv' is in the same folder."
    except Exception as e:
        return f"An error occurred: {e}"

  
    daily_avg = df.mean()
    weekly_avg = df.resample('W').mean()
    monthly_avg = df.resample('M').mean()

    best_day_steps = df['Steps'].idxmax()
    worst_day_steps = df['Steps'].idxmin()
    best_day_sleep = df['SleepHours'].idxmax()
    worst_day_sleep = df['SleepHours'].idxmin()

    
    df['Steps_7_day_avg'] = df['Steps'].rolling(window=7).mean()
    
    last_week_trend_start = df['Steps_7_day_avg'].iloc[-7]
    last_week_trend_end = df['Steps_7_day_avg'].iloc[-1]
    trend_direction = "upward" if last_week_trend_end > last_week_trend_start else "downward"

  
    report = f"""
========================================
    Your Fitness Analysis Report
========================================

--- Overall Averages ---
Average Daily Steps: {daily_avg['Steps']:.0f}
Average Daily Sleep: {daily_avg['SleepHours']:.1f} hours
Average Daily Workout: {daily_avg['WorkoutDurationMinutes']:.0f} mins

--- Performance Highlights ---
Best Day for Steps: {best_day_steps.strftime('%Y-%m-%d')} ({df.loc[best_day_steps, 'Steps']} steps)
Worst Day for Steps: {worst_day_steps.strftime('%Y-%m-%d')} ({df.loc[worst_day_steps, 'Steps']} steps)

Best Night's Sleep: {best_day_sleep.strftime('%Y-%m-%d')} ({df.loc[best_day_sleep, 'SleepHours']:.1f} hours)
Worst Night's Sleep: {worst_day_sleep.strftime('%Y-%m-%d')} ({df.loc[worst_day_sleep, 'SleepHours']:.1f} hours)

--- Trends Over Time ---
Your 7-day step average shows a recent **{trend_direction}** trend.
The rolling average on your last recorded day was {last_week_trend_end:.0f} steps.

========================================
    Recommendations 💡
========================================
"""

    if daily_avg['Steps'] < 7000:
        report += "- Your average daily steps are a bit low. Try incorporating a short walk into your daily routine.\n"
    else:
        report += "- You're doing great with your daily steps. Keep up the consistency!\n"

    if daily_avg['SleepHours'] < 7:
        report += "- Your average sleep is below the recommended 7-8 hours. Prioritizing sleep can boost your energy.\n"
    else:
        report += "- Excellent! You're getting a healthy amount of sleep on average.\n"

    return report

if __name__ == "__main__":
    csv_file = 'fitness_data.csv'
    analysis_report = analyze_fitness_data(csv_file)
    print(analysis_report)
    
    with open('fitness_report.txt', 'w') as f:
        f.write(analysis_report)

    print("\nReport has also been saved to 'fitness_report.txt'")
