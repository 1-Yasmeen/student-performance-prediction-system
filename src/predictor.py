import os
import pandas as pd

from src.data_loader import get_all_students



MODEL_PATH = "models/performance_model.pkl"

SCALER_PATH = "models/scaler.pkl"

ENCODER_PATH = "models/label_encoder.pkl"


import joblib
import os
import pandas as pd

from src.data_loader import get_all_students


MODEL_PATH = "models/performance_model.pkl"

SCALER_PATH = "models/scaler.pkl"

ENCODER_PATH = "models/label_encoder.pkl"


FEATURES = [
    "gender",
    "age",
    "attendance",
    "study_hours",
    "assignment_score",
    "internal_marks",
    "previous_marks",
    "backlogs",
    "extracurricular"
]

import joblib
import os
import pandas as pd

from src.data_loader import get_all_students


MODEL_PATH = "models/performance_model.pkl"

SCALER_PATH = "models/scaler.pkl"

ENCODER_PATH = "models/label_encoder.pkl"


FEATURES = [
    "gender",
    "age",
    "attendance",
    "study_hours",
    "assignment_score",
    "internal_marks",
    "previous_marks",
    "backlogs",
    "extracurricular"
]


def _safe_encode_series(series, encoder):
    """Safely transform a pandas Series using a sklearn LabelEncoder-like object.
    Unseen values are mapped to a dedicated 'Unknown' class if present, otherwise the most frequent known class.
    """
    enc_classes = [str(c) for c in encoder.classes_]
    classes_set = set(enc_classes)

    # Prefer an explicit 'Unknown' label if present in the encoder classes
    fallback_label = None
    for candidate in ('Unknown', 'unknown', 'UNK', 'N/A'):
        if candidate in enc_classes:
            fallback_label = candidate
            break
    if fallback_label is None:
        # fallback to encoder.classes_[0] (most frequent in many encoders)
        fallback_label = enc_classes[0]

    def _map_value(v):
        if pd.isna(v):
            return v
        sv = str(v)
        if sv in classes_set:
            return int(encoder.transform([sv])[0])
        # map unseen to fallback_label
        return int(encoder.transform([fallback_label])[0])

    return series.apply(_map_value)


# def predict_student(student_id, source):
#     try:
#         students = get_all_students(source)
#     except Exception as e:
#         return {"error": str(e)}

#     student_id_value = str(student_id).strip().lower()
#     student = students[students["student_id"].astype(str).str.lower() == student_id_value]
#     if student.empty:
#         return {"error": "Student ID not found"}

#     student_data = student.iloc[0].copy()

#     try:
#         import joblib
#     except Exception as e:
#         return {"error": f"joblib import failed: {e}"}

#     model = joblib.load(MODEL_PATH)
#     scaler = joblib.load(SCALER_PATH)
#     encoders = joblib.load(ENCODER_PATH)

#     prediction_data = student.iloc[0:1].copy()

#     # Convert text values safely
#     for column, encoder in encoders.items():
#         if column in prediction_data.columns:
#             try:
#                 prediction_data[column] = _safe_encode_series(prediction_data[column], encoder)
#             except Exception:
#                 # As a last resort, coerce to string and map unknowns to fallback
#                 enc_classes = [str(c) for c in encoder.classes_]
#                 fallback = enc_classes[0] if enc_classes else ''
#                 prediction_data[column] = prediction_data[column].astype(str).apply(
#                     lambda v: int(encoder.transform([v if v in enc_classes else fallback])[0])
#                 )

#     features = prediction_data[FEATURES]
#     features = scaler.transform(features)
#     features = pd.DataFrame(features, columns=FEATURES)

#     prediction = model.predict(features)[0]
#     probability = model.predict_proba(features)[0]

#     classes = list(model.classes_)
#     prob_map = {classes[i]: round(float(probability[i]) * 100, 2) for i in range(len(classes))}
#     confidence = max(prob_map.values())

#     return {
#         "student_details": student_data.to_dict(),
#         "prediction": prediction,
#         "confidence": confidence,
#         "probabilities": prob_map
#     }
















































def predict_student(student_id, source):
    try:
        students = get_all_students(source)
    except Exception as e:
        return {"error": str(e)}

    # --------------------------------------------
    # Find student
    # --------------------------------------------

    student_id_value = str(student_id).strip().lower()

# --------------------------------------------
# Debug student dataset
# --------------------------------------------

    print("===================================")
    print("PREDICT STUDENT DEBUG")
    print("SOURCE:", source)
    print("STUDENT ID:", student_id)
    print("STUDENTS TYPE:", type(students))
    print("STUDENTS SHAPE:", students.shape)
    print("STUDENTS COLUMNS:", students.columns.tolist())
    print("STUDENTS HEAD:")
    print(students.head())
    print("===================================")


    # --------------------------------------------
    # Find student
    # --------------------------------------------

    student_id_value = str(student_id).strip().lower()

    student = students[
        students["student_id"]
        .astype(str)
        .str.strip()
        .str.lower()
        == student_id_value
    ]
    if student.empty:
        return {
            "error": "Student ID not found"
        }

    student_data = student.iloc[0].copy()

    # --------------------------------------------
    # Load model files
    # --------------------------------------------

    try:
        import joblib

        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        encoders = joblib.load(ENCODER_PATH)

    except Exception as e:
        return {
            "error": f"Unable to load prediction model: {e}"
        }

    # --------------------------------------------
    # Prepare student data
    # --------------------------------------------

    prediction_data = student.iloc[0:1].copy()

    for column, encoder in encoders.items():

        if column not in prediction_data.columns:
            continue

        try:
            prediction_data[column] = _safe_encode_series(
                prediction_data[column],
                encoder
            )

        except Exception:

            enc_classes = [
                str(value)
                for value in encoder.classes_
            ]

            fallback = (
                enc_classes[0]
                if enc_classes
                else ""
            )

            prediction_data[column] = (
                prediction_data[column]
                .astype(str)
                .apply(
                    lambda value:
                    int(
                        encoder.transform(
                            [
                                value
                                if value in enc_classes
                                else fallback
                            ]
                        )[0]
                    )
                )
            )

    # --------------------------------------------
    # Prepare features
    # --------------------------------------------

    try:
        features = prediction_data[FEATURES]

        features = scaler.transform(features)

        features = pd.DataFrame(
            features,
            columns=FEATURES
        )

    except Exception as e:
        return {
            "error": f"Unable to prepare student data: {e}"
        }

    # --------------------------------------------
    # Prediction
    # --------------------------------------------

    try:
        prediction = model.predict(features)[0]

        probabilities = model.predict_proba(
            features
        )[0]

    except Exception as e:
        return {
            "error": f"Prediction failed: {e}"
        }

    # --------------------------------------------
    # Convert prediction probabilities
    # to normal Python values
    # --------------------------------------------

    classes = model.classes_

    probability_map = {}

    for class_name, probability in zip(
        classes,
        probabilities
    ):

        label = str(class_name)

        probability_map[label] = round(
            float(probability) * 100,
            2
        )

    # Highest probability = confidence
    confidence = round(
        max(probability_map.values()),
        2
    )

    # Convert NumPy prediction to normal Python string
    prediction = str(prediction)

    # --------------------------------------------
    # Return result
    # --------------------------------------------

    return {
        "student_id": str(student_id),

        "student_details":
            student_data.to_dict(),

        "prediction": prediction,

        "confidence": confidence,

        "probabilities": probability_map
    }                           





































def predict_from_row(row_dict):
    """Predict from a single student row provided as a dict (no lookup). Returns same shape as predict_student but uses provided row."""
    try:
        import joblib
    except Exception as e:
        return {"error": f"joblib import failed: {e}"}

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    encoders = joblib.load(ENCODER_PATH)

    # Build single-row DataFrame
    df = pd.DataFrame([row_dict])

    # Ensure required feature columns exist
    for feat in FEATURES:
        if feat not in df.columns:
            df[feat] = None

    # Apply encoders for categorical columns found (safely)
    for column, encoder in encoders.items():
        if column in df.columns:
            try:
                df[column] = _safe_encode_series(df[column], encoder)
            except Exception:
                enc_classes = [str(c) for c in encoder.classes_]
                fallback = enc_classes[0] if enc_classes else ''
                df[column] = df[column].astype(str).apply(
                    lambda v: int(encoder.transform([v if v in enc_classes else fallback])[0])
                )

    features = df[FEATURES]
    features = scaler.transform(features)
    features = pd.DataFrame(features, columns=FEATURES)

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]

    classes = list(model.classes_)
    prob_map = {classes[i]: round(float(probability[i]) * 100, 2) for i in range(len(classes))}
    confidence = max(prob_map.values())

    return {
        "student_details": row_dict,
        "prediction": prediction,
        "confidence": confidence,
        "probabilities": prob_map
    }




