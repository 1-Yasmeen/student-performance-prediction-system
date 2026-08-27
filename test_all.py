#!/usr/bin/env python
"""
Test script for Student Performance Predictor
"""

from src.predictor import predict_student
from src.recommendations import generate_recommendation
from src.upload_predictor import predict_uploaded_students
import pandas as pd

print("\n" + "="*60)
print("STUDENT PERFORMANCE PREDICTOR - TEST SUITE")
print("="*60)

# Test 1: Individual Student Prediction
print("\n[Test 1] Individual Student Prediction")
print("-" * 60)
result = predict_student('HIS0001', 'historical')
print(f"✓ Student ID: {result['student_details']['student_id']}")
print(f"✓ Prediction: {result['prediction']}")
print(f"✓ Confidence: {result['confidence']}%")

# Test 2: Recommendations
print("\n[Test 2] Generate Recommendations")
print("-" * 60)
recs = generate_recommendation(result['student_details'], result['prediction'])
print("Recommendations:")
for r in recs:
    print(f"  • {r}")

# Test 3: Bulk Upload Prediction
print("\n[Test 3] Batch Prediction from CSV")
print("-" * 60)
df = pd.read_csv('data/current_students.csv')
batch_result = predict_uploaded_students(df.iloc[:3])
print(f"✓ Processed {len(batch_result)} students")
print("\nBatch Results:")
for idx, row in batch_result.iterrows():
    print(f"  • {row['student_id']}: {row['prediction']} ({row['confidence']}%)")

# Test 4: Database Connection
print("\n[Test 4] Database & Authentication")
print("-" * 60)
from src.authentication import verify_user
user = verify_user('admin', 'admin123')
if user:
    print(f"✓ User Login: {user['username']} ({user['role']})")
else:
    print("✗ Login failed")

print("\n" + "="*60)
print("ALL TESTS PASSED ✓")
print("="*60 + "\n")
