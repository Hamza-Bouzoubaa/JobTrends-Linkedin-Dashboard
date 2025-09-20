"""
Configuration settings for LinkedIn Job Trends Scraper
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# LinkedIn configuration
LINKEDIN_BASE_URL = "https://www.linkedin.com"
LINKEDIN_JOBS_SEARCH_URL = f"{LINKEDIN_BASE_URL}/jobs/search"
LINKEDIN_JOBS_API_URL = f"{LINKEDIN_BASE_URL}/jobs-guest/jobs/api/seeMoreJobPostings/search"

# Default cities to scrape
DEFAULT_CITIES = [
    "Ottawa",
    "Toronto", 
    "Montreal",
    "Vancouver",
    "Calgary",
    "Edmonton"
]

# Default job positions to watch
DEFAULT_JOB_POSITIONS = [
    "Software Engineer",
    "Internship"
]

# Scraping configuration
DEFAULT_LIMIT = 1000
MAX_RETRIES = 5
REQUEST_DELAY = 5  # seconds
RATE_LIMIT_DELAY = 15  # seconds for 429 errors

# Dashboard configuration
DASHBOARD_TITLE = "LinkedIn Job Trends"
DASHBOARD_LAYOUT = "wide"

# File paths
LOG_FILE = BASE_DIR / "app.log"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)