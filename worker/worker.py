import numpy as np
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
import pandas as pd

# Read dataset
dataset = pd.read_csv('cic-ids-2017(10).csv')

# Train test split
normal_traffic = dataset.loc[dataset['Attack Type'] == 'BENIGN']
intrusions = dataset.loc[dataset['Attack Type'] != 'BENIGN']

normal_traffic = normal_traffic.sample(n=len(intrusions), replace=False)

ids_data = pd.concat([intrusions, normal_traffic])
ids_data['Attack Type'] = np.where((ids_data['Attack Type'] == 'BENIGN'), 0, 1)
bc_data = ids_data.sample(n=15000)

X = bc_data.drop('Attack Type', axis=1)
y = bc_data['Attack Type']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=101)

# Initialize Logistic Regression model
model = LogisticRegression()

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.4f}")

# Send model weights to the aggregator
aggregator_url = "http://aggregator:5000/aggregate"
model_weights = pickle.dumps(model)

# Send the serialized model weights to the aggregator
response = requests.post(aggregator_url, data=model_weights)

if response.status_code == 200:
    print("Model weights successfully sent to aggregator.")
else:
    print("Failed to send model weights.")
