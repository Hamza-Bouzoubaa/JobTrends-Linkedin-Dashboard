"""
Main orchestrator for LinkedIn job scraping operations
"""

import pandas as pd
import datetime
from pathlib import Path
from typing import List, Optional

from ..scrapers.linkedin_scraper import LinkedInScraper
from ..scrapers.job_list_scraper import JobListScraper
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ScrapingOrchestrator:
    """
    Orchestrates the complete LinkedIn job scraping workflow.
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the orchestrator.
        
        Args:
            data_dir: Directory to store scraped data
        """
        self.data_dir = data_dir or Path("data/raw/JobData")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize scrapers
        self.linkedin_scraper = LinkedInScraper(self.data_dir)
        self.job_list_scraper = JobListScraper()
    
    def create_city_comparison(self, job_title: str, cities: List[str] = None) -> Optional[pd.DataFrame]:
        """
        Create a comparison of job counts across cities.
        
        Args:
            job_title: Job title to search for
            cities: List of cities to compare (optional)
        
        Returns:
            DataFrame with city comparison data
        """
        if cities is None:
            from ...config.settings import DEFAULT_CITIES
            cities = DEFAULT_CITIES
        
        logger.info(f"Creating city comparison for '{job_title}' across {len(cities)} cities")
        
        # Create directory structure
        job_data_dir = self.data_dir / f"{job_title}/TotalJobs"
        job_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize DataFrame
        df = pd.DataFrame(columns=['City', '24h_Jobs', 'Week_Jobs', 'Month_Jobs', 'Total_Jobs', 'Date'])
        total_jobs = []
        
        # Get job counts for each city
        for city in cities:
            logger.info(f"Getting job counts for {city}")
            
            result = self.job_list_scraper.get_total_jobs(job_title, city)
            
            if result == [None, None, None, None]:
                logger.error(f"Failed to get job counts for {city}")
                return None
            
            total_jobs.append(result)
        
        logger.info(f"Job counts collected: {total_jobs}")
        
        # Populate DataFrame
        df["City"] = cities
        df["24h_Jobs"] = [x[3] for x in total_jobs]  # Past 24 hours
        df["Week_Jobs"] = [x[2] for x in total_jobs]  # Past week
        df["Month_Jobs"] = [x[1] for x in total_jobs]  # Past month
        df["Total_Jobs"] = [x[0] for x in total_jobs]  # Total
        df['Date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # Try to append to existing data
        total_jobs_file = job_data_dir / "TotalJobs.csv"
        
        try:
            if total_jobs_file.exists():
                existing_df = pd.read_csv(total_jobs_file)
                df = pd.concat([existing_df, df], ignore_index=True)
        except Exception as e:
            logger.warning(f"Could not read existing TotalJobs.csv: {e}")
        
        # Sort by date and save
        df = df.sort_values(by='Date')
        df.to_csv(total_jobs_file, index=False)
        
        logger.info(f"City comparison data saved to {total_jobs_file}")
        return df
    
    def scrape_city_data(self, job_title: str, cities: List[str] = None) -> None:
        """
        Scrape detailed job data for all cities.
        
        Args:
            job_title: Job title to search for
            cities: List of cities to scrape (optional)
        """
        if cities is None:
            from ...config.settings import DEFAULT_CITIES
            cities = DEFAULT_CITIES
        
        logger.info(f"Starting detailed data scraping for '{job_title}' across {len(cities)} cities")
        
        for city in cities:
            logger.info(f"Scraping data for {city}")
            
            try:
                # Scrape job listings
                jobs_df, jobs_path = self.linkedin_scraper.scrape_all_jobs(job_title, city, limit=100)
                
                if jobs_df is None:
                    logger.error(f"Failed to scrape jobs for {city}")
                    continue
                
                # Scrape job details
                details_df, details_path = self.linkedin_scraper.scrape_all_job_details(jobs_path)
                
                if details_df is None:
                    logger.error(f"Failed to scrape job details for {city}")
                    continue
                
                # Scrape company details
                company_df, final_path = self.linkedin_scraper.scrape_all_company_details(details_path)
                
                if company_df is None:
                    logger.error(f"Failed to scrape company details for {city}")
                    continue
                
                logger.info(f"Successfully scraped complete data for {city}")
                
            except Exception as e:
                logger.error(f"Error scraping data for {city}: {e}")
                continue
    
    def run_complete_workflow(self, job_titles: List[str] = None, cities: List[str] = None) -> None:
        """
        Run the complete scraping workflow.
        
        Args:
            job_titles: List of job titles to scrape (optional)
            cities: List of cities to scrape (optional)
        """
        if job_titles is None:
            from ...config.settings import DEFAULT_JOB_POSITIONS
            job_titles = DEFAULT_JOB_POSITIONS
        
        logger.info(f"Starting complete workflow for {len(job_titles)} job titles")
        
        for job_title in job_titles:
            logger.info(f"Processing job title: {job_title}")
            
            try:
                # Create city comparison
                comparison_df = self.create_city_comparison(job_title, cities)
                
                if comparison_df is not None:
                    logger.info(f"Successfully created city comparison for {job_title}")
                else:
                    logger.error(f"Failed to create city comparison for {job_title}")
                    continue
                
                # Scrape detailed city data
                self.scrape_city_data(job_title, cities)
                
                logger.info(f"Completed workflow for {job_title}")
                
            except Exception as e:
                logger.error(f"Error in workflow for {job_title}: {e}")
                continue
        
        logger.info("Complete workflow finished")