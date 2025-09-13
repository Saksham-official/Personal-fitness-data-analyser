import pandas as pd

def analyze_fitness_data(filepath):
    """
    Loads fitness data from a CSV, analyzes it, and generates a report.
    """
    try:
        # Requirement 1: Load fitness data from CSV
        df = pd.read_csv(filepath)

        # --- FIX IS HERE ---
        # 1. Convert the 'Date' column to actual datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        # 2. Set the 'Date' column as the DataFrame's index
        df.set_index('Date', inplace=True)
        # --- END OF FIX ---

    except FileNotFoundError:
        return "Error: The file was not found. Make sure 'fitness_data.csv' is in the same folder."
    except Exception as e:
        return f"An error occurred: {e}"

    # ... the rest of your code continues here ...

def analyze_fitness_data(filepath):
    """
    Loads fitness data from a CSV, analyzes it, and generates a report.
    """
    try:
        # Requirement 1: Load fitness data from CSV
        # We parse the 'Date' column as datetime objects right away.
        df = pd.read_csv(filepath, parse_dates=['Date'])
        # Setting the Date as the index helps with time-based analysis.
        df.set_index('Date', inplace=True)
    except FileNotFoundError:
        return "Error: The file was not found. Make sure 'fitness_data.csv' is in the same folder."
    except Exception as e:
        return f"An error occurred: {e}"

    # --- Calculations ---

    # Requirement 2: Calculate daily/weekly/monthly averages
    daily_avg = df.mean()
    # 'W' stands for weekly frequency. We calculate the mean for each week.
    weekly_avg = df.resample('W').mean()
    # 'M' stands for monthly frequency.
    monthly_avg = df.resample('M').mean()

    # Requirement 3: Find best and worst days for each metric
    best_day_steps = df['Steps'].idxmax()
    worst_day_steps = df['Steps'].idxmin()
    best_day_sleep = df['SleepHours'].idxmax()
    worst_day_sleep = df['SleepHours'].idxmin()

    # Requirement 4: Identify trends over time using a 7-day rolling average
    # This smooths out daily fluctuations to show the underlying trend.
    df['Steps_7_day_avg'] = df['Steps'].rolling(window=7).mean()
    
    # Check the trend in the last week
    last_week_trend_start = df['Steps_7_day_avg'].iloc[-7]
    last_week_trend_end = df['Steps_7_day_avg'].iloc[-1]
    trend_direction = "upward" if last_week_trend_end > last_week_trend_start else "downward"

    # --- Report Generation ---

    # Requirement 5: Create a simple report with recommendations
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

    # Add recommendations based on the data
    if daily_avg['Steps'] < 7000:
        report += "- Your average daily steps are a bit low. Try incorporating a short walk into your daily routine.\n"
    else:
        report += "- You're doing great with your daily steps. Keep up the consistency!\n"

    if daily_avg['SleepHours'] < 7:
        report += "- Your average sleep is below the recommended 7-8 hours. Prioritizing sleep can boost your energy.\n"
    else:
        report += "- Excellent! You're getting a healthy amount of sleep on average.\n"

    return report

# --- Main execution block ---
if __name__ == "__main__":
    # The name of your data file
    csv_file = 'fitness_data.csv'
    # Generate the report by calling the function
    analysis_report = analyze_fitness_data(csv_file)
    # Print the final report to the console
    print(analysis_report)
    
    # Optionally, save the report to a text file
    with open('fitness_report.txt', 'w') as f:
        f.write(analysis_report)
    print("\nReport has also been saved to 'fitness_report.txt'")