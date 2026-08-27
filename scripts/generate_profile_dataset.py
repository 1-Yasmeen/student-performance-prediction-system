import pandas as pd
import random
import os


# Make results repeatable
random.seed(42)


# Create data folder if not exists
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)



# Student performance profiles

profiles = {

    "Excellent": {
        "attendance": (85,100),
        "study_hours": (5,8),
        "assignment_score": (85,100),
        "internal_marks": (85,100),
        "previous_marks": (80,100),
        "backlogs": (0,0)
    },


    "Good": {
        "attendance": (75,90),
        "study_hours": (4,6),
        "assignment_score": (70,90),
        "internal_marks": (70,90),
        "previous_marks": (65,90),
        "backlogs": (0,1)
    },


    "Average": {
        "attendance": (60,80),
        "study_hours": (2,5),
        "assignment_score": (55,75),
        "internal_marks": (55,75),
        "previous_marks": (50,75),
        "backlogs": (0,2)
    },


    "Poor": {
        "attendance": (50,65),
        "study_hours": (1,3),
        "assignment_score": (40,60),
        "internal_marks": (40,60),
        "previous_marks": (40,60),
        "backlogs": (1,3)
    },


    "At Risk": {
        "attendance": (30,55),
        "study_hours": (0.5,2),
        "assignment_score": (30,50),
        "internal_marks": (30,50),
        "previous_marks": (30,50),
        "backlogs": (2,5)
    }

}



def generate_student(student_id, include_result=True):


    performance_type = random.choice(
        list(profiles.keys())
    )


    profile = profiles[performance_type]


    attendance = random.randint(
        *profile["attendance"]
    )


    study_hours = round(
        random.uniform(
            *profile["study_hours"]
        ),
        1
    )


    assignment_score = random.randint(
        *profile["assignment_score"]
    )


    internal_marks = random.randint(
        *profile["internal_marks"]
    )


    previous_marks = random.randint(
        *profile["previous_marks"]
    )


    backlogs = random.randint(
        *profile["backlogs"]
    )


    extracurricular = random.choice(
        ["Yes","No"]
    )


    # Controlled noise
    noise = random.randint(-5,5)


    performance_score = (

        attendance * 0.25 +

        study_hours * 5 +

        assignment_score * 0.20 +

        internal_marks * 0.20 +

        previous_marks * 0.15 -

        backlogs * 5 +

        noise

    )


    if performance_score >= 85:
        result = "Excellent"

    elif performance_score >= 70:
        result = "Good"

    elif performance_score >= 55:
        result = "Average"

    elif performance_score >= 40:
        result = "Poor"

    else:
        result = "At Risk"



    student = {

        "student_id": student_id,

        "gender": random.choice(
            ["Male","Female"]
        ),

        "age": random.randint(
            17,23
        ),

        "attendance": attendance,

        "study_hours": study_hours,

        "assignment_score": assignment_score,

        "internal_marks": internal_marks,

        "previous_marks": previous_marks,

        "backlogs": backlogs,

        "extracurricular": extracurricular

    }



    if include_result:

        student["final_result"] = result



    return student





# -----------------------------
# Create Historical Dataset
# -----------------------------

historical_data = []


for i in range(1,2001):

    student = generate_student(
        f"HIS{i:04d}",
        True
    )

    historical_data.append(student)



historical_df = pd.DataFrame(
    historical_data
)


historical_df.to_csv(

    os.path.join(
        DATA_DIR,
        "historical_students.csv"
    ),

    index=False

)



# -----------------------------
# Create Current Dataset
# -----------------------------


current_data = []


for i in range(1,201):

    student = generate_student(
        f"CUR{i:04d}",
        False
    )

    current_data.append(student)



current_df = pd.DataFrame(
    current_data
)


current_df.to_csv(

    os.path.join(
        DATA_DIR,
        "current_students.csv"
    ),

    index=False

)



print("Dataset generation completed successfully!")
print("Historical students:", len(historical_df))
print("Current students:", len(current_df))
