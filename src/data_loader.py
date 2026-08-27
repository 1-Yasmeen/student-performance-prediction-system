import pandas as pd
import os



BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)



DATA_FOLDER = os.path.join(
    BASE_DIR,
    "data"
)





def load_dataset(file_path):


    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )


    return pd.read_csv(file_path)







def get_historical_data():


    path = os.path.join(

        DATA_FOLDER,

        "historical_students.csv"

    )


    return load_dataset(path)







def get_current_students():


    path = os.path.join(

        DATA_FOLDER,

        "current_students.csv"

    )


    return load_dataset(path)







def get_real_students():


    path = os.path.join(

        DATA_FOLDER,

        "real_students.csv"

    )


    if os.path.exists(path):

        return load_dataset(path)


    else:

        return pd.DataFrame()


def get_all_students(source):

    if source == "historical":

        path = os.path.join(
            DATA_FOLDER,
            "historical_students.csv"
        )

    elif source == "current":

        path = os.path.join(
            DATA_FOLDER,
            "current_students.csv"
        )

    elif source == "real":

        path = os.path.join(
            DATA_FOLDER,
            "real_students.csv"
        )

    else:

        raise ValueError(
            "Invalid dataset source"
        )

    # -----------------------------------------
    # Check that dataset exists
    # -----------------------------------------

    if not os.path.exists(path):

        print("DATASET NOT FOUND:", path)

        return pd.DataFrame()

    # -----------------------------------------
    # Load dataset
    # -----------------------------------------

    data = pd.read_csv(path)

    # -----------------------------------------
    # Clean column names
    # -----------------------------------------

    data.columns = (
        data.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # -----------------------------------------
    # Debug information
    # -----------------------------------------

    print("===================================")
    print("DATASET LOADED")
    print("SOURCE:", source)
    print("PATH:", path)
    print("ROWS:", len(data))
    print("COLUMNS:", data.columns.tolist())
    print("===================================")

    # -----------------------------------------
    # Make sure student_id exists
    # -----------------------------------------

    if "student_id" not in data.columns:

        raise ValueError(
            "Dataset does not contain 'student_id'. "
            f"Available columns: {data.columns.tolist()}"
        )

    # -----------------------------------------
    # Add dataset source
    # -----------------------------------------

    data["dataset"] = source

    return data