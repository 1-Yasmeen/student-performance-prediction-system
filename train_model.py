from src.data_loader import get_historical_data
from src.trainer import train_model



print("Loading dataset...")


data = get_historical_data()



print(
    "Training model..."
)


model = train_model(
    data
)


print(
    "Training completed successfully!"
)

