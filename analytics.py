import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# --- INTELLIGENT PATH FINDING ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, 'Master_Data.xlsx')

def calculate_readiness(daily_df):
    if daily_df.empty: return 50, "Unknown"
    today = daily_df.iloc[-1]
    battery = 100
    
    # Penalties
    sleep = today.get('Sleep_Hours', 8)
    if pd.isna(sleep): sleep = 8
    if (8 - sleep) > 0: battery -= ((8 - sleep) * 10)
    screen = today.get('Screen_Time_Phone', 0)
    if pd.isna(screen): screen = 0
    if (screen - 4) > 0: battery -= ((screen - 4) * 5)
    soreness = today.get('Soreness_Level', 0)
    if pd.isna(soreness): soreness = 0
    battery -= (soreness * 5)
    
    score = max(0, min(100, battery))
    if score >= 85: mission = "🔥 GOD MODE"
    elif score >= 60: mission = "🟢 OPTIMAL"
    elif score >= 40: mission = "⚠️ FATIGUED"
    else: mission = "🛑 CRITICAL"
    return score, mission

def analyze_performance():
    print(f"\n🚀 LAUNCHING V10.0 UNIFIED COCKPIT...")
    
    # 1. Load Data
    try:
        daily = pd.read_excel(FILE_PATH, sheet_name='Daily_Log')
        workout = pd.read_excel(FILE_PATH, sheet_name='Workout_Log')
    except Exception as e: print(f"❌ Error: {e}"); return

    # 2. Cleaning & Merging
    daily['Date'] = pd.to_datetime(daily['Date'], dayfirst=True)
    workout['Date'] = pd.to_datetime(workout['Date'], dayfirst=True)
    for col in ['Caffeine_Mg', 'Screen_Time_Phone', 'Soreness_Level']:
        if col in daily.columns: daily[col] = daily[col].fillna(0)
    workout = workout.ffill()
    merged = pd.merge(workout, daily, on='Date', how='inner')
    
    # Calculations
    merged['1RM_Est'] = merged['Weight_KG'] * (1 + merged['Reps'] / 30)
    merged['Volume'] = merged['Weight_KG'] * merged['Reps']
    merged['Day_Name'] = merged['Date'].dt.day_name()

    # --- APEX CALCULATIONS ---
    if len(merged) > 5:
        threshold = merged['Volume'].quantile(0.75)
        apex_days = merged[merged['Volume'] >= threshold].copy()
    else:
        apex_days = merged[merged['Volume'] == merged['Volume'].max()].copy()
    ideal_sleep = apex_days['Sleep_Hours'].mean() if 'Sleep_Hours' in apex_days else 8.0
    ideal_screen = apex_days['Screen_Time_Phone'].mean() if 'Screen_Time_Phone' in apex_days else 2.0
    try: ideal_music = apex_days['Music_Genre'].mode().iloc[0]
    except: ideal_music = "Silence"

    # --- GET STATUS ---
    battery_score, mission_text = calculate_readiness(daily)

    # --- 🏗️ BUILD THE SUPER-GRID (3 Rows x 2 Cols) ---
    fig = make_subplots(
        rows=3, cols=2,
        specs=[
            [{'type': 'domain'}, {'type': 'domain'}], # Row 1: Gauge + Blueprint
            [{'type': 'xy'}, {'type': 'xy'}],         # Row 2: Trend + Streak
            [{'type': 'xy'}, {'type': 'polar'}]       # Row 3: Toxicity + Radar
        ],
        subplot_titles=(
            f"LIVE BATTERY: {mission_text}", "APEX BLUEPRINT (Target Stats)",
            "Strength Trend (1RM)", "Consistency Streak",
            "Digital Toxicity", "Prime Time Detector"
        )
    )

    # 1. SPEEDOMETER (Row 1, Col 1)
    fig.add_trace(go.Indicator(
        mode = "gauge+number", value = battery_score,
        gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "white"},
                 'steps' : [{'range': [0, 40], 'color': "red"}, {'range': [75, 100], 'color': "#00ff00"}],
                 'threshold' : {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 85}}),
        row=1, col=1)

    # 2. BLUEPRINT (Row 1, Col 2)
    # Using a clever "Table" approach for the blueprint to make it readable in the grid
    fig.add_trace(go.Table(
        header=dict(values=['Metric', 'Target', 'Action'], fill_color='grey', align='left'),
        cells=dict(values=[
            ['😴 Sleep', '📱 Screen Limit', '🎧 Audio Fuel'],
            [f"{ideal_sleep:.1f} hrs", f"{ideal_screen:.1f} hrs", ideal_music],
            ['Recover', 'Focus', 'Hype Mode']
        ], fill_color='black', font=dict(color='white'), align='left')),
        row=1, col=2)

    # 3. STRENGTH TREND (Row 2, Col 1)
    fig.add_trace(go.Scatter(x=merged['Date'], y=merged['1RM_Est'], mode='markers', 
                             marker=dict(size=merged['RPE']*1.5, color=merged['Volume'], colorscale='Viridis'),
                             name='Strength'), row=2, col=1)

    # 4. CONSISTENCY (Row 2, Col 2)
    daily_vol = merged.groupby('Date')['Volume'].sum().reset_index()
    fig.add_trace(go.Bar(x=daily_vol['Date'], y=daily_vol['Volume'], name='Volume'), row=2, col=2)

    # 5. TOXICITY (Row 3, Col 1)
    fig.add_trace(go.Scatter(x=merged['Screen_Time_Phone'], y=merged['Sleep_Hours'], mode='markers',
                             marker=dict(size=10, color='red'), name='Bad Habits'), row=3, col=1)

    # 6. RADAR (Row 3, Col 2)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly = merged.groupby('Day_Name')['Volume'].mean().reindex(days).fillna(0).reset_index()
    fig.add_trace(go.Scatterpolar(r=weekly['Volume'], theta=weekly['Day_Name'], fill='toself', name='Energy'), row=3, col=2)

    # --- 🎨 FINAL POLISH ---
    fig.update_layout(height=1000, width=1500, template="plotly_dark", showlegend=False,
                      title_text="<b>🚀 BIO-OPTIMIZATION COMMAND CENTER</b>")
    
    fig.show()
    print("✅ COCKPIT LOADED.")

if __name__ == "__main__":
    analyze_performance()