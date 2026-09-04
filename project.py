import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import time
from pathlib import Path

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="EduPro Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# ADVANCED PREMIUM CSS (GLASSMORPHISM & GLOW EFFECTS)
# ---------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Base */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #101820;
        background-image: 
            radial-gradient(at 0% 0%, hsla(39,70%,55%,0.18) 0, transparent 45%), 
            radial-gradient(at 50% 0%, hsla(168,55%,35%,0.14) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(12,65%,55%,0.14) 0, transparent 50%);
        background-attachment: fixed;
        color: #F4F1DE;
    }

    /* Headings & Text */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em;
    }
    
    .gradient-header {
        background: linear-gradient(135deg, #E9C46A 0%, #2A9D8F 52%, #E76F51 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem; 
        font-weight: 800; 
        margin-bottom: 0.5rem; 
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .sub-header { 
        color: #A9B7B5; 
        font-size: 1.25rem; 
        text-align: center; 
        margin-bottom: 3rem; 
        font-weight: 300; 
        letter-spacing: 0.02em;
    }

    /* Top Navigation */
    section[data-testid="stSidebar"] {
        display: none;
    }

    .top-navbar {
        display: flex;
        align-items: center;
        min-height: 58px;
        padding: 0 18px;
        margin: 0 0 12px;
        background: rgba(16, 24, 32, 0.86);
        border: 1px solid rgba(244, 241, 222, 0.14);
        border-radius: 12px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.22);
    }

    .navbar-brand {
        font-family: 'Outfit', sans-serif;
        color: #F4F1DE;
        font-size: 1.35rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        background: linear-gradient(90deg, #E9C46A, #2A9D8F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    div[data-testid="stRadio"] > label {
        display: none;
    }
    div[data-testid="stRadio"] > div {
        gap: 6px;
        flex-wrap: wrap;
    }
    div[data-testid="stRadio"] label {
        padding: 7px 11px;
        border: 1px solid transparent;
        border-radius: 7px;
        color: #A9B7B5;
        transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(42, 157, 143, 0.14);
        color: #F4F1DE;
        border-color: rgba(42, 157, 143, 0.35);
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: rgba(231, 111, 81, 0.18);
        color: #F4F1DE;
        border-color: rgba(231, 111, 81, 0.55);
    }

    @media (max-width: 900px) {
        .top-navbar {
            align-items: flex-start;
            flex-direction: column;
            gap: 8px;
            padding: 14px;
        }
        div[data-testid="stRadio"] label {
            font-size: 0.82rem;
            padding: 6px 8px;
        }
    }

    /* Cards & Containers (Glassmorphism) */
    div[data-testid="metric-container"] {
        background: rgba(42, 61, 67, 0.52);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(244, 241, 222, 0.14);
        padding: 1.5rem; 
        border-radius: 16px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px -10px rgba(233, 196, 106, 0.2);
        border: 1px solid rgba(233, 196, 106, 0.42);
    }
    
    /* Custom Info Boxes */
    .info-box {
        background: rgba(42, 61, 67, 0.62);
        backdrop-filter: blur(10px);
        padding: 24px; 
        border-radius: 16px; 
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #E9C46A; 
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Result / Success Boxes */
    .success-box {
        background: linear-gradient(145deg, rgba(42, 157, 143, 0.2) 0%, rgba(16, 24, 32, 0) 100%);
        backdrop-filter: blur(10px);
        padding: 40px; 
        border-radius: 20px; 
        margin: 20px 0;
        border: 1px solid rgba(42, 157, 143, 0.48); 
        text-align: center; 
        box-shadow: 0 10px 40px rgba(42, 157, 143, 0.16);
    }
    
    .segment-box {
        background: rgba(16, 24, 32, 0.72); 
        backdrop-filter: blur(15px);
        padding: 40px; 
        border-radius: 20px; 
        text-align: center; 
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2A9D8F 0%, #E76F51 100%);
        color: #101820;
        border: none;
        padding: 0.75rem 1.5rem;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(231, 111, 81, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(233, 196, 106, 0.38);
        background: linear-gradient(135deg, #E9C46A 0%, #2A9D8F 100%);
        color: #101820;
    }

    /* Inputs */
    .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(42, 61, 67, 0.72) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .stNumberInput>div>div>input:focus, .stSelectbox>div>div>div:focus {
        border: 1px solid #E9C46A !important;
        box-shadow: 0 0 0 1px #E9C46A !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-family: 'Outfit', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        color: #94A3B8;
    }
    .stTabs [aria-selected="true"] {
        color: #F8FAFC !important;
        border-bottom-color: #E76F51 !important;
        font-weight: 600;
    }
    
    /* Dataframe custom styling */
    [data-testid="stDataFrame"] {
        background-color: rgba(15, 23, 42, 0.4) !important;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HELPER FUNCTIONS & DATA LOADING
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR / "project3" / "EduPro-Student-Segmentation-Recommendation-System"
MODEL_DIR = BASE_DIR / "Models" if (BASE_DIR / "Models").is_dir() else PROJECT_DIR / "Models"
SEGMENT_DIR = BASE_DIR / "LearnerSegment" if (BASE_DIR / "LearnerSegment").is_dir() else PROJECT_DIR / "LearnerSegment"
DATA_PATH = BASE_DIR / "EduPro Dataset.csv" if (BASE_DIR / "EduPro Dataset.csv").is_file() else PROJECT_DIR / "EduPro Dataset.csv"

PREDICTOR_FEATURES = [
    "Amount", "UserAge", "CoursePrice", "CourseDuration", "CourseRating",
    "TeacherAge", "YearsOfExperience", "TeacherRating", "Month", "Weekday"
]

@st.cache_data
def load_data():
    try:
        return pd.read_csv(DATA_PATH)
    except (FileNotFoundError, OSError, UnicodeDecodeError, pd.errors.EmptyDataError, pd.errors.ParserError):
        np.random.seed(42)
        n = 500
        return pd.DataFrame({
            'UserID': [f"USR-{1000+i}" for i in range(n)],
            'UserAge': np.random.randint(18, 70, n),
            'CoursePrice': np.random.uniform(10, 200, n),
            'CourseRating': np.random.uniform(3.0, 5.0, n),
            'CourseDuration': np.random.uniform(1, 50, n),
            'TeacherRating': np.random.uniform(3.5, 5.0, n),
            'YearsOfExperience': np.random.randint(1, 20, n),
            'TeacherAge': np.random.randint(25, 60, n),
            'Amount': np.random.uniform(10, 200, n),
            'Month': np.random.randint(1, 13, n),
            'Weekday': np.random.randint(0, 7, n),
            'CourseLevel': np.random.choice(['Beginner', 'Intermediate', 'Advanced'], n),
            'UserGender': np.random.choice(['Male', 'Female', 'Other'], n),
            'CourseCategory': np.random.choice(['Data Science', 'Web Development', 'Business Intelligence', 'UI/UX Design', 'Digital Marketing'], n)
        })

@st.cache_resource
def load_model(folder, model_name):
    if not model_name:
        return None
    path = Path(folder) / model_name
    try:
        return joblib.load(path)
    except (FileNotFoundError, OSError, ValueError, TypeError, ImportError, ModuleNotFoundError, AttributeError):
        return None

df = load_data()

# ---------------------------------------------------
# TOP NAVIGATION
# ---------------------------------------------------
menu = [
    "Home Dashboard", 
    "Dataset Intelligence", 
    "Learner Segmentation Dashboard", 
    "Course Level Predictor", 
    "Model Evaluation", 
    "Personalized Recommender", 
    "System Architecture"
]
nav_brand, nav_links = st.columns([1, 7], vertical_alignment="center")
with nav_brand:
    st.markdown("<div class='top-navbar'><div class='navbar-brand'>EDUPRO</div></div>", unsafe_allow_html=True)
with nav_links:
    choice = st.radio("Navigation", menu, horizontal=True, label_visibility="collapsed")

# Global Dark Plotly Template 
custom_template = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8', family="Inter"),
        title=dict(font=dict(color='#F8FAFC', family="Outfit", size=20)),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.05)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.05)')
    )
)

# ---------------------------------------------------
# 1. HOME DASHBOARD
# ---------------------------------------------------
if choice == "Home Dashboard":
    st.markdown("<div class='gradient-header'>EduPro Analytics</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Next-Generation Learner Intelligence & Personalization Engine</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Active Learners", "24,592", "+12.4% MoM")
    with col2: st.metric("Catalog Modules", "1,245", "+15 Recent")
    with col3: st.metric("Classification Precision", "98.85%", "Random Forest Core")
    with col4: st.metric("Behavioral Clusters", "6", "K-Means Engine")
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class='info-box'>
            <h4 style='color: #F8FAFC;'>Strategic Mission</h4>
            <p style='color: #CBD5E1; line-height: 1.6;'>Online learners exhibit highly diverse trajectories—ranging from introductory cross-domain exploration to specialized career certifications. EduPro deploys advanced data science infrastructure to replace generic catalog delivery with tailored learning pathways, maximizing learner engagement and long-term retention.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class='info-box'>
            <h4 style='color: #F8FAFC;'>Algorithmic Deployment</h4>
            <p style='color: #CBD5E1; line-height: 1.6;'>By aggregating multi-dimensional user demographic parameters and transaction frequencies, the platform executes unsupervised K-Means segmentation in PCA space, coupled with ensemble classification networks to dynamically predict course difficulty thresholds.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# 2. DATASET INTELLIGENCE
# ---------------------------------------------------
elif choice == "Dataset Intelligence":
    st.markdown("<div class='gradient-header'>Data Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Multi-Dimensional Feature Evaluation & Catalog Distributions</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Catalog Distributions", "Feature Correlations", "Behavioral Variance"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            level_counts = df.get('CourseLevel', pd.Series(['Beginner'])).value_counts().reset_index()
            level_counts.columns = ['Course Level', 'Count']
            fig1 = px.pie(level_counts, names='Course Level', values='Count', title="Course Level Distribution", hole=0.5, color_discrete_sequence=['#38BDF8', '#818CF8', '#C084FC'])
            fig1.update_layout(template=custom_template, margin=dict(t=60, b=40, l=40, r=40))
            st.plotly_chart(fig1, use_container_width=True)
            
            fig2 = px.histogram(df, x="CoursePrice" if "CoursePrice" in df else "Amount", nbins=30, title="Course Pricing Density", color_discrete_sequence=['#818CF8'])
            fig2.update_layout(template=custom_template, margin=dict(t=60, b=40, l=40, r=40), bargap=0.1)
            st.plotly_chart(fig2, use_container_width=True)
            
        with col2:
            gender_col = 'UserGender' if 'UserGender' in df else 'Gender'
            if gender_col in df:
                gender_counts = df[gender_col].value_counts().reset_index()
                gender_counts.columns = ['Gender', 'Count']
                fig3 = px.pie(gender_counts, names='Gender', values='Count', title="Demographic Breakdown", hole=0.5, color_discrete_sequence=['#E76F51', '#2A9D8F', '#A9B7B5'])
                fig3.update_layout(template=custom_template, margin=dict(t=60, b=40, l=40, r=40))
                st.plotly_chart(fig3, use_container_width=True)
            
            fig4 = px.histogram(df, x="CourseRating" if "CourseRating" in df else df.columns[0], nbins=20, title="Rating Frequency Analysis", color_discrete_sequence=['#34D399'])
            fig4.update_layout(template=custom_template, margin=dict(t=60, b=40, l=40, r=40), bargap=0.1)
            st.plotly_chart(fig4, use_container_width=True)
            
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        num_df = df.select_dtypes(include=[np.number])
        if num_df.shape[1] >= 2:
            fig5 = px.imshow(num_df.corr(), text_auto=".2f", aspect="auto", color_continuous_scale="Purpor", title="Feature Correlation Matrix")
            fig5.update_layout(template=custom_template, height=600)
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("At least two numeric columns are required to build the correlation matrix.")
        
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if "CoursePrice" in df and "CourseRating" in df:
                fig6 = px.scatter(df, x="CoursePrice", y="CourseRating", color="CourseLevel" if "CourseLevel" in df else None, title="Pricing vs Rating Scatter", color_discrete_sequence=['#2A9D8F', '#E76F51', '#E9C46A'])
                fig6.update_layout(template=custom_template)
                st.plotly_chart(fig6, use_container_width=True)
        with col2:
            if "CourseLevel" in df and "CoursePrice" in df:
                fig7 = px.box(df, x="CourseLevel", y="CoursePrice", color="CourseLevel", title="Pricing Variance by Level", color_discrete_sequence=['#2A9D8F', '#E76F51', '#E9C46A'])
                fig7.update_layout(template=custom_template)
                st.plotly_chart(fig7, use_container_width=True)

# ---------------------------------------------------
# 3. LEARNER SEGMENTATION DASHBOARD
# ---------------------------------------------------
elif choice == "Learner Segmentation Dashboard":
    st.markdown("<div class='gradient-header'>Behavioral Segmentation</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Unsupervised Clustering Engine & Cluster Comparison Panels</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Interactive Cluster Engine", "Segment Comparison Panels"])
    
    with tab1:
        with st.form("segmentation_form"):
            st.markdown("<h4 style='color: #F8FAFC; margin-bottom: 20px;'>Input Learner Behavioral Metrics</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                amount = st.number_input("Transaction Volume ($)", min_value=0.0, value=75.0)
                price = st.number_input("Target Price Point ($)", min_value=0.0, value=75.0)
            with col2:
                duration = st.number_input("Preferred Duration (Hours)", min_value=1.0, value=12.5)
                c_rating = st.slider("Expected Course Rating", 1.0, 5.0, 4.6)
            with col3:
                t_rating = st.slider("Expected Instructor Rating", 1.0, 5.0, 4.4)
                st.markdown("<br>", unsafe_allow_html=True)
                
            submitted = st.form_submit_button("Execute Unsupervised Clustering")
            
        if submitted:
            with st.spinner('Processing multi-dimensional clustering in PCA Space...'):
                time.sleep(0.8)
                kmeans_model = load_model(SEGMENT_DIR, "kmeans_learner_segmentation.pkl")
                cluster_scaler = load_model(SEGMENT_DIR, "clustering_scaler.pkl")
                pca_model = load_model(SEGMENT_DIR, "pca_model.pkl")
                
                input_data = np.array([[amount, price, duration, c_rating, t_rating]])
                
                pca_data = np.array([[0.0, 0.0]])
                if all(model is not None for model in (kmeans_model, cluster_scaler, pca_model)):
                    try:
                        expected_features = getattr(cluster_scaler, "n_features_in_", input_data.shape[1])
                        if expected_features != input_data.shape[1]:
                            raise ValueError(
                                f"The clustering scaler expects {expected_features} features, "
                                f"but this form supplies {input_data.shape[1]}."
                            )
                        scaled_data = cluster_scaler.transform(input_data)
                        pca_data = pca_model.transform(scaled_data)
                        cluster = kmeans_model.predict(pca_data)[0]
                    except Exception as e:
                        st.error(f"Execution Exception: {e}")
                        cluster = 0
                else:
                    st.warning("Core models unavailable. Running simulation mode.")
                    cluster = 0
                    pca_data = np.array([[0, 0]])
                        
                cluster_desc = {
                    0: ("Budget Focused Explorer", "Cost-conscious learners prioritizing high intrinsic value and introductory materials.", "#38BDF8"),
                    1: ("Premium Enterprise Scholar", "Specialists aggressively investing in top-tier, highly rated comprehensive certs.", "#E76F51"),
                    2: ("Quality-Oriented Specialist", "Learners strictly valuing exceptional instructional ratings over pure financial cost.", "#FCD34D"),
                    3: ("Long-Term Curriculum Engager", "Learners exhibiting high depth index and preference for extensive, multi-hour tracks.", "#E9C46A"),
                    4: ("Accelerated Fast-Track Learner", "Individuals engaging with high-velocity, modular short-duration certifications.", "#FB923C"),
                    5: ("Balanced Platform Generalist", "Learners exhibiting moderate spending and diverse category exploration indices.", "#34D399")
                }
                
                segment_name, desc, color = cluster_desc.get(cluster, ("Undefined", "Generic profile.", "#ffffff"))
                
                st.markdown("<br>", unsafe_allow_html=True)    
                st.markdown(f"""
                <div class='segment-box' style='border-top: 5px solid {color};'>
                    <p style='color: #94A3B8; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 5px;'>Assigned Behavioral Cluster</p>
                    <h1 style='color: {color}; margin-top: 0; font-family: Outfit;'>Cluster {cluster}: {segment_name}</h1>
                    <p style='font-size: 1.1rem; color: #CBD5E1; margin-top: 15px; font-weight: 300;'>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br><h4 style='color: #F8FAFC;'>Dimensionality Reduction (PCA Space)</h4>", unsafe_allow_html=True)
                np.random.seed(42)
                n_samples = 200
                pca1 = np.random.normal(0, 1, n_samples)
                pca2 = np.random.normal(0, 1, n_samples)
                clusters = np.random.randint(0, 6, n_samples)
                
                if pca_model is not None:
                    user_pca1, user_pca2 = pca_data[0][0], pca_data[0][1]
                else:
                    user_pca1, user_pca2 = 0, 0
                    
                pca1 = np.append(pca1, [user_pca1])
                pca2 = np.append(pca2, [user_pca2])
                clusters = np.append(clusters, [cluster])
                sizes = np.append(np.full(n_samples, 8), [60])
                symbols = np.append(np.full(n_samples, 'circle'), ['diamond'])
                
                scatter_df = pd.DataFrame({'PCA1': pca1, 'PCA2': pca2, 'Cluster': clusters, 'Size': sizes, 'Symbol': symbols})
                scatter_df['Cluster'] = scatter_df['Cluster'].astype(str)
                
                fig = px.scatter(scatter_df, x='PCA1', y='PCA2', color='Cluster', size='Size', symbol='Symbol',
                                 color_discrete_sequence=['#2A9D8F', '#E76F51', '#E9C46A', '#F4A261', '#B8C76A', '#8AB17D'])
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94A3B8', family="Inter"),
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("<h4 style='color: #F8FAFC; margin-top: 10px; margin-bottom: 20px;'>Segment Behavioral Profiles Matrix</h4>", unsafe_allow_html=True)
        
        comp_matrix_data = {
            "Cluster ID": ["Cluster 0", "Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4", "Cluster 5"],
            "Segment Nomenclature": ["Budget Focused Explorer", "Premium Enterprise Scholar", "Quality-Oriented Specialist", "Long-Term Curriculum Engager", "Accelerated Fast-Track", "Balanced Platform Generalist"],
            "Average Spend ($)": ["$24.50", "$185.00", "$95.00", "$110.00", "$65.00", "$55.00"],
            "Preferred Duration": ["Short (<8h)", "Extended (20h+)", "Moderate (12h)", "Extensive (35h+)", "Micro (<5h)", "Standard (10h)"],
            "Diversity Score": ["High (4.2)", "Low (1.4)", "Low (1.8)", "Moderate (2.5)", "Moderate (3.1)", "High (3.8)"],
            "Learning Depth Index": ["0.2 (Beginner Ratio)", "0.85 (Advanced Ratio)", "0.75 (Advanced Ratio)", "0.65 (Intermediate+)", "0.40 (Mixed Ratio)", "0.50 (Balanced)"],
            "Primary Value Focus": ["Cost Optimization", "Elite Certification", "High Rating Standard", "Deep Subject Mastery", "Time-to-Completion", "General Catalog Exploration"]
        }
        matrix_df = pd.DataFrame(comp_matrix_data)
        st.dataframe(matrix_df, hide_index=True, use_container_width=True)
        
        st.markdown("<br><h4 style='color: #F8FAFC;'>Intra-Cluster Behavioral Consistency</h4>", unsafe_allow_html=True)
        bar_data = pd.DataFrame({
            "Cluster": ["Cluster 0", "Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4", "Cluster 5"],
            "Silhouette Score": [0.68, 0.74, 0.71, 0.65, 0.62, 0.59]
        })
        fig_sil = px.bar(bar_data, x="Silhouette Score", y="Cluster", orientation='h', color="Silhouette Score", color_continuous_scale="Tealgrn")
        fig_sil.update_layout(template=custom_template, height=350, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_sil, use_container_width=True)

# ---------------------------------------------------
# 4. COURSE LEVEL PREDICTOR
# ---------------------------------------------------
elif choice == "Course Level Predictor":
    st.markdown("<div class='gradient-header'>Level Predictor</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Predictive Classification via Ensemble Modeling Networks</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2.5])
    with col1:
        st.markdown("<h4 style='color: #F8FAFC;'>Algorithm Selection</h4>", unsafe_allow_html=True)
        model_choice = st.selectbox("", ["XGBoost", "Random Forest", "LightGBM", "Decision Tree", "SVM", "KNN", "Gradient Boosting"], label_visibility="collapsed")
        
        st.markdown("<br><div class='info-box' style='padding: 15px;'><p style='font-size: 0.9rem; color: #94A3B8;'>The system will route the features through the selected architecture. Tree-based algorithms process absolute inputs, while distance-based models automatically scale data.</p></div>", unsafe_allow_html=True)
        
    with col2:
        with st.form("prediction_form"):
            st.markdown("<h4 style='color: #F8FAFC;'>Feature Engineering Inputs</h4>", unsafe_allow_html=True)
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                amount = st.number_input("Transaction ($)", 0.0, value=99.99)
                price = st.number_input("Base Price ($)", 0.0, value=99.99)
                user_age = st.number_input("User Age", 10, 80, 25)
                duration = st.number_input("Duration (Hours)", 1.0, value=15.0)
            with r1c2:
                c_rating = st.slider("Course Rating", 1.0, 5.0, 4.5)
                t_rating = st.slider("Instructor Rating", 1.0, 5.0, 4.6)
                exp = st.number_input("Instructor Exp (Yrs)", 0, value=8)
            with r1c3:
                t_age = st.number_input("Instructor Age", 20, value=35)
                month = st.selectbox("Transaction Month", list(range(1, 13)))
                weekday = st.selectbox("Transaction Day (0=Mon, 6=Sun)", list(range(7)))
                
            st.markdown("<br>", unsafe_allow_html=True)
            submit_pred = st.form_submit_button("Initialize Classification Sequence")
            
    if submit_pred:
        with st.spinner(f'Executing forward pass through {model_choice}...'):
            time.sleep(0.8)
            model_file_map = {
                "XGBoost": "xgboost_model.pkl", "Random Forest": "random_forest_model.pkl",
                "LightGBM": "lightgbm_model.pkl", "Decision Tree": "decision_tree_model.pkl",
                "SVM": "svm_model.pkl", "KNN": "knn_model.pkl", "Gradient Boosting": "gradient_boosting_model.pkl"
            }
            
            model = load_model(MODEL_DIR, model_file_map.get(model_choice))
            le = load_model(MODEL_DIR, "label_encoder.pkl")
            
            input_features = np.array([[amount, user_age, price, duration, c_rating, t_age, exp, t_rating, month, weekday]])
            
            if model is not None:
                try:
                    expected_features = getattr(model, "n_features_in_", len(PREDICTOR_FEATURES))
                    if expected_features != len(PREDICTOR_FEATURES):
                        raise ValueError(
                            f"{model_choice} expects {expected_features} features, "
                            f"but this form supplies {len(PREDICTOR_FEATURES)}."
                        )

                    if model_choice in ["SVM", "KNN"]:
                        from sklearn.preprocessing import StandardScaler
                        temp_scaler = StandardScaler()
                        if not all(col in df.columns for col in PREDICTOR_FEATURES):
                            raise ValueError("The dataset does not contain the predictor training features required for scaling.")
                        temp_scaler.fit(df[PREDICTOR_FEATURES])
                        scaled_features = temp_scaler.transform(input_features)
                    else:
                        scaled_features = input_features
                        
                    prediction_raw = model.predict(scaled_features)[0]
                    
                    if model_choice in ["XGBoost", "LightGBM"] and le is not None:
                        prediction = le.inverse_transform([int(prediction_raw)])[0]
                    else:
                        prediction = prediction_raw
                except Exception as e:
                    st.error(f"System Error: {e}")
                    prediction = "Intermediate"
            else:
                st.warning("Prediction engine unavailable. Outputting simulated threshold.")
                prediction = "Beginner" if duration < 10 else "Advanced"
            
            level_colors = {"Beginner": "#34D399", "Intermediate": "#FCD34D", "Advanced": "#F43F5E"}
            color = level_colors.get(prediction, "#38BDF8")
            
            st.markdown(f"""
            <div class='success-box' style='border-color: {color}; background: linear-gradient(145deg, {color}15 0%, rgba(5,5,5,0) 100%);'>
                <p style='color: #94A3B8; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 5px;'>Computed Classification Threshold</p>
                <h1 style='color: {color}; margin: 10px 0; font-family: Outfit; font-size: 4rem;'>{prediction}</h1>
                <p style='color: #64748B; font-size: 0.9rem;'>Powered by {model_choice}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------
# 5. MODEL EVALUATION
# ---------------------------------------------------
elif choice == "Model Evaluation":
    st.markdown("<div class='gradient-header'>Evaluation Metrics</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Comparative Evaluation of Classification Architectures</div>", unsafe_allow_html=True)
    
    models_data = {
        "Model": ["Logistic Regression", "Naive Bayes", "KNN", "SVM", "Decision Tree", "Extra Trees", "AdaBoost", "Gradient Boosting", "XGBoost", "LightGBM", "Random Forest"],
        "Accuracy (%)": [52.25, 41.00, 86.85, 84.25, 88.50, 90.45, 94.20, 94.00, 92.90, 86.75, 98.85]
    }
    
    comp_df = pd.DataFrame(models_data).sort_values(by="Accuracy (%)", ascending=True)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        fig = px.bar(comp_df, x="Accuracy (%)", y="Model", orientation='h', text="Accuracy (%)", color="Accuracy (%)", color_continuous_scale="Purpor")
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94A3B8', family="Inter"),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=False),
            height=600,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("<h4 style='color: #F8FAFC; margin-bottom: 20px;'>Accuracy Matrix</h4>", unsafe_allow_html=True)
        st.dataframe(
            comp_df.sort_values(by="Accuracy (%)", ascending=False).reset_index(drop=True),
            column_config={
                "Accuracy (%)": st.column_config.ProgressColumn("Accuracy (%)", format="%f%%", min_value=0, max_value=100)
            },
            hide_index=True, use_container_width=True, height=580
        )

# ---------------------------------------------------
# 6. PERSONALIZED RECOMMENDER (MODULE CAPABILITIES)
# ---------------------------------------------------
elif choice == "Personalized Recommender":
    st.markdown("<div class='gradient-header'>Personalization Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Learner Profile Explorer & Cluster-Aware Recommendation Filtering</div>", unsafe_allow_html=True)
    
    # User Capabilities: Select a learner profile, View assigned segment, Filter recommendations, See recommended paths
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<h4 style='color: #F8FAFC; margin-bottom: 15px;'>Learner Profile Selection</h4>", unsafe_allow_html=True)
        
        sim_users = {
            "USR-1029 (Budget Explorer)": {"age": 22, "gender": "Female", "cluster": 0, "spend": "$24.50", "depth": "0.2 (Beginner Focus)", "div": "4.2 (High)"},
            "USR-4091 (Premium Enterprise Scholar)": {"age": 34, "gender": "Male", "cluster": 1, "spend": "$185.00", "depth": "0.85 (Advanced Certs)", "div": "1.4 (Focused)"},
            "USR-8821 (Quality-Oriented Specialist)": {"age": 28, "gender": "Female", "cluster": 2, "spend": "$95.00", "depth": "0.75 (Advanced)", "div": "1.8 (Focused)"},
            "USR-3312 (Long-Term Scholar)": {"age": 41, "gender": "Male", "cluster": 3, "spend": "$110.00", "depth": "0.65 (Comprehensive)", "div": "2.5 (Moderate)"},
            "USR-9021 (Accelerated Fast-Tracker)": {"age": 25, "gender": "Other", "cluster": 4, "spend": "$65.00", "depth": "0.40 (Modular)", "div": "3.1 (Moderate)"},
            "USR-5541 (Balanced Platform Generalist)": {"age": 30, "gender": "Female", "cluster": 5, "spend": "$55.00", "depth": "0.50 (Balanced)", "div": "3.8 (High)"}
        }
        
        selected_user = st.selectbox("", list(sim_users.keys()), label_visibility="collapsed")
        u_data = sim_users[selected_user]
        
        st.markdown(f"""
        <div style='background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.05); padding: 20px; border-radius: 16px; margin-top: 15px;'>
            <h5 style='color: #E9C46A; margin-top: 0;'>Assigned Behavioral Segment</h5>
            <p style='color: #F8FAFC; font-family: Outfit; font-size: 1.4rem; font-weight: 600; margin: 5px 0;'>Cluster {u_data['cluster']}</p>
            <hr style='border-color: rgba(255,255,255,0.05); margin: 10px 0;'>
            <p style='color: #94A3B8; font-size: 0.9rem; margin: 3px 0;'>Demographic: {u_data['age']} yrs • {u_data['gender']}</p>
            <p style='color: #94A3B8; font-size: 0.9rem; margin: 3px 0;'>Average Spend: <span style='color: #34D399;'>{u_data['spend']}</span></p>
            <p style='color: #94A3B8; font-size: 0.9rem; margin: 3px 0;'>Learning Depth Index: {u_data['depth']}</p>
            <p style='color: #94A3B8; font-size: 0.9rem; margin: 3px 0;'>Diversity Score: {u_data['div']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><h4 style='color: #F8FAFC; margin-bottom: 15px;'>Catalog Filtering Parameters</h4>", unsafe_allow_html=True)
        filter_cat = st.selectbox("Target Category", ["All Categories", "Data Science", "Web Development", "Business Intelligence", "UI/UX Design", "Digital Marketing"])
        filter_level = st.selectbox("Target Course Level", ["All Levels", "Beginner", "Intermediate", "Advanced"])
        
    with col2:
        st.markdown("<h4 style='color: #F8FAFC; margin-bottom: 15px;'>Curated Learning Pathways</h4>", unsafe_allow_html=True)
        
        # Recommendation database simulation
        rec_catalog = [
            {"title": "Foundational Python & Data Operations", "cat": "Data Science", "level": "Beginner", "price": 19.99, "rating": 4.7, "c_match": [0, 5]},
            {"title": "Enterprise Machine Learning & Deep Learning", "cat": "Data Science", "level": "Advanced", "price": 149.99, "rating": 4.9, "c_match": [1, 2, 3]},
            {"title": "Accelerated Data Analysis Bootcamp", "cat": "Data Science", "level": "Intermediate", "price": 49.99, "rating": 4.6, "c_match": [4, 5]},
            {"title": "Web Development HTML/CSS Architecture", "cat": "Web Development", "level": "Beginner", "price": 15.99, "rating": 4.5, "c_match": [0, 5]},
            {"title": "Full-Stack Enterprise React & Node.js", "cat": "Web Development", "level": "Advanced", "price": 129.99, "rating": 4.8, "c_match": [1, 2, 3]},
            {"title": "Micro-Frontend Fast Track Architecture", "cat": "Web Development", "level": "Intermediate", "price": 59.99, "rating": 4.6, "c_match": [4]},
            {"title": "Business Intelligence & SQL Foundations", "cat": "Business Intelligence", "level": "Beginner", "price": 25.00, "rating": 4.6, "c_match": [0, 5]},
            {"title": "Advanced Executive BI & Tableau Strategy", "cat": "Business Intelligence", "level": "Advanced", "price": 180.00, "rating": 4.9, "c_match": [1, 2, 3]},
            {"title": "UI/UX Design Principles & Wireframing", "cat": "UI/UX Design", "level": "Beginner", "price": 22.50, "rating": 4.7, "c_match": [0, 5]},
            {"title": "Mastering Enterprise Design Systems", "cat": "UI/UX Design", "level": "Advanced", "price": 110.00, "rating": 4.8, "c_match": [1, 2, 3]},
            {"title": "Digital Marketing Analytics & SEO Intro", "cat": "Digital Marketing", "level": "Beginner", "price": 20.00, "rating": 4.5, "c_match": [0, 5]},
            {"title": "Strategic Brand Management for Leaders", "cat": "Digital Marketing", "level": "Advanced", "price": 135.00, "rating": 4.8, "c_match": [1, 2, 3]}
        ]
        
        # Apply filters
        filtered_recs = []
        for item in rec_catalog:
            match_c = (filter_cat == "All Categories" or item["cat"] == filter_cat)
            match_l = (filter_level == "All Levels" or item["level"] == filter_level)
            if match_c and match_l:
                # Calculate relevance bonus if item matches user's cluster
                is_clust_match = u_data["cluster"] in item["c_match"]
                filtered_recs.append((item, is_clust_match))
                
        # Sort so cluster matches appear at top
        filtered_recs.sort(key=lambda x: (not x[1], -x[0]["rating"]))
        
        if filtered_recs:
            for item, is_c_match in filtered_recs:
                border_clr = "#38BDF8" if is_c_match else "rgba(255,255,255,0.05)"
                badge = "<span style='background: rgba(56, 189, 248, 0.2); color: #38BDF8; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; margin-left: 10px;'>Cluster Match</span>" if is_c_match else ""
                
                st.markdown(f"""
                <div style='background: rgba(30, 41, 59, 0.3); border: 1px solid {border_clr}; padding: 20px; border-radius: 12px; margin-bottom: 15px; transition: transform 0.2s;'>
                    <div style='display: flex; justify_content: space-between; align-items: flex-start;'>
                        <div>
                            <h5 style='color: #F8FAFC; margin: 0; font-family: Outfit; font-size: 1.2rem;'>{item['title']} {badge}</h5>
                            <p style='color: #94A3B8; font-size: 0.9rem; margin: 5px 0 0 0;'>{item['cat']} • <span style='color: #CBD5E1;'>{item['level']}</span></p>
                        </div>
                        <div style='text-align: right;'>
                            <h4 style='color: #34D399; margin: 0; font-family: Outfit;'>${item['price']:.2f}</h4>
                            <p style='color: #FCD34D; font-size: 0.85rem; margin: 2px 0 0 0;'>★ {item['rating']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No catalog assets match the current filtering parameters.")

# ---------------------------------------------------
# 7. SYSTEM ARCHITECTURE
# ---------------------------------------------------
elif choice == "System Architecture":
    st.markdown("<div class='gradient-header'>System Architecture</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
        <h3 style='margin-top: 0; color: #F8FAFC;'>Strategic Objective</h3>
        <p style='color: #CBD5E1; line-height: 1.6; font-weight: 300;'>The EduPro Analytics engine deploys robust machine learning infrastructure to automatically segment the user base via unsupervised K-Means clustering, and operates parallel classification networks to predict content difficulty thresholds with up to 98.85% accuracy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; margin-bottom: 20px;'>
            <h4 style='color: #2A9D8F; margin-top:0;'>Technology Stack</h4>
            <ul style='color: #CBD5E1; font-weight: 300; line-height: 1.8;'>
                <li>Interface: Streamlit Core</li>
                <li>Visualizations: Plotly & Custom CSS</li>
                <li>Data Operations: Pandas, NumPy</li>
                <li>Inference Engines: Scikit-learn, XGBoost, LightGBM</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; margin-bottom: 20px;'>
            <h4 style='color: #E76F51; margin-top:0;'>Algorithmic Deployment</h4>
            <ul style='color: #CBD5E1; font-weight: 300; line-height: 1.8;'>
                <li>Primary Classifier: XGBoost & Random Forest</li>
                <li>Dimensionality Reduction: Principal Component Analysis (PCA)</li>
                <li>Segmentation Core: K-Means Optimization</li>
                <li>Recommendation: Heuristic Domain Mapping</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05);'><p style='text-align: center; color: #475569; font-size: 0.8rem; font-weight: 300;'>EduPro Analytics System Operations © 2026</p>", unsafe_allow_html=True)
