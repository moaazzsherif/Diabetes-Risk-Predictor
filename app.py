import streamlit as st
import joblib
import numpy as np
import time
import plotly.graph_objects as go
import plotly.express as px

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DiabetesAI",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #050810 !important;
    font-family: 'DM Sans', sans-serif;
    color: #e8eaf0;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #0d1b3e 0%, #050810 50%),
                radial-gradient(ellipse at 80% 80%, #0a1628 0%, transparent 60%) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.block-container { padding: 2rem 1.5rem !important; max-width: 780px !important; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    animation: fadeDown 0.8s cubic-bezier(.16,1,.3,1) both;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 1.4rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}
.hero-badge::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #38bdf8;
    animation: pulse-dot 2s ease infinite;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 6vw, 3.8rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero h1 span {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    color: #64748b;
    font-size: 1rem;
    font-weight: 300;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Divider ── */
.fancy-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2rem 0;
    opacity: 0.4;
}
.fancy-divider::before, .fancy-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #334155, transparent);
}
.fancy-divider span { font-size: 0.65rem; letter-spacing: 0.2em; color: #475569; text-transform: uppercase; }

/* ── Card ── */
.card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(20px);
    animation: fadeUp 0.6s cubic-bezier(.16,1,.3,1) both;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.3), transparent);
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.card-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(56,189,248,0.15);
}

/* ── Streamlit inputs override ── */
[data-testid="stNumberInput"] label,
[data-testid="stSlider"] label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    letter-spacing: 0.04em !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(56,189,248,0.4) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.08) !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    border: none !important;
    border-radius: 14px !important;
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
    margin-top: 0.5rem !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 20px 40px rgba(14,165,233,0.25) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── Result Cards ── */
.result-high {
    background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(239,68,68,0.04));
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    animation: scaleIn 0.5s cubic-bezier(.16,1,.3,1) both;
    position: relative;
    overflow: hidden;
}
.result-low {
    background: linear-gradient(135deg, rgba(34,197,94,0.12), rgba(34,197,94,0.04));
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    animation: scaleIn 0.5s cubic-bezier(.16,1,.3,1) both;
    position: relative;
    overflow: hidden;
}
.result-icon {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    display: block;
    animation: bounceIn 0.6s cubic-bezier(.16,1,.3,1) 0.2s both;
}
.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}
.result-title-high { color: #f87171; }
.result-title-low  { color: #4ade80; }
.result-sub {
    color: #64748b;
    font-size: 0.9rem;
    font-weight: 300;
    margin-bottom: 2rem;
}

/* ── Probability Ring ── */
.prob-ring-wrap {
    display: flex;
    justify-content: center;
    margin: 1.5rem 0;
}
.prob-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #475569;
    margin-top: 1.2rem;
}

/* ── Stats Row ── */
.stats-row {
    display: flex;
    gap: 12px;
    margin-top: 1.5rem;
    justify-content: center;
    flex-wrap: wrap;
}
.stat-chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.78rem;
    color: #94a3b8;
    font-weight: 400;
}
.stat-chip strong {
    display: block;
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
}

/* ── Progress Bar ── */
.prog-wrap { margin: 1rem 0; }
.prog-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: #475569;
    margin-bottom: 6px;
}
.prog-track {
    background: rgba(255,255,255,0.06);
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
}
.prog-fill-high {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #f87171, #ef4444);
    transition: width 1s cubic-bezier(.16,1,.3,1);
}
.prog-fill-low {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #4ade80, #22c55e);
    transition: width 1s cubic-bezier(.16,1,.3,1);
}

/* ── Dashboard ── */
.dash-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.dash-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(129,140,248,0.15);
}
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 1.2rem;
}
.metric-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1rem 0.8rem;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-box:hover { border-color: rgba(129,140,248,0.25); }
.metric-box .val {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    display: block;
    margin-bottom: 2px;
}
.metric-box .lbl {
    font-size: 0.68rem;
    color: #475569;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.metric-box .status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    margin-right: 4px;
    vertical-align: middle;
}
.normal  { color: #4ade80; }
.warning { color: #facc15; }
.danger  { color: #f87171; }

.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #1e293b;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
}

/* ── Animations ── */
@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.92); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes bounceIn {
    0%   { opacity: 0; transform: scale(0.3); }
    60%  { transform: scale(1.1); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.7); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
</style>
""", unsafe_allow_html=True)

# ─── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model  = joblib.load("xgboost_fe.pkl")
    scaler = joblib.load("scaler_fe.pkl")
    return model, scaler

try:
    model, scaler = load_artifacts()
    model_loaded = True
except:
    model_loaded = False

# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Powered · XGBoost Model</div>
    <h1>Diabetes<br><span>Risk Predictor</span></h1>
    <p>Enter patient vitals below for an instant, intelligent assessment powered by machine learning.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"><span>Patient Data</span></div>', unsafe_allow_html=True)

# ─── Input Cards ───────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">🫀 Vital Signs</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: Glucose       = st.number_input("Glucose (mg/dL)",   0, 300, 110)
with c2: BloodPressure = st.number_input("Blood Pressure",     0, 200, 72)
with c3: Insulin       = st.number_input("Insulin (μU/mL)",   0, 900, 80)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-title">📋 Physical Metrics</div>', unsafe_allow_html=True)
c4, c5, c6 = st.columns(3)
with c4: BMI           = st.number_input("BMI",                0.0, 70.0, 25.0, step=0.1)
with c5: SkinThickness = st.number_input("Skin Thickness (mm)",0, 100, 20)
with c6: Age           = st.number_input("Age",                1, 120, 30)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-title">🧬 Clinical History</div>', unsafe_allow_html=True)
c7, c8 = st.columns(2)
with c7: Pregnancies   = st.number_input("Pregnancies",        0, 20, 1)
with c8: DPF           = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.47, step=0.01)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Predict Button ────────────────────────────────────────────────────────────
predict = st.button("⚡  Run Prediction", use_container_width=True)

# ─── Result ────────────────────────────────────────────────────────────────────
if predict:
    if not model_loaded:
        st.error("⚠️ Model files not found. Make sure `xgboost_fe.pkl` and `scaler_fe.pkl` are in the same directory.")
    else:
        with st.spinner(""):
            time.sleep(0.8)

        # Feature Engineering
        Glucose_BMI     = Glucose * BMI
        Glucose_Age     = Glucose * Age
        BMI_Age         = BMI * Age
        Insulin_Glucose = Insulin / (Glucose + 1)

        input_data   = np.array([[Pregnancies, Glucose, BloodPressure, SkinThickness,
                                   Insulin, BMI, DPF, Age,
                                   Glucose_BMI, Glucose_Age, BMI_Age, Insulin_Glucose]])
        input_scaled = scaler.transform(input_data)
        prediction   = model.predict(input_scaled)[0]
        probability  = model.predict_proba(input_scaled)[0][1]
        pct          = probability * 100
        risk_label   = "High" if pct >= 70 else "Moderate" if pct >= 40 else "Low"

        st.markdown('<div class="fancy-divider"><span>Prediction Result</span></div>', unsafe_allow_html=True)

        if prediction == 1:
            st.markdown(f"""
            <div class="result-high">
                <span class="result-icon">⚠️</span>
                <div class="result-title result-title-high">High Diabetes Risk</div>
                <div class="result-sub">This patient shows significant indicators of diabetes.</div>
                <div class="prog-wrap">
                    <div class="prog-label"><span>Risk Level</span><span>{pct:.1f}%</span></div>
                    <div class="prog-track"><div class="prog-fill-high" style="width:{pct}%"></div></div>
                </div>
                <div class="stats-row">
                    <div class="stat-chip"><strong>{pct:.1f}%</strong>Probability</div>
                    <div class="stat-chip"><strong>{risk_label}</strong>Risk Level</div>
                    <div class="stat-chip"><strong>XGB+FE</strong>Model Used</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-low">
                <span class="result-icon">✅</span>
                <div class="result-title result-title-low">Low Diabetes Risk</div>
                <div class="result-sub">This patient shows minimal indicators of diabetes.</div>
                <div class="prog-wrap">
                    <div class="prog-label"><span>Risk Level</span><span>{pct:.1f}%</span></div>
                    <div class="prog-track"><div class="prog-fill-low" style="width:{pct}%"></div></div>
                </div>
                <div class="stats-row">
                    <div class="stat-chip"><strong>{pct:.1f}%</strong>Probability</div>
                    <div class="stat-chip"><strong>{risk_label}</strong>Risk Level</div>
                    <div class="stat-chip"><strong>XGB+FE</strong>Model Used</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:1rem; padding: 1rem 1.5rem;
                    background: rgba(255,255,255,0.02);
                    border: 1px solid rgba(255,255,255,0.05);
                    border-radius: 12px; font-size: 0.78rem; color: #334155; line-height: 1.6;">
            ⚕️ <strong style="color:#475569">Medical Disclaimer:</strong>
            This tool is for educational purposes only and does not constitute medical advice.
            Always consult a qualified healthcare professional.
        </div>
        """, unsafe_allow_html=True)

        # ── Medical ranges ──────────────────────────────────────────
        def classify(val, low, high):
            if val < low:   return "warning", "Low"
            elif val > high: return "danger",  "High"
            else:            return "normal",  "Normal"

        g_cls, g_lbl = classify(Glucose, 70, 140)
        b_cls, b_lbl = classify(BloodPressure, 60, 90)
        i_cls, i_lbl = classify(Insulin, 16, 166)
        bmi_cls, bmi_lbl = classify(BMI, 18.5, 24.9)

        st.markdown('<div class="fancy-divider"><span>Patient Dashboard</span></div>', unsafe_allow_html=True)

        # ── Metric Grid ─────────────────────────────────────────────
        st.markdown(f"""
        <div class="card">
            <div class="dash-title">📊 Vitals Overview</div>
            <div class="metric-grid">
                <div class="metric-box">
                    <span class="val {g_cls}">{Glucose}</span>
                    <span class="lbl"><span class="status-dot" style="background:{'#4ade80' if g_cls=='normal' else '#facc15' if g_cls=='warning' else '#f87171'}"></span>Glucose</span>
                    <div style="font-size:0.65rem;color:#334155;margin-top:4px">{g_lbl} · 70–140</div>
                </div>
                <div class="metric-box">
                    <span class="val {b_cls}">{BloodPressure}</span>
                    <span class="lbl"><span class="status-dot" style="background:{'#4ade80' if b_cls=='normal' else '#facc15' if b_cls=='warning' else '#f87171'}"></span>Blood Pressure</span>
                    <div style="font-size:0.65rem;color:#334155;margin-top:4px">{b_lbl} · 60–90</div>
                </div>
                <div class="metric-box">
                    <span class="val {i_cls}">{Insulin}</span>
                    <span class="lbl"><span class="status-dot" style="background:{'#4ade80' if i_cls=='normal' else '#facc15' if i_cls=='warning' else '#f87171'}"></span>Insulin</span>
                    <div style="font-size:0.65rem;color:#334155;margin-top:4px">{i_lbl} · 16–166</div>
                </div>
                <div class="metric-box">
                    <span class="val {bmi_cls}">{BMI:.1f}</span>
                    <span class="lbl"><span class="status-dot" style="background:{'#4ade80' if bmi_cls=='normal' else '#facc15' if bmi_cls=='warning' else '#f87171'}"></span>BMI</span>
                    <div style="font-size:0.65rem;color:#334155;margin-top:4px">{bmi_lbl} · 18.5–24.9</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Radar Chart ─────────────────────────────────────────────
        radar_col, fi_col = st.columns(2)

        with radar_col:
            # Normalize each feature to 0-100 for radar
            def norm(val, mn, mx): return min(100, max(0, (val - mn) / (mx - mn) * 100))

            categories = ['Glucose', 'Blood\nPressure', 'Insulin', 'BMI', 'Age', 'Pregnancies']
            values = [
                norm(Glucose, 0, 300),
                norm(BloodPressure, 0, 200),
                norm(Insulin, 0, 900),
                norm(BMI, 0, 70),
                norm(Age, 1, 120),
                norm(Pregnancies, 0, 20),
            ]
            values_closed = values + [values[0]]
            categories_closed = categories + [categories[0]]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                fillcolor='rgba(129,140,248,0.15)',
                line=dict(color='#818cf8', width=2),
                name='Patient'
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=[50]*7,
                theta=categories_closed,
                fill='toself',
                fillcolor='rgba(255,255,255,0.02)',
                line=dict(color='rgba(255,255,255,0.08)', width=1, dash='dot'),
                name='Average'
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0, 100],
                                   gridcolor='rgba(255,255,255,0.05)',
                                   tickfont=dict(color='#334155', size=9)),
                    angularaxis=dict(gridcolor='rgba(255,255,255,0.06)',
                                    tickfont=dict(color='#94a3b8', size=10))
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                legend=dict(font=dict(color='#64748b', size=10),
                            bgcolor='rgba(0,0,0,0)'),
                margin=dict(t=30, b=20, l=40, r=40),
                title=dict(text='Feature Radar', font=dict(color='#818cf8', size=11,
                           family='Syne'), x=0.5)
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

        # ── Feature Importance Bar ───────────────────────────────────
        with fi_col:
            features  = ['Glucose', 'BMI', 'Pregnancies', 'DPF', 'BloodPressure', 'Insulin', 'Age', 'SkinThick']
            patient_v = [Glucose, BMI, Pregnancies, DPF, BloodPressure, Insulin, Age, SkinThickness]
            # Normalize to 0-1 for display
            maxv = [300, 70, 20, 3, 200, 900, 120, 100]
            norm_v = [round(v/m*100, 1) for v, m in zip(patient_v, maxv)]

            bar_colors = ['#f87171' if n > 65 else '#facc15' if n > 40 else '#4ade80' for n in norm_v]

            fig_bar = go.Figure(go.Bar(
                x=norm_v,
                y=features,
                orientation='h',
                marker=dict(color=bar_colors, line=dict(width=0)),
                text=[f'{v}' for v in norm_v],
                textposition='outside',
                textfont=dict(color='#64748b', size=10)
            ))
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(range=[0, 120], gridcolor='rgba(255,255,255,0.04)',
                           tickfont=dict(color='#334155', size=9),
                           title=dict(text='Relative Value (%)', font=dict(color='#475569', size=9))),
                yaxis=dict(gridcolor='rgba(0,0,0,0)',
                           tickfont=dict(color='#94a3b8', size=10)),
                margin=dict(t=30, b=20, l=10, r=50),
                title=dict(text='Patient Values (%)', font=dict(color='#818cf8', size=11,
                           family='Syne'), x=0.5)
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

        # ── Gauge Chart ─────────────────────────────────────────────
        gauge_color = "#ef4444" if pct >= 70 else "#facc15" if pct >= 40 else "#22c55e"
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(pct, 1),
            delta={'reference': 50, 'valueformat': '.1f',
                   'font': {'color': '#64748b', 'size': 13}},
            number={'suffix': '%', 'font': {'color': '#e2e8f0', 'size': 32, 'family': 'Syne'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#334155',
                         'tickfont': {'color': '#475569', 'size': 10}},
                'bar': {'color': gauge_color, 'thickness': 0.25},
                'bgcolor': 'rgba(255,255,255,0.03)',
                'bordercolor': 'rgba(255,255,255,0.06)',
                'steps': [
                    {'range': [0,  40], 'color': 'rgba(34,197,94,0.08)'},
                    {'range': [40, 70], 'color': 'rgba(250,204,21,0.08)'},
                    {'range': [70,100], 'color': 'rgba(239,68,68,0.08)'},
                ],
                'threshold': {
                    'line': {'color': gauge_color, 'width': 3},
                    'thickness': 0.85,
                    'value': pct
                }
            },
            title={'text': 'Diabetes Probability Gauge',
                   'font': {'color': '#818cf8', 'size': 11, 'family': 'Syne'}}
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            height=250,
            margin=dict(t=50, b=10, l=30, r=30)
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div class="footer">DiabetesAI · Built with XGBoost + Streamlit</div>', unsafe_allow_html=True)