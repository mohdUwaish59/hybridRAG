import pickle

# Load the classification model pickle file
model_path = "classification_model.pkl"

with open(model_path, 'rb') as file:
    classification_model = pickle.load(file)

# Print the type of the loaded object
print(f"Loaded model type: {type(classification_model)}")

# If it's a Pipeline, list its steps
if hasattr(classification_model, 'steps'):
    print("Pipeline steps:")
    for step_name, step_object in classification_model.steps:
        print(f" - {step_name}: {type(step_object)}")
else:
    print("The loaded object is not a Pipeline.")
