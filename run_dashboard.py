"""
Run the LinkedIn Job Trends Dashboard
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.linkedin_scraper.dashboard.app import main

if __name__ == "__main__":
    main()