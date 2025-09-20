"""
Dashboard utility functions for LinkedIn Job Trends
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List


# Translation mapping for job date options
JOB_DATE_OPTIONS = {
    'Last 24h': '24h_Jobs',
    'Last Week': 'Week_Jobs',
    'Last Month': 'Month_Jobs',
    'Total': 'Total_Jobs'
}


def find_number_jobs_per_city(job_search: str, city: str, job_date: str, data_dir: Path = None) -> pd.DataFrame:
    """
    Find the number of jobs per city over time for a specific job search.
    
    Args:
        job_search: Job title/position to search for
        city: City to filter by
        job_date: Time period (Last 24h, Last Week, Last Month, Total)
        data_dir: Directory containing the data (optional)
    
    Returns:
        DataFrame with date and job counts
    """
    if data_dir is None:
        data_dir = Path("data/raw/JobData")
    
    csv_path = data_dir / f"{job_search}/TotalJobs/TotalJobs.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")
    
    df = pd.read_csv(csv_path)
    df = df[df['City'] == city]
    
    if job_date not in JOB_DATE_OPTIONS:
        raise ValueError(f"Invalid job_date: {job_date}. Must be one of {list(JOB_DATE_OPTIONS.keys())}")
    
    column_name = JOB_DATE_OPTIONS[job_date]
    df = df[['Date', 'City', column_name]]
    df.rename(columns={column_name: 'Total_Jobs'}, inplace=True)
    
    return df


def find_latest_jobs_cities(job_search: str, job_date: str, data_dir: Path = None) -> pd.DataFrame:
    """
    Find the latest job counts for all cities.
    
    Args:
        job_search: Job title/position to search for
        job_date: Time period (Last 24h, Last Week, Last Month, Total)
        data_dir: Directory containing the data (optional)
    
    Returns:
        DataFrame with latest job counts and deltas for all cities
    """
    if data_dir is None:
        data_dir = Path("data/raw/JobData")
    
    csv_path = data_dir / f"{job_search}/TotalJobs/TotalJobs.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    if job_date not in JOB_DATE_OPTIONS:
        raise ValueError(f"Invalid job_date: {job_date}. Must be one of {list(JOB_DATE_OPTIONS.keys())}")
    
    column_name = JOB_DATE_OPTIONS[job_date]
    df = df[['Date', 'City', column_name]]
    df.rename(columns={column_name: 'Total_Jobs'}, inplace=True)
    
    # Sort by date and group by city
    df = df.sort_values(by='Date', ascending=False)
    df = df.groupby('City').apply(lambda x: x.sort_values(by='Date')).reset_index(drop=True)
    
    # Calculate delta (change from previous period)
    df['delta'] = df.groupby('City')['Total_Jobs'].diff()
    
    # Fill NaN values and convert to int
    df['Total_Jobs'] = df['Total_Jobs'].fillna(0).astype(int)
    df['delta'] = df['delta'].fillna(0).astype(int)
    
    # Get only the latest data
    df = df[df['Date'] == df['Date'].max()]
    
    return df


def get_available_reports(data_dir: Path = None) -> List[str]:
    """
    Get list of available job reports from the data directory.
    
    Args:
        data_dir: Directory containing the data (optional)
    
    Returns:
        List of available report names
    """
    if data_dir is None:
        data_dir = Path("data/raw/JobData")
    
    if not data_dir.exists():
        return []
    
    # Get all directories in the data directory
    report_names = [folder.name for folder in data_dir.iterdir() if folder.is_dir()]
    
    return sorted(report_names)


def get_city_data_summary(job_search: str, city: str, data_dir: Path = None) -> Dict:
    """
    Get summary statistics for a specific city and job search.
    
    Args:
        job_search: Job title/position to search for
        city: City to analyze
        data_dir: Directory containing the data (optional)
    
    Returns:
        Dictionary with summary statistics
    """
    if data_dir is None:
        data_dir = Path("data/raw/JobData")
    
    csv_path = data_dir / f"{job_search}/{job_search} in {city}.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    summary = {
        'total_jobs': len(df),
        'seniority_levels': df['seniority_level'].value_counts().to_dict() if 'seniority_level' in df.columns else {},
        'employment_types': df['employment_type'].value_counts().to_dict() if 'employment_type' in df.columns else {},
        'industries': df['industries'].value_counts().to_dict() if 'industries' in df.columns else {},
        'company_sizes': df['company_size'].value_counts().to_dict() if 'company_size' in df.columns else {}
    }
    
    return summary