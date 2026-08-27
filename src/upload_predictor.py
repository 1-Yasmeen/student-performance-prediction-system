import pandas as pd
import joblib
import os


from src.preprocessing import FEATURES




# MODEL_PATH = "models/performance_model.pkl"
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "performance_model.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "scaler.pkl"
)

ENCODER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "label_encoder.pkl"
)





# SCALER_PATH = "models/scaler.pkl"

# ENCODER_PATH = "models/label_encoder.pkl"




def predict_uploaded_students(df):


    model = joblib.load(
        MODEL_PATH
    )


    scaler = joblib.load(
        SCALER_PATH
    )


    encoders = joblib.load(
        ENCODER_PATH
    )



    data = df.copy()



    for column, encoder in encoders.items():

        data[column] = (

            data[column]

            .astype(str)

            .str.strip()

        )

        unknown = set(data[column]) - set(encoder.classes_)

        if unknown:

            raise ValueError(

                f"Unknown values in '{column}': {unknown}"

            )

        data[column] = encoder.transform(
            data[column]
        )

    missing_columns = [

    column

    for column in FEATURES

    if column not in data.columns

]

    if missing_columns:

        raise ValueError(

            f"Missing columns: {missing_columns}"

        )

    features = data[FEATURES]



    features = scaler.transform(
        features
    )

    # Create DataFrame with feature names to avoid sklearn warnings
    features = pd.DataFrame(
        features,
        columns=FEATURES
    )


    predictions = model.predict(
        features
    )


    probabilities = model.predict_proba(
        features
    )



    confidence = (

        probabilities.max(axis=1)
        *100

    )



    data["prediction"] = predictions

    data["confidence"] = confidence.round(2)

    return data