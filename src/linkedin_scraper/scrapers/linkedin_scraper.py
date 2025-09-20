"""
Main LinkedIn scraper orchestrator
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Tuple

from ..models.job_posting import JobPosting
from .job_list_scraper import JobListScraper
from .job_details_scraper import JobDetailsScraper
from .company_details_scraper import CompanyDetailsScraper
from ..utils.request_handler import RequestHandler
from ..utils.logger import get_logger

logger = get_logger(__name__)


class LinkedInScraper:
    """
    Main orchestrator for LinkedIn job scraping operations.
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize LinkedIn scraper.
        
        Args:
            data_dir: Directory to store scraped data
        """
        self.data_dir = data_dir or Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize scrapers
        request_handler = RequestHandler()
        self.job_list_scraper = JobListScraper(request_handler)
        self.job_details_scraper = JobDetailsScraper(request_handler)
        self.company_details_scraper = CompanyDetailsScraper(request_handler)
    
    def scrape_all_jobs(self, job_title: str, location: str, limit: int = 1000) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Scrape all job listings for a given job title and location.
        
        Args:
            job_title: Job title to search for
            location: Location to search in
            limit: Maximum number of jobs to scrape
            
        Returns:
            Tuple of (DataFrame of jobs, file path)
        """
        logger.info(f"Starting job scraping for '{job_title}' in '{location}'")
        
        # Get total job count
        total_jobs = self.job_list_scraper.get_total_jobs(job_title, location)
        if total_jobs[0] is None:
            logger.error("Failed to get total job count")
            return None, None
        
        # Determine actual limit
        actual_limit = min(total_jobs[0], limit)
        logger.info(f"Found {total_jobs[0]} total jobs, limiting to {actual_limit}")
        
        # Get initial job list
        jobs_df = self.job_list_scraper.get_job_list(job_title, location, 0)
        
        if jobs_df.empty:
            logger.error("No jobs found in initial search")
            return None, None
        
        # Paginate through results
        for position in range(60, actual_limit, 10):
            logger.info(f"Scraping positions {position}-{min(position + 10, actual_limit)}")
            
            new_jobs = self.job_list_scraper.get_job_list(job_title, location, position)
            
            if new_jobs.empty or new_jobs['title'].isnull().all():
                logger.warning(f"No more jobs found at position {position}")
                break
            
            jobs_df = pd.concat([jobs_df, new_jobs], ignore_index=True)
        
        # Save to file
        file_path = self.data_dir / f"{job_title}/{job_title} in {location}.csv"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        jobs_df.to_csv(file_path, index=False)
        
        logger.info(f"Successfully scraped {len(jobs_df)} jobs and saved to {file_path}")
        return jobs_df, str(file_path)
    
    def scrape_all_job_details(self, file_path: str) -> Tuple[Optional[pd.DataFrame], str]:
        """
        Scrape detailed information for all jobs in a file.
        
        Args:
            file_path: Path to CSV file containing job listings
            
        Returns:
            Tuple of (DataFrame with details, file path)
        """
        logger.info(f"Starting job details scraping for {file_path}")
        
        df = pd.read_csv(file_path)
        jobs_with_details = []
        
        for i, row in df.iterrows():
            logger.info(f"Processing job {i+1}/{len(df)}: {row.get('title', 'Unknown')}")
            
            job_url = row.get('job_link')
            if pd.isna(job_url):
                logger.warning(f"No job URL for row {i}")
                continue
            
            # Get job details
            job_details = self.job_details_scraper.get_job_details(job_url)
            
            if job_details.empty:
                logger.warning(f"No details found for job {i}")
                continue
            
            # Create enhanced job posting
            job = JobPosting(
                title=row.get('title'),
                company=row.get('company'),
                location=row.get('location'),
                date_posted=row.get('date_posted'),
                job_link=row.get('job_link'),
                description=job_details['description'].iloc[0],
                time_posted=job_details['time_posted'].iloc[0],
                seniority_level=job_details['seniority_level'].iloc[0],
                employment_type=job_details['employment_type'].iloc[0],
                job_function=job_details['job_function'].iloc[0],
                industries=job_details['industries'].iloc[0],
                applicants=job_details['applicants'].iloc[0],
                company_url=job_details['company_url'].iloc[0]
            )
            
            jobs_with_details.append(job.to_dict())
        
        # Create DataFrame and save
        result_df = pd.DataFrame(jobs_with_details)
        result_df.to_csv(file_path, index=False)
        
        logger.info(f"Successfully added details to {len(result_df)} jobs")
        return result_df, file_path
    
    def scrape_all_company_details(self, file_path: str) -> Tuple[Optional[pd.DataFrame], str]:
        """
        Scrape company details for all jobs in a file.
        
        Args:
            file_path: Path to CSV file containing job listings
            
        Returns:
            Tuple of (DataFrame with company details, file path)
        """
        logger.info(f"Starting company details scraping for {file_path}")
        
        df = pd.read_csv(file_path)
        jobs_with_company_details = []
        
        for i, row in df.iterrows():
            logger.info(f"Processing company {i+1}/{len(df)}: {row.get('company', 'Unknown')}")
            
            company_url = row.get('company_url')
            if pd.isna(company_url):
                logger.warning(f"No company URL for row {i}")
                continue
            
            # Get company details
            company_details = self.company_details_scraper.get_company_details(company_url)
            
            if company_details.empty:
                logger.warning(f"No company details found for row {i}")
                continue
            
            # Create enhanced job posting with company details
            job = JobPosting(
                title=row.get('title'),
                company=row.get('company'),
                location=row.get('location'),
                date_posted=row.get('date_posted'),
                job_link=row.get('job_link'),
                description=row.get('description'),
                time_posted=row.get('time_posted'),
                seniority_level=row.get('seniority_level'),
                employment_type=row.get('employment_type'),
                job_function=row.get('job_function'),
                industries=row.get('industries'),
                applicants=row.get('applicants'),
                company_url=row.get('company_url'),
                company_size=company_details.get('company_size', [None]).iloc[0] if 'company_size' in company_details.columns else None,
                founded=company_details.get('founded', [None]).iloc[0] if 'founded' in company_details.columns else None,
                company_type=company_details.get('type', [None]).iloc[0] if 'type' in company_details.columns else None,
                industry=company_details.get('industry', [None]).iloc[0] if 'industry' in company_details.columns else None,
                headquarters=company_details.get('headquarters', [None]).iloc[0] if 'headquarters' in company_details.columns else None
            )
            
            jobs_with_company_details.append(job.to_dict())
        
        # Create DataFrame and save
        result_df = pd.DataFrame(jobs_with_company_details)
        result_df.to_csv(file_path, index=False)
        
        logger.info(f"Successfully added company details to {len(result_df)} jobs")
        return result_df, file_path