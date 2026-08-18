import os
import glob
import json
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
# import time  

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()
model = None

# load latest model 
try:
    model_files= glob.glob("xgboost_netguard_v2_*.pkl")
    if len(model_files) > 0:
        latest_model = max(model_files, key=os.path.getctime)
        model = joblib.load(latest_model)
        print("INFO: loaded model ->", latest_model)
    else:
        print("warning: no v2 model found")
except Exception as e:
    print("model load error:", e)


class NetworkData(BaseModel):
    location: int
    severity_type: int
    num_events: int
    num_resources : int
    total_log_volume: int

class CopilotRequest(BaseModel):
    role: str
    fault_severity: int
    location: str

@app.get("/")
def health_check():
    return {"status": "active", "version":"v2", "service": "NetGuard API running"}

@app.post("/predict")
def predict_severity(data: NetworkData):
    if model is None:
        return {"error":"model not loaded"}
        
    df = pd.DataFrame([data.dict()])
    
    prediction= model.predict(df)
    prob = model.predict_proba(df).tolist()
    
    return {
        "fault_severity": int(prediction[0]),
        "confidence": round(max(prob[0]) * 100, 2)
    }


@app.post("/copilot")
def copilot_action(request: CopilotRequest):
    
    prompt = f"""
    You are NetGuard AI, an enterprise telecom network assistant.
    A network fault has been detected.
    - Fault Severity: {request.fault_severity} (0=Normal, 1=Warning, 2=Critical)
    - Location: Node {request.location}
    - User Role: {request.role}

    If the User Role is 'L1 Engineer', provide highly technical, step-by-step hardware/software troubleshooting steps (e.g., reroute traffic, reboot optical switch).
    If the User Role is 'NOC Manager', provide the business impact, SLA violation risks, and estimated downtime cost.

    IMPORTANT: You MUST respond in pure JSON format exactly like this:
    {{
        "analysis": "Brief 2-line explanation",
        "actions": [
            {{"label": "Action 1 Name", "command": "backend_system_command_1"}},
            {{"label": "Action 2 Name", "command": "backend_system_command_2"}}
        ]
    }}
    """
    
    try:
        # call ai api
        ai_model = genai.GenerativeModel('gemini-1.5-flash') 
        resp = ai_model.generate_content(prompt)
        
        # clean output if it gives markdown tags
        clean_json = resp.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    
    except Exception as e:
        # print("err:", e)
        return {"error": "generation_failed", "trace": str(e)}