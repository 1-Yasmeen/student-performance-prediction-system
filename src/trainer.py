from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


from src.preprocessing import preprocess_data, FEATURES
from src.model_utils import save_model



def train_model(df):


    X = df[FEATURES]

    y = df["final_result"]



    processed_data, scaler, encoders = preprocess_data(
        df
    )


    X = processed_data[FEATURES]



    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,
        test_size=0.2,
        random_state=42

    )



    model = RandomForestClassifier(

        n_estimators=200,
        random_state=42

    )



    model.fit(

        X_train,
        y_train

    )



    predictions = model.predict(
        X_test
    )


    accuracy = accuracy_score(
        y_test,
        predictions
    )


    print(
        "Model Accuracy:",
        accuracy
    )



    save_model(

        model,

        "models/performance_model.pkl"

    )


    save_model(

        scaler,

        "models/scaler.pkl"

    )


    save_model(

        encoders,

        "models/label_encoder.pkl"

    )


    return model
