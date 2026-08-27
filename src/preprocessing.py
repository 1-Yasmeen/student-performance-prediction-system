import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler



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



def preprocess_data(df):


    data = df.copy()


    encoders = {}


    categorical_columns = [

        "gender",
        "extracurricular"

    ]


    for column in categorical_columns:


        encoder = LabelEncoder()


        data[column] = encoder.fit_transform(
            data[column]
        )


        encoders[column] = encoder



    scaler = StandardScaler()


    data[FEATURES] = scaler.fit_transform(
        data[FEATURES]
    )


    return data, scaler, encoders
