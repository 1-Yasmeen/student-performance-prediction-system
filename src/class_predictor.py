import pandas as pd

from src.data_loader import get_all_students
from src.predictor import predict_student


def predict_class(source):

    print("===================================")
    print("PREDICT CLASS")
    print("SOURCE:", source)

    students = get_all_students(source)

    print("STUDENTS SHAPE:", students.shape)
    print("STUDENT COLUMNS:", students.columns.tolist())

    if students.empty:

        print("WARNING: DATASET IS EMPTY")

        return pd.DataFrame(
            columns=[
                "student_id",
                "prediction",
                "confidence",
                "dataset"
            ]
        )

    results = []

    for _, student in students.iterrows():

        student_id = student["student_id"]

        print("-----------------------------------")
        print("PREDICTING STUDENT:", student_id)

        try:

            result = predict_student(
                student_id,
                source
            )

            print("PREDICTION RESULT:", result)

            if "error" not in result:

                results.append({
                    "student_id": student_id,
                    "prediction": result["prediction"],
                    "confidence": result["confidence"],
                    "dataset": source
                })

            else:

                print(
                    "PREDICTION ERROR:",
                    result["error"]
                )

        except Exception as e:

            print(
                "STUDENT EXCEPTION:",
                repr(e)
            )

    final_results = pd.DataFrame(results)

    print("===================================")
    print("FINAL RESULTS")
    print("RESULT SHAPE:", final_results.shape)

    return final_results