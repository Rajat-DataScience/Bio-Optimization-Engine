import pandas as pd
import plotly.express as px
import os

# --- INTELLIGENT PATH FINDING ---
# This forces Python to look in the same folder as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, 'Master_Data.xlsx')

def analyze_performance():
    print(f"--- 🧠 STARTING BIO-INTELLIGENCE ANALYSIS ---")
    print(f"📂 Looking for data in: {FILE_PATH}")
    
    # 1. Load Data
    try:
        daily = pd.read_excel(FILE_PATH, sheet_name='Daily_Log')
        workout = pd.read_excel(FILE_PATH, sheet_name='Workout_Log')
    except FileNotFoundError:
        print("❌ ERROR: Could not find 'Master_Data.xlsx'.")
        print("👉 Make sure the Excel file is in the SAME folder as this python script.")
        input("Press Enter to close...")
        return
    except Exception as e:
        print(f"❌ Error loading Excel: {e}")
        input("Press Enter to close...")
        return

    # 2. Smart Cleaning & Merging
    daily['Date'] = pd.to_datetime(daily['Date'], dayfirst=True)
    workout['Date'] = pd.to_datetime(workout['Date'], dayfirst=True)
    
    # Clean Daily Log
    if 'Caffeine_Mg' in daily.columns:
        daily['Caffeine_Mg'] = daily['Caffeine_Mg'].fillna(0)
    if 'Screen_Time_Phone' in daily.columns:
        daily['Screen_Time_Phone'] = daily['Screen_Time_Phone'].fillna(0)

    # Clean Workout Log
    workout = workout.ffill()
    if 'Pre_Workout' in workout.columns:
        workout['Pre_Workout'] = workout['Pre_Workout'].fillna('No')
    if 'Gym_Crowd_Level' in workout.columns:
        workout['Gym_Crowd_Level'] = workout['Gym_Crowd_Level'].fillna(1)

    # 3. Merge Tables
    merged = pd.merge(workout, daily, on='Date', how='inner')
    
    if merged.empty:
        print("⚠️ No matching data found! Check that dates match in both sheets.")
        input("Press Enter to close...")
        return

    # Calculate Volume
    merged['Volume'] = merged['Weight_KG'] * merged['Reps']
    print(f"✅ Analyzed {len(merged)} sets.")

    # --- 4. GENERATE DASHBOARD ---
    
    # Graph 1: Screen Time vs Strength
    if 'Screen_Time_Phone' in merged.columns:
        fig1 = px.scatter(merged, x="Screen_Time_Phone", y="Volume", size="RPE", color="Physical_Condition",
                        title="📱 Digital Toxicity: Screen Time vs Strength", template="plotly_dark")
        fig1.show()

    # Graph 2: Environment
    if 'Gym_Crowd_Level' in merged.columns:
        fig2 = px.box(merged, x="Gym_Crowd_Level", y="RPE", color="Music_Genre",
                    title="🎧 Environment Check: Crowd & Music", template="plotly_dark")
        fig2.show()

    # Graph 3: Recovery
    if 'Sleep_Hours' in merged.columns:
        fig3 = px.scatter(merged, x="Sleep_Hours", y="Volume", color="Physical_Condition", 
                        title="🔋 The Recovery Matrix", template="plotly_dark")
        fig3.show()

    print("✅ Dashboard Generated! Check your browser.")
    # Keep window open for 5 seconds so you can see success
    import time
    time.sleep(5)

if __name__ == "__main__":
    analyze_performance()