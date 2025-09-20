"""
LinkedIn job list scraper
"""

import re
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple
from urllib.parse import quote

from ..models.job_posting import JobPosting
from ..utils.request_handler import RequestHandler
from ..utils.logger import get_logger

logger = get_logger(__name__)


class JobListScraper:
    """
    Scrapes job listings from LinkedIn.
    """
    
    def __init__(self, request_handler: Optional[RequestHandler] = None):
        """
        Initialize job list scraper.
        
        Args:
            request_handler: Custom request handler (optional)
        """
        self.request_handler = request_handler or RequestHandler()
        
        # LinkedIn-specific headers
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'dnt': '1',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }
    
    def _build_search_url(self, job_title: str, location: str, position: int = 0) -> str:
        """
        Build LinkedIn job search URL.
        
        Args:
            job_title: Job title to search for
            location: Location to search in
            position: Starting position for pagination
            
        Returns:
            Complete search URL
        """
        encoded_job_title = quote(job_title)
        
        if position == 0:
            return f"https://www.linkedin.com/jobs/search?keywords={encoded_job_title}&location={location}&trk=public_jobs_jobs-search-bar_search-submit&position=0&pageNum=0"
        else:
            return f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={encoded_job_title}&location={location}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start={position}"
    
    def _parse_jobs(self, response_text: str) -> pd.DataFrame:
        """
        Parse job listings from HTML response.
        
        Args:
            response_text: HTML response text
            
        Returns:
            DataFrame of job listings
        """
        soup = BeautifulSoup(response_text, 'html.parser')
        
        # Find all job postings
        job_postings = soup.find_all('div', class_='base-search-card__info')
        job_posting_urls = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        
        if not job_postings:
            logger.warning("No jobs found in response")
            return JobPosting(
                title=None, 
                company=None, 
                location=None, 
                date_posted=None, 
                job_link=None
            ).to_df()
        
        jobs_data = []
        
        for i, job_posting in enumerate(job_postings):
            try:
                # Extract job title
                title_elem = job_posting.find('h3', class_='base-search-card__title')
                title = title_elem.get_text(strip=True) if title_elem else None
                
                # Extract company name
                company_elem = job_posting.find('a', class_='hidden-nested-link')
                company = company_elem.get_text(strip=True) if company_elem else None
                
                # Extract location
                location_elem = job_posting.find('span', class_='job-search-card__location')
                location = location_elem.get_text(strip=True) if location_elem else None
                
                # Extract date posted
                date_elem = job_posting.find('time', class_='job-search-card__listdate') or \
                           job_posting.find('time', class_='job-search-card__listdate--new')
                date_posted = date_elem.get_text(strip=True) if date_elem else None
                
                # Extract job link
                job_link = None
                if i < len(job_posting_urls):
                    link_elem = job_posting_urls[i].find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
                    job_link = link_elem.get('href') if link_elem else None
                
                # Create job posting object
                job = JobPosting(
                    title=title,
                    company=company,
                    location=location,
                    date_posted=date_posted,
                    job_link=job_link
                )
                
                jobs_data.append(job.to_dict())
                
            except Exception as e:
                logger.error(f"Error parsing job posting {i}: {e}")
                continue
        
        return pd.DataFrame(jobs_data)
    
    def _parse_total_jobs(self, response_text: str) -> List[int]:
        """
        Parse total job counts from HTML response.
        
        Args:
            response_text: HTML response text
            
        Returns:
            List of [total, past_month, past_week, past_24h] job counts
        """
        soup = BeautifulSoup(response_text, 'html.parser')
        
        # Find job count elements
        total_elem = soup.find('label', {'for': 'f_TPR-0'})
        past_month_elem = soup.find('label', {'for': 'f_TPR-1'})
        past_week_elem = soup.find('label', {'for': 'f_TPR-2'})
        past_24h_elem = soup.find('label', {'for': 'f_TPR-3'})
        
        def extract_count(elem) -> int:
            """Extract numeric count from element."""
            if elem:
                text = elem.get_text(strip=True)
                # Extract last number from text
                numbers = re.findall(r'\d+', text)
                return int(numbers[-1]) if numbers else 0
            return 0
        
        total_jobs = extract_count(total_elem)
        past_month_jobs = extract_count(past_month_elem)
        past_week_jobs = extract_count(past_week_elem)
        past_24h_jobs = extract_count(past_24h_elem)
        
        logger.info(f"Job counts - Total: {total_jobs}, Month: {past_month_jobs}, Week: {past_week_jobs}, 24h: {past_24h_jobs}")
        
        return [total_jobs, past_month_jobs, past_week_jobs, past_24h_jobs]
    
    def get_total_jobs(self, job_title: str, location: str) -> List[Optional[int]]:
        """
        Get total job counts for a search.
        
        Args:
            job_title: Job title to search for
            location: Location to search in
            
        Returns:
            List of job counts [total, past_month, past_week, past_24h]
        """
        url = self._build_search_url(job_title, location)
        response = self.request_handler.get(url, self.headers)
        
        if response is None:
            logger.error(f"Failed to get job counts for {job_title} in {location}")
            return [None, None, None, None]
        
        return self._parse_total_jobs(response.text)
    
    def get_job_list(self, job_title: str, location: str, position: int = 0) -> pd.DataFrame:
        """
        Get job listings for a search.
        
        Args:
            job_title: Job title to search for
            location: Location to search in
            position: Starting position for pagination
            
        Returns:
            DataFrame of job listings
        """
        url = self._build_search_url(job_title, location, position)
        response = self.request_handler.get(url, self.headers)
        
        if response is None:
            logger.error(f"Failed to get job list for {job_title} in {location}")
            return JobPosting(
                title=None, 
                company=None, 
                location=None, 
                date_posted=None, 
                job_link=None
            ).to_df()
        
        return self._parse_jobs(response.text)