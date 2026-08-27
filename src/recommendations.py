def generate_recommendation(student, prediction):


    recommendations = []



    if student["attendance"] < 75:

        recommendations.append(
            "Improve attendance regularly."
        )


    if student["study_hours"] < 3:

        recommendations.append(
            "Increase daily study hours."
        )


    if student["backlogs"] > 0:

        recommendations.append(
            "Focus on clearing backlogs."
        )


    if prediction == "Excellent":

        recommendations.append(
            "Maintain your current performance."
        )


    elif prediction == "Good":

        recommendations.append(
            "Try improving consistency."
        )


    elif prediction in [
        "Poor",
        "At Risk"
    ]:

        recommendations.append(
            "Meet academic advisor for improvement plan."
        )



    return recommendations


