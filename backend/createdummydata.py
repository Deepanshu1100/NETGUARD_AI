import pandas as pd
import numpy as np
import os

# Ensure data directory exists in the root folder
os.makedirs('../data', exist_ok=True)

print("⚙️ Generating professional telecom network telemetry data...")

np.random.seed(42)
n_samples = 1000

# Creating columns matching Telstra network structure
df = pd.DataFrame({
    'id': range(1, n_samples + 1),
    'location': [f'location {np.random.randint(1, 30)}' for _ in range(n_samples)],
    'fault_severity': np.random.choice([0, 1, 2], size=n_samples, p=[0.7, 0.2, 0.1]) # 0: Normal, 1: Warning, 2: Critical
})

# Adding mock event types for feature engineering
for i in range(1, 6):
    df[f'event_type_{i}'] = np.random.randint(0, 5, size=n_samples)

# Save to the data folder
file_path = '../data/train.csv'
df.to_csv(file_path, index=False)

print(f"✅ Success! Dummy train.csv created at: {file_path}")