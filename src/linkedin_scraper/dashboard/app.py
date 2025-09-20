"""
Streamlit dashboard application for LinkedIn Job Trends
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import os
import sys
from pathlib import Path
import plotly.graph_objects as go

# Add project root to path for config import
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from .dashboard_functions import (
    find_number_jobs_per_city,
    find_latest_jobs_cities,
    get_available_reports,
    get_city_data_summary
)
from config.settings import DEFAULT_CITIES, DASHBOARD_TITLE, DASHBOARD_LAYOUT


def setup_page_config():
    """Set up Streamlit page configuration."""
    st.set_page_config(
        page_title=DASHBOARD_TITLE,
        layout=DASHBOARD_LAYOUT,
        initial_sidebar_state="expanded",
        page_icon="📊"
    )
    
    # Enhanced CSS with cooler visuals and animations
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling with animation */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 0;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
        animation: slideInDown 1s ease-out;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    @keyframes slideInDown {
        from { transform: translateY(-100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .main-header h1 {
        font-size: 4rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        background: linear-gradient(45deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); }
        to { text-shadow: 0 4px 20px rgba(255, 255, 255, 0.5); }
    }
    
    .main-header h2 {
        font-size: 1.8rem;
        font-weight: 400;
        margin: 1rem 0 0 0;
        opacity: 0.9;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Enhanced chart containers with glassmorphism */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .chart-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Section headers with gradient text */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2rem;
        padding: 1rem 0;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    /* Enhanced sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Cool selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Cool metrics styling */
    .metric-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-3px);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom spacing */
    .stApp > div:first-child {
        padding-top: 1rem;
    }
    
    /* Loading spinner enhancement */
    .stSpinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Error message styling */
    .stAlert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border-radius: 15px;
        border: none;
        box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        color: white;
        border-radius: 15px;
        border: none;
        box-shadow: 0 10px 25px rgba(0, 184, 148, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)


def create_sidebar(data_dir: Path) -> tuple:
    """
    Create the sidebar with city and report selection.
    
    Args:
        data_dir: Directory containing the data
        
    Returns:
        Tuple of (selected_city, selected_report)
    """
    # Sidebar header
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: #0077b5; margin: 0;">🎯 Filters</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # City selection
    st.sidebar.markdown("### 📍 Select City")
    selected_city = st.sidebar.selectbox(
        "Choose a city to analyze", 
        DEFAULT_CITIES,
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Get available reports
    st.sidebar.markdown("### 📊 Available Reports")
    report_names = get_available_reports(data_dir)
    default_index = 0
    
    if "Software Engineer" in report_names:
        default_index = report_names.index("Software Engineer")
    
    selected_report = st.sidebar.selectbox(
        "Choose a job position", 
        report_names, 
        index=default_index,
        label_visibility="collapsed"
    )

    
    st.sidebar.markdown("---")
    
    # Contact section
    st.sidebar.markdown("""
    <div style="background: linear-gradient(90deg, #0077b5 0%, #005885 100%); 
                padding: 1rem; border-radius: 10px; text-align: center; margin-top: 2rem;">
        <h4 style="color: white; margin: 0 0 0.5rem 0;">📧 Contact</h4>
        <p style="color: white; margin: 0; font-size: 0.9rem;">
            <a href="mailto:hamza.bouzoubaa@hotmail.com" 
               style="color: white; text-decoration: none;">
                hamza.bouzoubaa@hotmail.com
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    return selected_city, selected_report


def create_job_trends_chart(selected_report: str, selected_city: str, job_date: str, data_dir: Path):
    """
    Create the main job trends chart.
    
    Args:
        selected_report: Selected job report
        selected_city: Selected city
        job_date: Selected time period
        data_dir: Directory containing the data
    """
    with st.spinner('Loading job trends data...'):
        try:
            df = find_number_jobs_per_city(selected_report, selected_city, job_date, data_dir)
            
            fig = px.line(
                df, 
                title='Evolution of Jobs in ' + selected_city + ' over Time',
                x='Date',
                y='Total_Jobs',
                labels={'Date': 'Date', 'Total_Jobs': 'Total Jobs'},
                line_shape='spline',
                hover_data={'Date': '|%B %d, %Y'}
            )
            
            fig.update_traces(
                hovertemplate='<b>Date: %{x}</b><br><b>Total Jobs: %{y}</b><extra></extra>',
                textfont_size=20,
                mode='lines+markers',
                line=dict(width=3),
                marker=dict()
            )
            
            fig.update_xaxes(
                tickformat='%Y-%m-%d',
                tickangle=-25,
                title_standoff=25
            )
            
            fig.update_layout(
                height=500,
                title_x=0.5,
                font=dict(size=16, family="Inter, sans-serif"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='rgba(102,126,234,0.3)',
                    borderwidth=1
                ),
                xaxis=dict(
                    gridcolor='rgba(102,126,234,0.1)',
                    linecolor='rgba(102,126,234,0.3)',
                    tickfont=dict(color='#667eea')
                ),
                yaxis=dict(
                    gridcolor='rgba(102,126,234,0.1)',
                    linecolor='rgba(102,126,234,0.3)',
                    tickfont=dict(color='#667eea')
                )
            )
            
            st.plotly_chart(fig)
        
        except Exception as e:
            st.error(f"Error creating trends chart: {e}")


def create_city_metrics(selected_report: str, job_date: str, data_dir: Path):
    """
    Create city metrics display.
    
    Args:
        selected_report: Selected job report
        job_date: Selected time period
        data_dir: Directory containing the data
    """
    try:
        df = find_latest_jobs_cities(selected_report, job_date, data_dir)
        
        # Split DataFrame into groups for display
        df1 = df.iloc[:2]
        df2 = df.iloc[2:4]
        df3 = df.iloc[4:6]
        
        col21, col22, col23, col24 = st.columns([0.5, 1, 1, 1])
        
        with col22:
            st.markdown('#')
            for _, row in df1.iterrows():
                st.metric(label=row['City'], value=row['Total_Jobs'], delta=row['delta'])
        
        with col23:
            st.markdown('#')
            for _, row in df2.iterrows():
                st.metric(label=row['City'], value=row['Total_Jobs'], delta=row['delta'])
        
        with col24:
            st.markdown('#')
            for _, row in df3.iterrows():
                st.metric(label=row['City'], value=row['Total_Jobs'], delta=row['delta'])
                
    except Exception as e:
        st.error(f"Error creating city metrics: {e}")


def create_seniority_chart(selected_report: str, selected_city: str, data_dir: Path):
    """
    Create seniority level pie chart.
    
    Args:
        selected_report: Selected job report
        selected_city: Selected city
        data_dir: Directory containing the data
    """
    try:
        csv_path = data_dir / f"{selected_report}/{selected_report} in {selected_city}.csv"
        print(csv_path)
        
        if not csv_path.exists():
            st.warning(f"No data available for {selected_report} in {selected_city}")
            return
        
        df = pd.read_csv(csv_path)
        print("df")
        print(df)
        
        if 'seniority_level' not in df.columns:
            st.warning("Seniority level data not available")
            return
        
        seniority_level = df['seniority_level'].value_counts()
        
        color_discrete_map = {
            'Entry level': 'blue',
            'Mid-Senior level': 'green',
            'Director': 'red',
            'Executive': 'purple',
            'Internship': 'orange'
        }
        
        fig = px.pie(
            seniority_level, 
            values=seniority_level.values, 
            names=seniority_level.index, 
            color=seniority_level.index, 
            color_discrete_map=color_discrete_map,
            hole=0.4
        )
        
        fig.update_layout(
            font=dict(size=14, family="Inter, sans-serif"),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(102,126,234,0.3)',
                borderwidth=1
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        
        st.plotly_chart(fig)
        
    except Exception as e:
        st.error(f"Error creating seniority chart: {e}")


def create_employment_type_chart(selected_report: str, selected_city: str, data_dir: Path):
    """
    Create employment type pie chart.
    
    Args:
        selected_report: Selected job report
        selected_city: Selected city
        data_dir: Directory containing the data
    """
    try:
        csv_path = data_dir / f"{selected_report}/{selected_report} in {selected_city}.csv"
        
        if not csv_path.exists():
            st.warning(f"No data available for {selected_report} in {selected_city}")
            return
        
        df = pd.read_csv(csv_path)
        
        if 'employment_type' not in df.columns:
            st.warning("Employment type data not available")
            return
        
        employment_type = df['employment_type'].value_counts()
        
        color_discrete_map = {
            'Full-time': 'blue',
            'Part-time': 'green',
            'Contract': 'red',
            'Temporary': 'purple',
            'Volunteer': 'orange',
            'Internship': 'pink'
        }
        
        fig = px.pie(
            employment_type, 
            values=employment_type.values, 
            names=employment_type.index, 
            color=employment_type.index, 
            color_discrete_map=color_discrete_map,
            hole=0.4
        )
        
        fig.update_layout(
            font=dict(size=14, family="Inter, sans-serif"),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(102,126,234,0.3)',
                borderwidth=1
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        
        st.plotly_chart(fig)
        
    except Exception as e:
        st.error(f"Error creating employment type chart: {e}")


def create_industries_chart(selected_report: str, selected_city: str, data_dir: Path):
    """
    Create industries pie chart.
    
    Args:
        selected_report: Selected job report
        selected_city: Selected city
        data_dir: Directory containing the data
    """
    try:
        csv_path = data_dir / f"{selected_report}/{selected_report} in {selected_city}.csv"
        
        if not csv_path.exists():
            st.warning(f"No data available for {selected_report} in {selected_city}")
            return
        
        df = pd.read_csv(csv_path)
        
        if 'industries' not in df.columns:
            st.warning("Industries data not available")
            return
        
        industries = df['industries'].value_counts()
        
        # Keep only top 10 industries, combine rest into 'Other'
        if len(industries) > 10:
            top_10 = industries.head(5)
            others_sum = industries.iloc[5:].sum()
            top_10['Other'] = others_sum
            industries = top_10
        
        fig = px.pie(industries, values=industries.values, names=industries.index, hole=0.4)
        
        fig.update_layout(
            font=dict(size=14, family="Inter, sans-serif"),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(102,126,234,0.3)',
                borderwidth=1
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        
        st.plotly_chart(fig)
        
    except Exception as e:
        st.error(f"Error creating industries chart: {e}")


def create_company_size_chart(selected_report: str, selected_city: str, data_dir: Path):
    """
    Create company size pie chart.
    
    Args:
        selected_report: Selected job report
        selected_city: Selected city
        data_dir: Directory containing the data
    """
    try:
        csv_path = data_dir / f"{selected_report}/{selected_report} in {selected_city}.csv"
        
        if not csv_path.exists():
            st.warning(f"No data available for {selected_report} in {selected_city}")
            return
        
        df = pd.read_csv(csv_path)
        
        if 'company_size' not in df.columns:
            st.warning("Company size data not available")
            return
        
        company_size = df['company_size'].value_counts()
        
        # Define size mapping
        size_mapping = {
            '1-10 employees': 'Small (less than 50)',
            '11-50 employees': 'Small (less than 50)',
            '51-200 employees': 'Medium (50-200)',
            '201-500 employees': 'Medium (50-200)',
            '501-1,000 employees': 'Large (500-5000)',
            '1,001-5,000 employees': 'Large (500-5000)',
            '5,001-10,000 employees': 'Very Large (5000+)',
            '10,001+ employees': 'Very Large (5000+)'
        }
        
        # Map company sizes to larger categories
        company_size = company_size.groupby(size_mapping).sum()
        
        # Ensure proper order
        size_order = ['Small (less than 50)', 'Medium (50-200)', 'Large (500-5000)', 'Very Large (5000+)']
        company_size.index = pd.Categorical(company_size.index, categories=size_order, ordered=True)
        company_size = company_size.sort_index()
        
        color_discrete_map = {
            'Small (less than 50)': 'lightblue',
            'Medium (50-200)': 'green',
            'Large (500-5000)': 'red',
            'Very Large (5000+)': 'purple'
        }
        
        fig = px.pie(
            company_size, 
            values=company_size.values, 
            names=company_size.index, 
            color=company_size.index, 
            color_discrete_map=color_discrete_map,
            hole=0.4
        )
        
        fig.update_layout(
            font=dict(size=14, family="Inter, sans-serif"),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(102,126,234,0.3)',
                borderwidth=1
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        
        st.plotly_chart(fig)
        
    except Exception as e:
        st.error(f"Error creating company size chart: {e}")


def main():
    """Main dashboard application."""
    # Setup
    setup_page_config()
    data_dir = Path("data/raw/JobData")
    
    # Create sidebar
    selected_city, selected_report = create_sidebar(data_dir)
    
    # Main header
    st.markdown(f"""
    <div class="main-header">
        <h1>📊 LinkedIn Job Trends</h1>
        <h2>Analyzing: {selected_report} Positions</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Info section with enhanced styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; margin: 2rem 0; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div style="color: white;">
                <h3 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">📍 City</h3>
                <h2 style="margin: 0.5rem 0 0 0; font-size: 1.8rem; font-weight: 700;">{selected_city}</h2>
            </div>
            <div style="color: white;">
                <h3 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">💼 Position</h3>
                <h2 style="margin: 0.5rem 0 0 0; font-size: 1.8rem; font-weight: 700;">{selected_report}</h2>
            </div>
            <div style="color: white;">
                <h3 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">📊 Analysis</h3>
                <h2 style="margin: 0.5rem 0 0 0; font-size: 1.8rem; font-weight: 700;">Total Jobs</h2>
            </div>
        </div>
    </div>
    """.format(selected_city=selected_city, selected_report=selected_report), unsafe_allow_html=True)
    
    # Set default time period to Total
    job_date = "Total"
    
    st.markdown("---")
    
    # Main metrics and trends section
    st.markdown(f"""
    <div class="section-header">
        📈 Job Trends & City Metrics
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        with st.container():
            create_job_trends_chart(selected_report, selected_city, job_date, data_dir)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <h4 style="color: #0077b5; margin: 0;">🏙️ City Metrics</h4>
        </div>
        """, unsafe_allow_html=True)
        create_city_metrics(selected_report, job_date, data_dir)
    
    # Analytics section
    st.markdown(f"""
    <div class="section-header">
        📊 Market Analysis for {selected_city}
    </div>
    """, unsafe_allow_html=True)
    
    # First row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h4 style="color: #0077b5; margin: 0;">👔 Seniority Level Distribution</h4>
            </div>
            """, unsafe_allow_html=True)
            print(selected_report, selected_city, data_dir)
            create_seniority_chart(selected_report, selected_city, data_dir)
    
    with col2:
        with st.container():
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h4 style="color: #0077b5; margin: 0;">💼 Employment Type Breakdown</h4>
            </div>
            """, unsafe_allow_html=True)
            create_employment_type_chart(selected_report, selected_city, data_dir)
    
    # Second row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h4 style="color: #0077b5; margin: 0;">🏭 Industry Distribution</h4>
            </div>
            """, unsafe_allow_html=True)
            create_industries_chart(selected_report, selected_city, data_dir)
    
    with col2:
        with st.container():
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h4 style="color: #0077b5; margin: 0;">🏢 Company Size Analysis</h4>
            </div>
            """, unsafe_allow_html=True)
            create_company_size_chart(selected_report, selected_city, data_dir)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; 
                background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%); 
                border-radius: 10px;">
        <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">
            📊 LinkedIn Job Trends Dashboard | Powered by Python & Streamlit
        </p>
        <p style="color: #6c757d; margin: 0.5rem 0 0 0; font-size: 0.8rem;">
            Data sourced from LinkedIn job postings 
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()