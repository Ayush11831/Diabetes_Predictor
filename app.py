from flask import Flask, render_template, request, jsonify, session, make_response
from fpdf import FPDF
import pickle
import os
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load models
def load_models():
    with open('models/enhanced_model.pkl', 'rb') as f:
        enhanced = pickle.load(f)
    with open('models/old_model.pkl', 'rb') as f:
        old = pickle.load(f)
    return enhanced['model'], enhanced['accuracy'], old['model'], old['accuracy']

enhanced_model, enhanced_acc, old_model, old_acc = load_models()

# Language support
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch'
}

@app.route('/')
def welcome():
    lang = request.args.get('lang', 'en')
    return render_template('welcome.html', lang=lang, languages=SUPPORTED_LANGUAGES)

@app.route('/questionnaire')
def questionnaire():
    lang = request.args.get('lang', 'en')
    return render_template('questionnaire.html', lang=lang, languages=SUPPORTED_LANGUAGES)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Map form data to model features
        age_mapping = {
            'less than 40': 35,
            '40-49': 45,
            '50-59': 55,
            '60 or older': 65
        }
        
        features = [
            float(data['pregnancies']),
            120 if 'glucose' not in data else float(data['glucose']),  # Default value
            80 if 'bloodPressure' not in data else float(data['bloodPressure']),  # Default value
            20 if 'skinThickness' not in data else float(data['skinThickness']),  # Default value
            80 if 'insulin' not in data else float(data['insulin']),  # Default value
            float(data['bmi']),
            0.5 if 'diabetesPedigree' not in data else float(data['diabetesPedigree']),  # Default value
            age_mapping.get(data['age'], 45),  # Default to 45 if not found
            1 if data['frequentUrination'] == 'yes' else 0,
            1 if data['excessiveThirst'] == 'yes' else 0,
            1 if data['hunger'] == 'yes' else 0,
            1 if data['fatigue'] == 'yes' else 0,
            1 if data['blurredVision'] == 'yes' else 0,
            1 if data['slowHealing'] == 'yes' else 0,
            1 if data['tinglingNumbness'] == 'yes' else 0
        ]
        
        enhanced_pred = enhanced_model.predict_proba([features[:8]])[0][1] * 100
        old_pred = old_model.predict_proba([features[:8]])[0][1] * 100
        
        symptom_count = sum(features[8:])
        symptom_adjustment = symptom_count * 5
        
        session['results'] = {
            'enhanced_risk': min(enhanced_pred + symptom_adjustment, 100),
            'old_risk': min(old_pred + symptom_adjustment, 100),
            'enhanced_accuracy': enhanced_acc * 100,
            'old_accuracy': old_acc * 100,
            'symptom_count': symptom_count,
            'user_data': data
        }
        
        return jsonify(success=True)
    
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/results')
def results():
    lang = request.args.get('lang', 'en')
    return render_template('result.html', results=session.get('results'), lang=lang, languages=SUPPORTED_LANGUAGES)

@app.route('/generate_pdf')
def generate_pdf():
    results = session.get('results')
    if not results:
        return "No results to generate PDF", 400
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_draw_color(74, 110, 224)  # Blue border
    pdf.set_line_width(2)
    pdf.rect(5, 5, 500, 287)  # x, y, width, height
  
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Diabetes Risk Assessment Report", ln=1, align='C')
    pdf.ln(10)
    
    # Risk level
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Your Diabetes Risk Assessment:", ln=1)
    pdf.set_font("Arial", size=12)
    
    risk_level = ""
    if results['enhanced_risk'] < 30:
        risk_level = "Low Risk"
    elif results['enhanced_risk'] < 60:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"
    
    pdf.cell(200, 10, txt=f"Risk Percentage: {results['enhanced_risk']:.1f}% ({risk_level})", ln=1)
    pdf.ln(5)
    
    # Model comparison
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Model Comparison:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Enhanced model risk: {results['enhanced_risk']:.1f}% (Accuracy: {results['enhanced_accuracy']:.1f}%)", ln=1)
    pdf.cell(200, 10, txt=f"Basic model risk: {results['old_risk']:.1f}% (Accuracy: {results['old_accuracy']:.1f}%)", ln=1)
    pdf.ln(5)
    
    # Recommendations
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Recommendations:", ln=1)
    pdf.set_font("Arial", size=12)
    
    if results['enhanced_risk'] < 30:
        pdf.multi_cell(0, 10, txt="Maintain healthy lifestyle with balanced diet and regular exercise. Continue monitoring your health annually.")
    elif results['enhanced_risk'] < 60:
        pdf.multi_cell(0, 10, txt="Consider consulting a doctor and monitor your blood sugar levels regularly. Improve diet and increase physical activity.")
    else:
        pdf.multi_cell(0, 10, txt="Please consult a healthcare professional for proper diagnosis and treatment plan. Immediate lifestyle changes are recommended.")
    
    # User data
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Your Submitted Data:", ln=1)
    pdf.set_font("Arial", size=12)
    
    user_data = results['user_data']
    pdf.cell(200, 10, txt=f"Age: {user_data['age']}", ln=1)
    pdf.cell(200, 10, txt=f"BMI: {user_data['bmi']}", ln=1)
    pdf.cell(200, 10, txt=f"Glucose: {user_data.get('glucose', 'Not provided')}", ln=1)
    pdf.cell(200, 10, txt=f"Blood Pressure: {user_data.get('bloodPressure', 'Not provided')}", ln=1)
    pdf.cell(200, 10, txt=f"Symptoms reported: {results['symptom_count']}", ln=1)
    
    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, txt="-- Generated by Diabetes Risk Assessment Tool --", ln=1, align='C')
    
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers.set('Content-Disposition', 'attachment', filename='diabetes_risk_report.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

if __name__ == '__main__':
    app.run(debug=True)