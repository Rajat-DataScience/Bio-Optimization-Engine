import pandas as pd
import plotly.express as px
import os

# --- INTELLIGENT PATH FINDING ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, 'Master_Data.xlsx')

def analyze_performance():
    print(f"--- 🧠 STARTING BIO-INTELLIGENCE ANALYSIS (V2.0) ---")
    
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
    
    # Clean Missing Data
    if 'Caffeine_Mg' in daily.columns: daily['Caffeine_Mg'] = daily['Caffeine_Mg'].fillna(0)
    if 'Screen_Time_Phone' in daily.columns: daily['Screen_Time_Phone'] = daily['Screen_Time_Phone'].fillna(0)
    workout = workout.ffill()

    # 3. Merge Tables
    merged = pd.merge(workout, daily, on='Date', how='inner')
    
    if merged.empty:
        print("⚠️ No matching data found! Check dates.")
        return

    # --- THE UPGRADE: 1RM CALCULATION (Epley Formula) ---
    # 1RM = Weight * (1 + Reps/30)
    merged['1RM_Est'] = merged['Weight_KG'] * (1 + merged['Reps'] / 30)
    merged['Volume'] = merged['Weight_KG'] * merged['Reps']
    
    print(f"✅ Calculated Strength Metrics for {len(merged)} sets.")

    # --- 4. NEW DASHBOARD ---
    
    # Graph 1: The "True Strength" Trend (New!)
    # This shows your theoretical max strength rising over time
    fig1 = px.scatter(merged, x="Date", y="1RM_Est", color="Exercise_Name", size="RPE",
                     title="📈 True Strength Trend (Estimated 1RM)", template="plotly_dark")
    fig1.show()

    # Graph 2: Screen Time vs Recovery
    if 'Screen_Time_Phone' in merged.columns:
        fig2 = px.scatter(merged, x="Screen_Time_Phone", y="Sleep_Hours", size="Caffeine_Mg", color="Physical_Condition",
                        title="📱 Digital Toxicity Analysis", template="plotly_dark")
        fig2.show()

    print("✅ Dashboard V2.0 Generated!")
    import time
    time.sleep(5)

if __name__ == "__main__":
    analyze_performance()