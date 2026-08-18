import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
import joblib
import os
from datetime import datetime

print("🚀 Starting NetGuard AI Training Pipeline...")

# 1. Load Data (Abhi hum basic train.csv use kar rahe hain)
# Note: Make sure tumhari kaggle files 'data' folder me hain
data_path = '../data/train.csv'

try:
    df = pd.read_csv(data_path)
    print("✅ Data Loaded Successfully!")
except FileNotFoundError:
    print("❌ Error: train.csv not found in the 'data' folder! Please check.")
    exit()

# (Mock Data Engineering for initial test - Assuming 'fault_severity' is the target)
# Real Telstra dataset me id, location, fault_severity columns hote hain.
X = df.drop(['id', 'fault_severity'], axis=1, errors='ignore') 
# Convert categorical locations (like 'location 1') to numeric codes for XGBoost
if 'location' in df.columns:
    X['location'] = X['location'].astype('category').cat.codes
    
y = df['fault_severity'] if 'fault_severity' in df.columns else np.random.randint(0, 3, size=len(X)) # Fallback

# 2. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. MLOPS FEATURE 1: SMOTE (Handling Imbalanced Telecom Data)
print("⚖️ Applying SMOTE to balance the fault logs...")
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# 4. Initialize and Train XGBoost
print("🧠 Training Enterprise XGBoost Model...")
model = xgb.XGBClassifier(
    objective='multi:softprob', 
    eval_metric='mlogloss', 
    use_label_encoder=False,
    max_depth=5,
    learning_rate=0.1
)

model.fit(X_train_smote, y_train_smote)

# 5. Evaluate the Model
y_pred = model.predict(X_test)
print("\n📊 Model Evaluation Report:")
print(classification_report(y_test, y_pred))

# 6. MLOPS FEATURE 2: Model Versioning
# Hum model ko version aur date ke hisaab se save karenge
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
model_filename = f"xgboost_netguard_v1_{timestamp}.pkl"

joblib.dump(model, model_filename)
print(f"💾 Model securely saved as: {model_filename}")
print("✅ Phase 1 Complete: Model is ready for the FastAPI Backend!")