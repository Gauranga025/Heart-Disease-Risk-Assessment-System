import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Heart Disease Predictor",
    page_icon="❤️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    color: #e63946;
    margin-bottom: 0.5rem;
}

.subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: #6c757d;
    margin-bottom: 2rem;
}

.stButton > button {
    width: 100%;
    background-color: #e63946;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    height: 3rem;
    border: none;
}

.stButton > button:hover {
    background-color: #d62839;
    color: white;
}

.result-card {
    padding: 20px;
    border-radius: 15px;
    margin-top: 15px;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 30px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL FILES ----------------
model = joblib.load("knn_heart_model.pkl")
scaler = joblib.load("heart_scaler.pkl")
expected_columns = joblib.load("heart_columns.pkl")

# ---------------- HEADER ----------------
st.markdown(
    '<div class="title">❤️ AI-Powered Heart Disease Prediction System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Enter patient details below to assess heart disease risk using a trained KNN Machine Learning Model.</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    age = st.slider("👤 Age", 18, 100, 40)

    sex = st.selectbox(
        "⚧ Sex",
        ["M", "F"]
    )

    chest_pain = st.selectbox(
        "💓 Chest Pain Type",
        ["ATA", "NAP", "TA", "ASY"]
    )

    resting_bp = st.number_input(
        "🩺 Resting Blood Pressure (mm Hg)",
        min_value=80,
        max_value=200,
        value=120
    )

    cholesterol = st.number_input(
        "🧪 Cholesterol (mg/dL)",
        min_value=100,
        max_value=600,
        value=200
    )

    fasting_bs = st.selectbox(
        "🍬 Fasting Blood Sugar > 120 mg/dL",
        [0, 1]
    )

with col2:
    resting_ecg = st.selectbox(
        "📈 Resting ECG",
        ["Normal", "ST", "LVH"]
    )

    max_hr = st.slider(
        "❤️ Maximum Heart Rate",
        60,
        220,
        150
    )

    exercise_angina = st.selectbox(
        "🏃 Exercise-Induced Angina",
        ["Y", "N"]
    )

    oldpeak = st.slider(
        "📉 Oldpeak (ST Depression)",
        0.0,
        6.0,
        1.0
    )

    st_slope = st.selectbox(
        "📊 ST Slope",
        ["Up", "Flat", "Down"]
    )

# ---------------- PATIENT SUMMARY ----------------
st.markdown("## 📋 Patient Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Age", age)

with c2:
    st.metric("Blood Pressure", resting_bp)

with c3:
    st.metric("Cholesterol", cholesterol)

with c4:
    st.metric("Max HR", max_hr)

st.markdown("")

# ---------------- PREDICTION BUTTON ----------------
if st.button("🔍 Predict Heart Disease Risk"):

    raw_input = {
        'Age': age,
        'RestingBP': resting_bp,
        'Cholesterol': cholesterol,
        'FastingBS': fasting_bs,
        'MaxHR': max_hr,
        'Oldpeak': oldpeak,
        'Sex_' + sex: 1,
        'ChestPainType_' + chest_pain: 1,
        'RestingECG_' + resting_ecg: 1,
        'ExerciseAngina_' + exercise_angina: 1,
        'ST_Slope_' + st_slope: 1
    }

    input_df = pd.DataFrame([raw_input])

    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[expected_columns]

    scaled_input = scaler.transform(input_df)

    with st.spinner("Analyzing patient data..."):
        prediction = model.predict(scaled_input)[0]

    st.markdown("---")

    if prediction == 1:

        st.error("⚠️ HIGH RISK OF HEART DISEASE DETECTED")

        st.markdown("""
### 🚨 Recommendations

- Consult a cardiologist as soon as possible.
- Monitor blood pressure regularly.
- Follow a heart-healthy diet.
- Reduce cholesterol levels if necessary.
- Exercise only under proper medical guidance.
- Schedule regular health checkups.
""")

    else:

        st.success("✅ LOW RISK OF HEART DISEASE DETECTED")

        st.markdown("""
### 🎉 Recommendations

- Continue maintaining a healthy lifestyle.
- Exercise regularly.
- Follow a balanced diet.
- Monitor blood pressure periodically.
- Maintain healthy cholesterol levels.
- Continue routine medical checkups.
""")

# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown(
    '<div class="footer">Built with Streamlit • Machine Learning Powered ❤️</div>',
    unsafe_allow_html=True
)

