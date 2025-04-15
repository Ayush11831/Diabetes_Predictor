import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

def preprocess_2019_data(df):
    # Convert categorical variables to numerical
    le = LabelEncoder()
    categorical_cols = ['Gender', 'Family_Diabetes', 'highBP', 'PhysicallyActive', 
                       'Smoking', 'Alcohol', 'RegularMedicine', 'JunkFood', 
                       'Stress', 'BPLevel', 'UriationFreq', 'Diabetic']
    
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])
    
    # Convert age ranges to numerical (taking the midpoint)
    age_mapping = {
        'less than 40': 35,
        '40-49': 45,
        '50-59': 55,
        '60 or older': 65
    }
    df['Age'] = df['Age'].map(age_mapping)
    
    # Select and rename relevant columns to match PIMA dataset
    df = df.rename(columns={
        'Age': 'Age',
        'BMI': 'BMI',
        'Pregancies': 'Pregnancies',
        'Diabetic': 'Outcome'
    })
    
    # Add missing columns with default values (since 2019 dataset doesn't have them)
    df['Glucose'] = 120  # Default value, could be imputed differently
    df['BloodPressure'] = 80
    df['SkinThickness'] = 20
    df['Insulin'] = 80
    df['DiabetesPedigreeFunction'] = 0.5
    
    return df[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
              'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']]

def create_datasets():
    os.makedirs('datasets', exist_ok=True)
    
    # Load the full Pima dataset from the CSV file
    dataset1 = pd.read_csv('datasets/dataset1.csv')
    
    # Save Pima dataset
    dataset1.to_csv('datasets/dataset1.csv', index=False)
    
    # Save 2019 dataset (we'll load it directly in train_models)

def train_models():
    os.makedirs('models', exist_ok=True)
    
    # Load Pima dataset - now with all entries
    df1 = pd.read_csv('datasets/dataset1.csv')
    
    # Load and preprocess 2019 dataset if available
    # Note: You'll need to have this file in your datasets folder
    try:
        df_2019 = pd.read_csv('datasets/diabetes_dataset__2019.csv')
        df2 = preprocess_2019_data(df_2019)
        # Combine datasets
        combined = pd.concat([df1, df2]).dropna()
    except FileNotFoundError:
        print("2019 dataset not found, using only Pima dataset")
        combined = df1
    
    # Split data
    X_combined = combined.drop('Outcome', axis=1)
    y_combined = combined['Outcome']
    X_train_combined, X_test_combined, y_train_combined, y_test_combined = train_test_split(
        X_combined, y_combined, test_size=0.3, random_state=42)
    
    # Train enhanced model (combined dataset)
    model_combined = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model_combined.fit(X_train_combined, y_train_combined)
    accuracy_combined = accuracy_score(y_test_combined, model_combined.predict(X_test_combined))
    
    # Train old model (only Pima dataset)
    X_pima = df1.drop('Outcome', axis=1)
    y_pima = df1['Outcome']
    X_train_pima, X_test_pima, y_train_pima, y_test_pima = train_test_split(
        X_pima, y_pima, test_size=0.3, random_state=42)
    
    model_pima = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model_pima.fit(X_train_pima, y_train_pima)
    accuracy_pima = accuracy_score(y_test_pima, model_pima.predict(X_test_pima))
    
    # Save models
    with open('models/enhanced_model.pkl', 'wb') as f:
        pickle.dump({'model': model_combined, 'accuracy': accuracy_combined}, f)
    
    with open('models/old_model.pkl', 'wb') as f:
        pickle.dump({'model': model_pima, 'accuracy': accuracy_pima}, f)
    
    # Create accuracy comparison visualization
    plt.figure(figsize=(8, 6))
    models = ['Combined Dataset Model', 'Pima Dataset Model']
    accuracies = [accuracy_combined, accuracy_pima]
    colors = ['#4c72b0', '#dd8452']
    
    bars = plt.bar(models, accuracies, color=colors)
    plt.ylabel('Accuracy')
    plt.title('Model Accuracy Comparison')
    plt.ylim(0, 1)
    
    # Add accuracy values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom')
    
    # Save the plot
    plt.savefig('static/model_comparison.png')
    plt.close()
    
    print(f"Combined model accuracy: {accuracy_combined:.2f}")
    print(f"Pima model accuracy: {accuracy_pima:.2f}")
    print(f"Number of entries in Pima dataset: {len(df1)}")
    if 'df2' in locals():
        print(f"Number of entries in 2019 dataset: {len(df2)}")
        print(f"Total entries in combined dataset: {len(combined)}")

if __name__ == '__main__':
    create_datasets()
    train_models()