from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from functools import wraps

import pandas as pd
import os


from src.predictor import predict_student
from src.recommendations import generate_recommendation

from src.authentication import (
    create_database,
    verify_user,
    update_password
)


from src.upload_handler import (
    save_uploaded_file,
    load_uploaded_data,
    validate_columns,
    append_student_row,
    REQUIRED_COLUMNS
)

from src.upload_predictor import (
    predict_uploaded_students
)






from src.class_predictor import (
    predict_class
)

from src.report_generator import (
    generate_prediction_report
)

import json










app = Flask(__name__)



app.secret_key = "student-performance-secret-key"

app.config["UPLOAD_FOLDER"] = "uploads"
# Create login database
create_database()




















def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "username" not in session:

            return redirect(
                url_for("login")
            )

        return function(*args, **kwargs)

    return wrapper









def role_required(*roles):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            if "role" not in session:

                return redirect(
                    url_for("login")
                )


            if session["role"] not in roles:

                return render_template(
                    "error.html",
                    message="Access Denied"
                )


            return function(*args, **kwargs)


        return wrapper


    return decorator








# @app.route("/")
# def home():

#     return render_template(
#         "index.html"
#     )

@app.route("/")
def home():
    return redirect(url_for("login"))




















@app.route("/login", methods=["GET","POST"])
def login():


    if request.method == "POST":


        username = request.form["username"]

        password = request.form["password"]


        user = verify_user(
            username,
            password
        )


        if user:


            session["username"] = user["username"]

            session["role"] = user["role"]


            return redirect(
                url_for("dashboard")
            )


        else:


            return render_template(
                "login.html",
                error="Invalid username or password"
            )


    return render_template(
        "login.html"
    )






@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session["role"]
    )
































@app.route("/student-data-selection", methods=["GET", "POST"])
@login_required
def student_data_selection():

    if request.method == "POST":

        source = request.form.get("source", "").strip()

        if not source:
            return render_template(
                "data_selection.html",
                selection_type="student",
                error="Please select a dataset."
            )

        return redirect(
            url_for(
                "student_search",
                source=source
            )
        )

    return render_template(
        "data_selection.html",
        selection_type="student"
    )


@app.route("/class-data-selection", methods=["GET", "POST"])
@login_required
@role_required("admin", "teacher")
def class_data_selection():

    if request.method == "POST":

        source = request.form.get("source", "").strip()

        if not source:
            return render_template(
                "data_selection.html",
                selection_type="class",
                error="Please select a dataset."
            )

        return redirect(
            url_for(
                "class_performance",
                source=source
            )
        )

    return render_template(
        "data_selection.html",
        selection_type="class"
    )





























@app.route("/logout")
def logout():


    session.clear()


    return redirect(
        url_for("login")
    )













@app.route("/student-search/<source>")
@login_required
def student_search(source):

    return render_template(
        "student_search.html",
        source=source
    )




























@app.route("/predict", methods=["POST"])
@login_required
def predict():

    student_id = request.form.get(
        "student_id",
        ""
    ).strip()

    source = request.form.get(
        "source",
        ""
    ).strip()

    if not student_id:
        return render_template(
            "result.html",
            error="Please enter a Student ID."
        )

    if not source:
        return render_template(
            "result.html",
            error="Please select a dataset."
        )

    result = predict_student(
        student_id,
        source
    )

    if "error" in result:
        return render_template(
            "result.html",
            error=result["error"]
        )

    recommendations = generate_recommendation(
        result["student_details"],
        result["prediction"]
    )

    return render_template(
        "result.html",
        result=result,
        recommendations=recommendations
    )


  






























# @app.route("/class-performance/<source>")
# @login_required
# @role_required("admin","teacher")
# def class_performance(source):

#     results = predict_class(
#         source
#     )


#     students = results.to_dict(
#         orient="records"
#     )


#     return render_template(

#         "class_result.html",

#         students=students

#     )











@app.route("/class-performance/<source>")
@login_required
@role_required("admin", "teacher")
def class_performance(source):

    print("===================================")
    print("CLASS PERFORMANCE ROUTE")
    print("SOURCE:", source)

    try:

        results = predict_class(source)

        print("RESULT TYPE:", type(results))
        print("RESULT SHAPE:", results.shape)
        print("RESULT COLUMNS:", results.columns.tolist())

        students = results.to_dict(
            orient="records"
        )

        print("STUDENTS:", len(students))

        return render_template(
            "class_result.html",
            students=students
        )

    except Exception as e:

        print("CLASS PERFORMANCE ERROR:", repr(e))

        return render_template(
            "error.html",
            message=f"Class performance error: {str(e)}"
        )





# Upload Student Data

@app.route("/upload", methods=["GET","POST"])
@login_required
@role_required("admin")
def upload():


    if request.method=="POST":


        form_type = request.form.get("form_type")

        if form_type == "single":
            row = {
                "student_id": request.form.get("student_id", "").strip(),
                "gender": request.form.get("gender", "").strip(),
                "age": request.form.get("age", "").strip(),
                "attendance": request.form.get("attendance", "").strip(),
                "study_hours": request.form.get("study_hours", "").strip(),
                "assignment_score": request.form.get("assignment_score", "").strip(),
                "internal_marks": request.form.get("internal_marks", "").strip(),
                "previous_marks": request.form.get("previous_marks", "").strip(),
                "backlogs": request.form.get("backlogs", "").strip(),
                "extracurricular": request.form.get("extracurricular", "").strip(),
            }

            missing_fields = [
                field for field in REQUIRED_COLUMNS
                if not row.get(field)
            ]

            if missing_fields:
                return render_template(
                    "upload.html",
                    error=f"Please fill in all fields: {', '.join(missing_fields)}"
                )

            append_student_row(row)

            return render_template(
                "upload.html",
                success="Student saved successfully to real student dataset."
            )


        file=request.files.get("file")


        if file is None:

            return render_template(

                "upload.html",

                error="No file selected"

            )



        if file.filename=="":

            return render_template(

                "upload.html",

                error="Please select a file"

            )



        file_path = save_uploaded_file(
            file
        )


        data = load_uploaded_data(
            file_path
        )


        missing = validate_columns(
            data
        )



        if missing:


            return render_template(

                "upload.html",

                error=f"Missing columns: {missing}"

            )



        predicted_data = predict_uploaded_students(
            data
        )

        students = predicted_data.to_dict(
            orient="records"
        )

        return render_template(
            "upload_result_new.html",
            students=students
        )

    return render_template(
        "upload.html"
    )





@app.route("/manage-users")
@login_required
@role_required("admin")
def manage_users():

    return render_template(
        "manage_users.html"
    )




# User Profile

@app.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html",
        username=session["username"],
        role=session["role"]
    )


@app.route("/change-password", methods=["POST"])
@login_required
def change_password():
    current_password = request.form.get("current_password", "").strip()
    new_password = request.form.get("new_password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()

    if not current_password or not new_password or not confirm_password:
        return render_template(
            "profile.html",
            username=session["username"],
            role=session["role"],
            error="All password fields are required."
        )

    if new_password != confirm_password:
        return render_template(
            "profile.html",
            username=session["username"],
            role=session["role"],
            error="New passwords do not match."
        )

    if not verify_user(session["username"], current_password):
        return render_template(
            "profile.html",
            username=session["username"],
            role=session["role"],
            error="Current password is incorrect."
        )

    update_password(session["username"], new_password)

    return render_template(
        "profile.html",
        username=session["username"],
        role=session["role"],
        success="Password updated successfully."
    )


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not username or not new_password or not confirm_password:
            return render_template(
                "forgot_password.html",
                error="All fields are required."
            )

        if new_password != confirm_password:
            return render_template(
                "forgot_password.html",
                error="Passwords do not match."
            )

        if update_password(username, new_password):
            return render_template(
                "forgot_password.html",
                success="Password reset successfully. You may now log in."
            )

        return render_template(
            "forgot_password.html",
            error="Username not found. Please try again."
        )

    return render_template("forgot_password.html")


# User Registration

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]

        if not username or not password:
            return render_template(
                "register.html",
                error="Username and password required"
            )

        if password != password_confirm:
            return render_template(
                "register.html",
                error="Passwords do not match"
            )

        try:
            from src.authentication import add_user
            result = add_user(username, password, "student")
            
            if result:
                return render_template(
                    "register.html",
                    success="Registration successful! Please login."
                )
            else:
                return render_template(
                    "register.html",
                    error="Username already exists"
                )
        except Exception as e:
            return render_template(
                "register.html",
                error=str(e)
            )

    return render_template("register.html")




# API: Search Students (AJAX)

@app.route("/api/search-student", methods=["POST"])
@login_required
def api_search_student():

    student_id = str(request.json.get("student_id", "")).strip()
    source = request.json.get("source")

    try:
        result = predict_student(student_id, source)
        return json.dumps(result, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})



@app.route("/api/predict-row", methods=["POST"])
@login_required
def api_predict_row():
    try:
        row = request.json.get("row")
        if not isinstance(row, dict):
            return json.dumps({"error": "Invalid row payload"})
        from src.predictor import predict_from_row
        result = predict_from_row(row)
        return json.dumps(result, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})




# Reports with Export

@app.route("/reports", methods=["GET", "POST"])
@login_required
@role_required("admin", "teacher")
def reports():

    reports_data = []
    
    if request.method == "POST":
        source = request.form.get("source", "historical")
        
        try:
            results = predict_class(source)
            reports_data = results.to_dict(orient="records")
            
            # Generate report file
            report_file = generate_prediction_report(
                results,
                source
            )
            
        except Exception as e:
            return render_template(
                "reports.html",
                error=str(e)
            )

    return render_template(
        "reports.html",
        reports=reports_data
    )




# Error Handlers

@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "error.html",
        message="Page not found. Please check the URL."
    ), 404




@app.errorhandler(500)
def internal_error(error):
    return render_template(
        "error.html",
        message="Internal server error. Please try again."
    ), 500



print(app.url_map)
# Run Application

if __name__ == "__main__":

    app.run(

        debug=True

    )

