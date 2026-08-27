# from src.predictor import predict_student
# from src.recommendations import generate_recommendation



# student_id = "CUR0001"



# result = predict_student(
#     student_id
# )



# print(result)



# if "error" not in result:


#     recommendations = generate_recommendation(

#         result["student_details"],

#         result["prediction"]

#     )


#     print("\nRecommendations:")


#     for item in recommendations:

#         print("-",item)






from src.predictor import predict_student



result = predict_student(

    "HIS0001",

    "historical"

)


print(result)