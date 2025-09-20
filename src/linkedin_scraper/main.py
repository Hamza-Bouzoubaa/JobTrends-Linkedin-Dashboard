"""
Main entry point for LinkedIn Job Trends Scraper
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from linkedin_scraper.core.orchestrator import ScrapingOrchestrator
from linkedin_scraper.utils.logger import setup_logger
from config.settings import DEFAULT_JOB_POSITIONS, DEFAULT_CITIES

logger = setup_logger(__name__)


def main():
    """
    Main function to run the LinkedIn job scraping workflow.
    """
    logger.info("Starting LinkedIn Job Trends Scraper")
    
    try:
        # Initialize orchestrator
        orchestrator = ScrapingOrchestrator()
        
        # Run complete workflow
        orchestrator.run_complete_workflow(DEFAULT_JOB_POSITIONS, DEFAULT_CITIES)
        
        logger.info("LinkedIn Job Trends Scraper completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main workflow: {e}")
        raise


if __name__ == "__main__":
    main()