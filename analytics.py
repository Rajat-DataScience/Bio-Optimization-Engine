import pandas as pd
import plotly.express as px
import os

# --- INTELLIGENT PATH FINDING ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, 'Master_Data.xlsm') # Updated to .xlsm just in case

def analyze_performance():
    print(f"--- 🧠 STARTING BIO-INTELLIGENCE ANALYSIS (V3.0) ---")
    
    # 1. Load Data
    try:
        daily = pd.read_excel(FILE_PATH, sheet_name='Daily_Log')
        workout = pd.read_excel(FILE_PATH, sheet_name='Workout_Log')
    except Exception as e:
        print(f"❌ Error loading Excel: {e}")
        return

    # 2. Smart Cleaning
    daily['Date'] = pd.to_datetime(daily['Date'], dayfirst=True)
    workout['Date'] = pd.to_datetime(workout['Date'], dayfirst=True)
    
    if 'Caffeine_Mg' in daily.columns: daily['Caffeine_Mg'] = daily['Caffeine_Mg'].fillna(0)
    if 'Screen_Time_Phone' in daily.columns: daily['Screen_Time_Phone'] = daily['Screen_Time_Phone'].fillna(0)
    workout = workout.ffill()

    # 3. Merge Tables
    merged = pd.merge(workout, daily, on='Date', how='inner')
    
    if merged.empty:
        print("⚠️ No matching data found! Check dates.")
        return

    # Strength Calculation
    merged['1RM_Est'] = merged['Weight_KG'] * (1 + merged['Reps'] / 30)
    merged['Volume'] = merged['Weight_KG'] * merged['Reps']
    
    # --- 4. GENERATE DASHBOARD ---
    
    # Graph 1: True Strength (The Line of Progress)
    fig1 = px.scatter(merged, x="Date", y="1RM_Est", color="Exercise_Name", trendline="lowess",
                     title="📈 Strength Prediction (1RM Trend)", template="plotly_dark")
    fig1.show()

    # Graph 2: Digital Toxicity (The Bad Habits)
    if 'Screen_Time_Phone' in merged.columns:
        fig2 = px.scatter(merged, x="Screen_Time_Phone", y="Sleep_Hours", color="Physical_Condition",
                        title="📱 Digital Toxicity (Screen Time vs Sleep)", template="plotly_dark")
        fig2.show()

    # Graph 3: Consistency Streak (The Chain) - NEW!
    # Summing up total volume per day to show "Effort Spikes"
    daily_volume = merged.groupby('Date')['Volume'].sum().reset_index()
    fig3 = px.bar(daily_volume, x="Date", y="Volume", 
                 title="📅 Consistency Streak (Don't Break The Chain)", template="plotly_dark")
    fig3.show()

    print("✅ Full Dashboard V3.0 Generated!")
    import time
    time.sleep(5)

if __name__ == "__main__":
    analyze_performance()