import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

st.set_page_config(
    page_title="Mental Health Risk Profile App",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Styling
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700&family=Lato:ital,wght@0,300;0,400;0,700;1,300&display=swap');

:root {
    --lavender:      #EAE6F8;
    --lavender-mid:  #C9BFF0;
    --lavender-deep: #9B8DC4;
    --blush:         #F8E6EC;
    --blush-mid:     #EDAFC8;
    --mint:          #E2F4EF;
    --mint-mid:      #A8D8C8;
    --sky:           #E3F0FA;
    --sky-mid:       #A3C8E8;
    --peach:         #FDF0E6;
    --white:         #FDFCFF;
    --text-dark:     #3A3550;
    --text-mid:      #6B6480;
    --text-light:    #9B94B0;
    --border:        rgba(155,141,196,0.18);
    --shadow-soft:   0 2px 20px rgba(100,80,160,0.07);
    --shadow-card:   0 4px 28px rgba(100,80,160,0.10);
}

/* ── Base ── */
html, body, [class*="css"], .stApp {
    font-family: 'Nunito', sans-serif !important;
    color: var(--text-dark);
}

.stApp {
    background:
        radial-gradient(ellipse 70% 50% at 5% 0%,   rgba(234,230,248,0.55) 0%, transparent 55%),
        radial-gradient(ellipse 50% 60% at 95% 100%, rgba(226,244,239,0.45) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 60% 50%,  rgba(248,230,236,0.20) 0%, transparent 50%),
        #FDFCFF !important;
}

/* ── Fix ALL widget text and select color ── */
label, .stSelectbox label, .stSlider label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] {
    color: var(--text-dark) !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
}

/* Selectbox box */
.stSelectbox > div > div,
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--lavender-mid) !important;
    border-radius: 10px !important;
    color: var(--text-dark) !important;
}

/* Selected value text */
[data-baseweb="select"] span,
[data-baseweb="select"] div,
[data-baseweb="select"] p {
    color: var(--text-dark) !important;
    font-family: 'Nunito', sans-serif !important;
}

/* Dropdown list */
[data-baseweb="popover"] li,
[data-baseweb="menu"] li,
[role="option"],
[data-baseweb="popover"] *,
[data-baseweb="menu"] * {
    color: var(--text-dark) !important;
    font-family: 'Nunito', sans-serif !important;
    background-color: #FFFFFF !important;
}
[role="option"]:hover,
[data-baseweb="menu"] [aria-selected="true"] {
    background-color: var(--lavender) !important;
}

/* ── Typography ── */
h1, h2, h3 {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-dark) !important;
}

/* ── Hero ── */
.hero-wrap {
    background: linear-gradient(135deg, #C9BFF0 0%, #EDAFC8 55%, #A8D8C8 100%);
    border-radius: 20px;
    padding: 48px 52px 44px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 6px 40px rgba(155,141,196,0.25);
}
.hero-wrap::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,0.15);
    pointer-events: none;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: rgba(255,255,255,0.10);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(58,53,80,0.70);
    margin-bottom: 12px;
}
.hero-title {
    font-family: 'Nunito', sans-serif;
    font-size: 2.7rem;
    font-weight: 700;
    color: #3A3550;
    line-height: 1.15;
    margin: 0 0 14px;
}
.hero-sub {
    font-family: 'Lato', sans-serif;
    font-size: 0.96rem;
    font-weight: 400;
    color: rgba(58,53,80,0.78);
    max-width: 560px;
    line-height: 1.72;
}
.hero-pill {
    display: inline-block;
    margin-top: 20px;
    background: rgba(255,255,255,0.45);
    border: 1px solid rgba(255,255,255,0.70);
    border-radius: 100px;
    padding: 5px 16px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.10em;
    color: var(--text-dark);
}

/* ── Image strip ── */
.img-strip {
    display: flex;
    gap: 12px;
    height: 130px;
    margin-bottom: 28px;
}
.img-strip-item {
    flex: 1;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: var(--shadow-soft);
}
.img-strip-item img {
    width: 100%; height: 100%;
    object-fit: cover;
    filter: saturate(0.78) brightness(1.05);
    transition: transform 0.5s ease, filter 0.4s ease;
}
.img-strip-item:hover img {
    transform: scale(1.05);
    filter: saturate(0.95) brightness(1.06);
}

/* ── Divider ── */
.soft-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lavender-mid), transparent);
    margin: 24px 0;
    opacity: 0.55;
}

/* ── Section label ── */
.sec-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--lavender-deep);
    margin-bottom: 4px;
}
.sec-title {
    font-family: 'Nunito', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--text-dark);
    margin: 0 0 16px;
}

/* ── Form card ── */
div[data-testid="stForm"] {
    background: rgba(255,255,255,0.82) !important;
    border: 1.5px solid rgba(201,191,240,0.35) !important;
    border-radius: 20px !important;
    padding: 32px !important;
    box-shadow: var(--shadow-card) !important;
}

.col-header {
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: var(--lavender-deep);
    padding-bottom: 10px;
    border-bottom: 1.5px solid rgba(201,191,240,0.45);
    margin-bottom: 16px;
}

/* ── Submit / action buttons ── */
div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #D8CCF6 0%, #F4C7DA 100%) !important;
    color: #4A435F !important;
    border: 1px solid rgba(155,141,196,0.22) !important;
    border-radius: 12px !important;
    padding: 13px 36px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.93rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    width: 100% !important;
    box-shadow: 0 4px 18px rgba(155,141,196,0.18) !important;
    transition: all 0.25s ease !important;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #E6DBFA 0%, #F8D6E4 100%) !important;
    color: #3A3550 !important;
    border: 1px solid rgba(155,141,196,0.28) !important;
    box-shadow: 0 6px 22px rgba(155,141,196,0.24) !important;
    transform: translateY(-1px) !important;
}

div.stButton > button:focus,
div[data-testid="stFormSubmitButton"] > button:focus,
div.stButton > button:active,
div[data-testid="stFormSubmitButton"] > button:active {
    background: linear-gradient(135deg, #D8CCF6 0%, #F4C7DA 100%) !important;
    color: #4A435F !important;
    outline: none !important;
    box-shadow: 0 0 0 0.18rem rgba(201,191,240,0.35) !important;
}
}

/* ── st.metric ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.82) !important;
    border: 1.5px solid rgba(201,191,240,0.30) !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    box-shadow: var(--shadow-soft) !important;
}
[data-testid="stMetricLabel"] p {
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-mid) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-dark) !important;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
}

/* ── Expander ── */
.stExpander {
    border: 1.5px solid rgba(201,191,240,0.35) !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.78) !important;
}

/* ── Body text ── */
.stMarkdown p, p {
    font-family: 'Nunito', sans-serif !important;
    color: var(--text-dark) !important;
    line-height: 1.65 !important;
}

/* ── Caption ── */
[data-testid="stCaptionContainer"] p {
    font-family: 'Lato', sans-serif !important;
    font-size: 0.82rem !important;
    color: var(--text-light) !important;
}

/* ── Footer ── */
.footer-wrap {
    text-align: center;
    padding: 28px 0 12px;
    font-family: 'Lato', sans-serif;
    font-size: 0.80rem;
    color: var(--text-light);
    letter-spacing: 0.03em;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load saved artifacts
# --------------------------------------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load("depression_safe_model.joblib")
    features = joblib.load("depression_safe_features.joblib")
    return model, features

model, features = load_artifacts()

# --------------------------------------------------
# UI mappings
# --------------------------------------------------
age_map = {
    "15–19": 1, "20–24": 2, "25–34": 3, "35–44": 4,
    "45–54": 5, "55–64": 6, "65+": 7
}
gender_map = {"Male": 1, "Female": 2}
education_map = {
    "Less than secondary school graduation": 1,
    "Secondary school graduation": 2,
    "Some postsecondary": 3,
    "Postsecondary certificate/diploma": 4,
    "University below bachelor's": 5,
    "Bachelor's degree": 6,
    "Above bachelor's degree": 7
}
employment_map = {
    "Worked last week": 1,
    "Did not work last week": 2,
    "Has job but absent from work": 3,
    "Permanent inability to work": 4,
    "Other": 5,
    "Not applicable / not in labour force": 6
}
activity_map = {"Active in past 7 days": 1, "Not active in past 7 days": 2}
stress_map = {
    "Not at all stressful": 1, "Not very stressful": 2,
    "A bit stressful": 3, "Quite a bit stressful": 4, "Extremely stressful": 5
}
coping_map = {"Excellent": 1, "Very good": 2, "Good": 3, "Fair": 4, "Poor": 5}
support_map = {
    "Strongly agree": 1, "Agree": 2,
    "Neither agree nor disagree": 3, "Disagree": 4, "Strongly disagree": 5
}

# --------------------------------------------------
# Helper functions (unchanged from original)
# --------------------------------------------------
def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def scale_relative_score(prob: float, low_anchor: float = 0.35, high_anchor: float = 1.00) -> float:
    scaled = (prob - low_anchor) / (high_anchor - low_anchor)
    return clamp01(scaled)

def get_relative_risk_label(prob: float) -> str:
    if prob < 0.50:
        return "Low Relative Risk"
    elif prob < 0.75:
        return "Moderate Relative Risk"
    return "High Relative Risk"

def show_banner(label: str):
    if label == "High Relative Risk":
        st.error("High Relative Risk Profile")
    elif label == "Moderate Relative Risk":
        st.warning("Moderate Relative Risk Profile")
    else:
        st.success("Low Relative Risk Profile")

def build_radar_scores(inp):
    return {
        "Life Satisfaction":  max(0, min(100, inp["GEN_02B"] * 10)),
        "Social Support":     max(0, min(100, 100 - inp["SPSDCON"])),
        "Stress Resilience":  {1: 95, 2: 80, 3: 60, 4: 35, 5: 10}[inp["GEN_07"]],
        "Coping Capacity":    {1: 95, 2: 80, 3: 60, 4: 35, 5: 10}[inp["STS_1"]],
        "Trusted Support":    {1: 95, 2: 80, 3: 55, 4: 30, 5: 10}[inp["STS_4"]],
        "Social Climate":     max(0, min(100, 100 - inp["NSIDSC"] * 8)),
        "Functioning":        max(0, min(100, 100 - inp["DASGSCR"] * 2))
    }

def pretty_feature_name(feature_name: str) -> str:
    mapping = {
        "num__NSIDSC": "Negative social interaction",
        "num__DASGSCR": "Functional difficulty",
        "num__GEN_02B": "Life satisfaction",
        "num__SPSDCON": "Low social support score",
        "cat__GEN_07_1.0": "Very low stress",
        "cat__GEN_07_2.0": "Low stress",
        "cat__GEN_07_3.0": "Moderate stress",
        "cat__GEN_07_4.0": "Quite a bit of stress",
        "cat__GEN_07_5.0": "Extreme stress",
        "cat__STS_1_1.0": "Excellent coping ability",
        "cat__STS_1_2.0": "Very good coping ability",
        "cat__STS_1_3.0": "Good coping ability",
        "cat__STS_1_4.0": "Fair coping ability",
        "cat__STS_1_5.0": "Poor coping ability",
        "cat__STS_4_1.0": "Strongly agree support is available",
        "cat__STS_4_2.0": "Agree support is available",
        "cat__STS_4_3.0": "Neutral perceived support",
        "cat__STS_4_4.0": "Disagree support is available",
        "cat__STS_4_5.0": "Strongly disagree support is available",
        "cat__PHSFPPA_1.0": "Recent physical activity",
        "cat__PHSFPPA_2.0": "No recent physical activity",
        "cat__LMAM_01_1.0": "Worked last week",
        "cat__LMAM_01_2.0": "Did not work last week",
        "cat__DHHGAGE_1.0": "Age 15–19",
        "cat__DHHGAGE_2.0": "Age 20–24",
        "cat__DHHGAGE_3.0": "Age 25–34",
        "cat__DHHGAGE_4.0": "Age 35–44",
        "cat__DHHGAGE_5.0": "Age 45–54",
        "cat__DHHGAGE_6.0": "Age 55–64",
        "cat__DHHGAGE_7.0": "Age 65+"
    }
    return mapping.get(feature_name, feature_name)

def get_top_model_factors(model, input_df, top_n=5):
    calibrated_model = model.named_steps["classifier"]
    base_model = calibrated_model.calibrated_classifiers_[0].estimator
    feature_names = model.named_steps["preprocessor"].get_feature_names_out()
    X_transformed = model.named_steps["preprocessor"].transform(input_df)
    if hasattr(X_transformed, "toarray"):
        x_row = X_transformed.toarray()[0]
    else:
        x_row = X_transformed[0]
    contributions = base_model.coef_[0] * x_row
    contrib_df = pd.DataFrame({"feature": feature_names, "contribution": contributions})
    contrib_df["abs_contribution"] = contrib_df["contribution"].abs()
    contrib_df = contrib_df.sort_values("abs_contribution", ascending=False).head(top_n).copy()
    contrib_df["pretty_name"] = contrib_df["feature"].apply(pretty_feature_name)
    return contrib_df

# ==================================================
# ── HEADER ──
# ==================================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">Psychosocial Wellbeing · Research Tool</div>
    <div class="hero-title">Depression Risk Profile App</div>
    <div class="hero-sub">
        This app estimates a <strong>relative depression risk profile</strong> using non-leaky demographic,
        social, behavioral, coping, and functioning variables. It is designed for
        <strong>comparative profile interpretation</strong>, not diagnosis.
    </div>
    <div class="hero-pill">Population-based &nbsp;·&nbsp; Non-clinical &nbsp;·&nbsp; Relative Risk Only</div>
</div>
""", unsafe_allow_html=True)

# ── Calming image strip
st.markdown("""
<div class="img-strip">
    <div class="img-strip-item">
        <img src="https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=1200&q=80&auto=format&fit=crop" alt="forest path">
    </div>
    <div class="img-strip-item">
        <img src="https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1200&q=80&auto=format&fit=crop" alt="peaceful meadow">
    </div>
    <div class="img-strip-item">
        <img src="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1200&q=80&auto=format&fit=crop" alt="calm water">
    </div>
    <div class="img-strip-item">
        <img src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&q=80&auto=format&fit=crop" alt="gentle beach">
    </div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# ── INPUT FORM ──
# ==================================================
st.markdown('<div class="sec-label">Step 01</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">Input Profile</div>', unsafe_allow_html=True)

with st.form("risk_form"):
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="col-header">Demographics &amp; Lifestyle</div>', unsafe_allow_html=True)
        age_label        = st.selectbox("Age Group", list(age_map.keys()))
        gender_label     = st.selectbox("Gender", list(gender_map.keys()))
        education_label  = st.selectbox("Education", list(education_map.keys()))
        employment_label = st.selectbox("Employment Status", list(employment_map.keys()))
        activity_label   = st.selectbox("Physical Activity", list(activity_map.keys()))
        life_satisfaction = st.slider(
            "Life Satisfaction (0 = very dissatisfied, 10 = very satisfied)",
            min_value=0, max_value=10, value=6
        )

    with right:
        st.markdown('<div class="col-header">Psychosocial &amp; Wellbeing</div>', unsafe_allow_html=True)
        social_support_raw = st.slider("Social Support Score (0–100)", 0, 100, 50)
        stress_label    = st.selectbox("Perceived Life Stress", list(stress_map.keys()))
        coping_label    = st.selectbox("Ability to Handle Unexpected Problems", list(coping_map.keys()))
        support_label   = st.selectbox("Can Count on People When Dealing With Stress", list(support_map.keys()))
        negative_social  = st.slider("Negative Social Interaction", 0, 12, 3)
        disability_score = st.slider("Functional Difficulty Score", 0, 50, 10)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Analyze Profile")

# ==================================================
# ── RESULTS  (original logic — preserved exactly) ──
# ==================================================
if submitted:
    inp = {
        "DHHGAGE": age_map[age_label],
        "GENDER":  gender_map[gender_label],
        "EDU_05":  education_map[education_label],
        "LMAM_01": employment_map[employment_label],
        "PHSFPPA": activity_map[activity_label],
        "SPSDCON": 100 - social_support_raw,
        "GEN_02B": life_satisfaction,
        "GEN_07":  stress_map[stress_label],
        "STS_1":   coping_map[coping_label],
        "STS_4":   support_map[support_label],
        "NSIDSC":  negative_social,
        "DASGSCR": disability_score
    }

    input_df = pd.DataFrame([inp])[features]

    dep_prob  = model.predict_proba(input_df)[:, 1][0]
    dep_pred  = int(dep_prob >= 0.50)

    dep_index = scale_relative_score(dep_prob)
    label     = get_relative_risk_label(dep_prob)
    radar_scores   = build_radar_scores(inp)
    top_factors_df = get_top_model_factors(model, input_df, top_n=5)

    st.subheader("Risk Assessment")
    show_banner(label)

    st.caption(
        "This is a **relative risk model based on population patterns**, not a clinical diagnosis."
    )

    # Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Relative Risk Score", f"{dep_index * 100:.0f}/100")
    with m2:
        st.metric("Relative Risk Label", label)
    with m3:
        st.metric("Predicted Class (0.50 threshold)", dep_pred)

    st.write(
        f"This profile falls into the **{label.lower()}** range for the current model. "
        "The displayed score is a relative index built from the model output so that profile differences "
        "are easier to interpret."
    )

    with st.expander("Show raw model output"):
        st.write(f"Raw depression probability: **{dep_prob:.3f}**")
        st.write("Final classification threshold: **0.50**")

    # Main layout
    left, right = st.columns([1, 1.2])

    with left:
        st.subheader("Profile Summary")

        st.write(f"**Age group:** {age_label}")
        st.write(f"**Employment:** {employment_label}")
        st.write(f"**Physical activity:** {activity_label}")
        st.write(f"**Stress level:** {stress_label}")

        st.write("**Top contributing factors (model-based):**")
        for _, row in top_factors_df.iterrows():
            direction = "increasing" if row["contribution"] > 0 else "reducing"
            st.write(f"- {row['pretty_name']} is **{direction}** relative risk")

        st.info(
            "These explanations come from the trained model coefficients after preprocessing. "
            "They are intended to make the prediction more transparent."
        )

    with right:
        st.subheader("Psychosocial Profile Radar")
        st.caption("Higher values indicate more favorable conditions across the displayed dimensions.")

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=list(radar_scores.values()),
            theta=list(radar_scores.keys()),
            fill="toself",
            name="Profile",
            line=dict(color="#9B8DC4", width=2),
            fillcolor="rgba(155,141,196,0.18)"
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(234,230,248,0.30)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=9, color="#6B6480"),
                    gridcolor="rgba(155,141,196,0.20)",
                    linecolor="rgba(155,141,196,0.25)"
                ),
                angularaxis=dict(
                    tickfont=dict(size=10, family="Nunito", color="#3A3550"),
                    gridcolor="rgba(155,141,196,0.15)"
                )
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=30, r=30, t=30, b=30),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# ==================================================
# ── FOOTER ──
# ==================================================
st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer-wrap">
    Built with a calibrated logistic regression model using non-leaky demographic, social, behavioral,
    coping, and functioning variables.<br>
    This tool is for comparative profile exploration only &nbsp;·&nbsp; Not a clinical diagnostic instrument.
</div>
""", unsafe_allow_html=True)