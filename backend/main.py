from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import glob
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# 1. API Key Load aur GenAI Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# 2. Automatically latest trained model dhundo
try:
    model_files = glob.glob("xgboost_netguard_v1_*.pkl")
    latest_model = max(model_files, key=os.path.getctime)
    model = joblib.load(latest_model)
    print(f"✅ Loaded latest model: {latest_model}")
except:
    print("❌ Model not found!")
    model = None

# 3. Data Structures (Security aur Validation ke liye)
class NetworkData(BaseModel):
    location: int
    event_type_1: int
    event_type_2: int
    event_type_3: int
    event_type_4: int
    event_type_5: int

class CopilotRequest(BaseModel):
    role: str  # "L1 Engineer" or "NOC Manager"
    fault_severity: int
    location: str

@app.get("/")
def read_root():
    return {"message": "NetGuard AI Backend & Copilot is Running! 🚀"}

# --- MACHINE LEARNING ENDPOINT ---
@app.post("/predict")
def predict(data: NetworkData):
    df = pd.DataFrame([data.dict()])
    prediction = model.predict(df)
    probability = model.predict_proba(df).tolist()
    return {
        "fault_severity": int(prediction[0]),
        "confidence": round(max(probability[0]) * 100, 2)
    }

# --- GEN AI COPILOT ENDPOINT (THE MASTERPIECE) ---
@app.post("/copilot")
def copilot_action(request: CopilotRequest):
    # DYNAMIC PROMPT ENGINEERING (Multi-Persona)
    prompt = f"""
    You are NetGuard AI, an enterprise telecom network assistant.
    A network fault has been detected.
    - Fault Severity: {request.fault_severity} (0=Normal, 1=Warning, 2=Critical)
    - Location: {request.location}
    - User Role: {request.role}

    If the User Role is 'L1 Engineer', provide highly technical, step-by-step hardware/software troubleshooting steps (e.g., reroute traffic, reboot optical switch).
    If the User Role is 'NOC Manager', provide the business impact, SLA violation risks, and estimated downtime cost.

    IMPORTANT: You MUST respond in pure JSON format exactly like this, so the frontend can render it as action buttons:
    {{
        "analysis": "Brief 2-line explanation",
        "actions": [
            {{"label": "Action 1 Name", "command": "backend_system_command_1"}},
            {{"label": "Action 2 Name", "command": "backend_system_command_2"}}
        ]
    }}
    """
    
    try:
        # Calling Gemini 1.5 Flash (Super fast for Hackathons)
        ai_model = genai.GenerativeModel('gemini-3.6-flash')
        response = ai_model.generate_content(prompt)
        
        # Cleaning the response to ensure it's valid JSON
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    
    except Exception as e:
        return {"error": "AI Copilot Error", "details": str(e)}