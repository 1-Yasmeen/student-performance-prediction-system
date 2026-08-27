import pandas as pd
import os
from datetime import datetime



BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

REPORTS_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)



def generate_prediction_report(data, source):
    """
    Generate a CSV report of predictions.
    
    Args:
        data: DataFrame with predictions
        source: Data source (historical, current, real)
    
    Returns:
        Path to the generated report file
    """
    
    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    
    # Create report filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prediction_report_{source}_{timestamp}.csv"
    filepath = os.path.join(REPORTS_FOLDER, filename)
    
    # Save report
    data.to_csv(filepath, index=False)
    
    return filepath



def generate_summary_report(data):
    """
    Generate summary statistics for the report.
    
    Args:
        data: DataFrame with predictions
    
    Returns:
        Dictionary with summary statistics
    """
    
    if data.empty:
        return {}
    
    summary = {
        "total_students": len(data),
        "excellent_count": len(data[data["prediction"] == "Excellent"]),
        "good_count": len(data[data["prediction"] == "Good"]),
        "at_risk_count": len(data[data["prediction"] == "At Risk"]),
        "poor_count": len(data[data["prediction"] == "Poor"]),
        "avg_confidence": data["confidence"].mean(),
        "min_confidence": data["confidence"].min(),
        "max_confidence": data["confidence"].max()
    }
    
    return summary
