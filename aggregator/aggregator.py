import pickle
from flask import Flask, request

app = Flask(__name__)

# Initialize an empty Logistic Regression model
model = None


@app.route('/aggregate', methods=['POST'])
def aggregate():
    global model
    model_weights = request.data

    # Deserialize the model weights
    new_model = pickle.loads(model_weights)

    # If model is not initialized, set the received model as the initial model
    if model is None:
        model = new_model
    else:
        # Aggregate the models
        model.coef_ = (model.coef_ + new_model.coef_) / 2
        model.intercept_ = (model.intercept_ + new_model.intercept_) / 2

    # Save the aggregated model to a file
    with open("/app/aggregated_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Model aggregated and saved.")
    return "Aggregation successful", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
