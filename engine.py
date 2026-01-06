import pandas as pd
import os

# --- 1. CONFIGURATION ---
FILE_PATH = 'Master_Data.xlsx'

def check_system():
    print("--- 🚀 STARTING BIO-OPTIMIZATION ENGINE ---")
    
    # A. Check if file exists
    if not os.path.exists(FILE_PATH):
        print(f"❌ ERROR: I cannot find '{FILE_PATH}'")
        print("   -> Make sure the Excel file is inside the 'Project_BioAlgorithm' folder!")
        return
    
    print("✅ CONNECTION: Excel file found.")

    # B. Try to load the 'Workout_Log'
    try:
        # We assume headers are in Row 0 (default)
        df_workout = pd.read_excel(FILE_PATH, sheet_name='Workout_Log')
        
        # Check if new columns exist
        if 'Set_Number' in df_workout.columns:
            print("✅ SCHEMA CHECK: 'Set_Number' column found.")
        else:
            print("⚠️ WARNING: I don't see the 'Set_Number' column. Did you save the Excel?")

        print(f"\n--- 📊 DATA PREVIEW (First 5 Rows) ---")
        print(df_workout[['Date', 'Exercise_Name', 'Set_Number', 'Weight_KG']].head())
        
        print("\n✅ SYSTEM STATUS: READY FOR REAL DATA.")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        print("   -> Hint: Is the Excel file still open? CLOSE IT!")

# --- 2. EXECUTE ---
if __name__ == "__main__":
    check_system()