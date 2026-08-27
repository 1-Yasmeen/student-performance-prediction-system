# import pandas as pd
# import os



# REQUIRED_COLUMNS = [

#     "student_id",
#     "gender",
#     "age",
#     "attendance",
#     "study_hours",
#     "assignment_score",
#     "internal_marks",
#     "previous_marks",
#     "backlogs",
#     "extracurricular"

# ]





# def validate_columns(df):


#     missing_columns = []


#     for column in REQUIRED_COLUMNS:


#         if column not in df.columns:

#             missing_columns.append(column)



#     return missing_columns





# def save_uploaded_file(file):


#     upload_folder = "uploads"


#     os.makedirs(
#         upload_folder,
#         exist_ok=True
#     )


#     file_path = os.path.join(

#         upload_folder,

#         file.filename

#     )


#     file.save(
#         file_path
#     )


#     return file_path





# def load_uploaded_data(file_path):


#     dataframe = pd.read_csv(
#         file_path
#     )


#     return dataframe













# import os
# import pandas as pd
# from werkzeug.utils import secure_filename



# UPLOAD_FOLDER = "uploads"



# REQUIRED_COLUMNS = [

#     "student_id",
#     "gender",
#     "age",
#     "attendance",
#     "study_hours",
#     "assignment_score",
#     "internal_marks",
#     "previous_marks",
#     "backlogs",
#     "extracurricular"

# ]




# def save_uploaded_file(file):


#     os.makedirs(
#         UPLOAD_FOLDER,
#         exist_ok=True
#     )


#     filename = secure_filename(
#         file.filename
#     )


#     path = os.path.join(
#         UPLOAD_FOLDER,
#         filename
#     )


#     file.save(path)


#     return path





# def load_uploaded_data(path):


#     return pd.read_csv(path)





# def validate_columns(data):


#     missing_columns = []


#     for column in REQUIRED_COLUMNS:

#         if column not in data.columns:

#             missing_columns.append(column)



#     return missing_columns







import os
import pandas as pd
from werkzeug.utils import secure_filename

# from werkzeug.utils import secure_filename



# UPLOAD_FOLDER = "uploads"



BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

DATA_FOLDER = os.path.join(
    BASE_DIR,
    "data"
)

REAL_STUDENTS_FILE = os.path.join(
    DATA_FOLDER,
    "real_students.csv"
)
























REQUIRED_COLUMNS = [

    "student_id",
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





def save_uploaded_file(file):

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    filename = secure_filename(
        file.filename
    )

    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(path)

    return path






def load_uploaded_data(path):


    return pd.read_csv(path)







def validate_columns(data):


    missing_columns=[]



    for column in REQUIRED_COLUMNS:


        if column not in data.columns:


            missing_columns.append(column)



    return missing_columns



def append_student_row(row):
    os.makedirs(
        DATA_FOLDER,
        exist_ok=True
    )

    path = REAL_STUDENTS_FILE

    if os.path.exists(path):
        existing = pd.read_csv(path)
    else:
        existing = pd.DataFrame(columns=REQUIRED_COLUMNS)

    new_row = {col: row.get(col, "") for col in REQUIRED_COLUMNS}
    existing = pd.concat([existing, pd.DataFrame([new_row])], ignore_index=True)
    existing.to_csv(path, index=False)
    return path