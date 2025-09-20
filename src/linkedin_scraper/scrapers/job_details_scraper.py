"""
LinkedIn job details scraper
"""

import re
import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any

from ..utils.request_handler import RequestHandler
from ..utils.logger import get_logger

logger = get_logger(__name__)


class JobDetailsScraper:
    """
    Scrapes detailed information from individual LinkedIn job postings.
    """
    
    def __init__(self, request_handler: Optional[RequestHandler] = None):
        """
        Initialize job details scraper.
        
        Args:
            request_handler: Custom request handler (optional)
        """
        self.request_handler = request_handler or RequestHandler()
        
        # LinkedIn-specific headers
        self.headers = {
            'Cookie': 'bcookie="v=2&d871c9f5-039b-4f64-85c5-dc2babc12b5d"; lang=v=2&lang=en-us; lidc="b=TGST01:s=T:r=T:a=T:p=T:g=3413:u=1:x=1:i=1725195445:t=1725281845:v=2:sig=AQE8ro7KHWSZ59NwKnOx1xnKUW-Xzroh"; JSESSIONID=ajax:6246440277120090716; bscookie="v=1&202409011301077868575c-c958-4da0-833b-39e76815efb2AQHU1aXEIsm920nFET3NHHcWxNwG9l-R"; ccookie=0001AQEpLClb0ypivQAAAZGtraD4o3LC40GB8eIXAjTd1+bZFvV//pN8zDuMBho1b24EWRUccBPsXfoAViaCjpwwC6bEUWGTbpJOmTmLVjO6ta62BZiXkHHFlnS6qHyxTwnxduY/423GjMencshxx3aL8Pi1IOnIwJI4XdiNNr4vnSzZ5sZ7IHc='
        }
    
    def _parse_response(self, response_text: str) -> pd.DataFrame:
        """
        Parse job details from HTML response.
        
        Args:
            response_text: HTML response text
            
        Returns:
            DataFrame with job details
        """
        soup = BeautifulSoup(response_text, 'html.parser')
        
        # Extract job criteria (seniority, employment type, etc.)
        job_criteria = soup.find_all('span', class_='description__job-criteria-text description__job-criteria-text--criteria')
        
        seniority_level = job_criteria[0].get_text(strip=True) if len(job_criteria) > 0 else None
        employment_type = job_criteria[1].get_text(strip=True) if len(job_criteria) > 1 else None
        job_function = job_criteria[2].get_text(strip=True) if len(job_criteria) > 2 else None
        industries = job_criteria[3].get_text(strip=True) if len(job_criteria) > 3 else None
        
        # Extract number of applicants
        applicants = None
        applicants_elem = soup.find('span', class_='num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet')
        
        if not applicants_elem:
            applicants_elem = soup.find('figcaption', class_='num-applicants__caption')
        
        if applicants_elem:
            applicants = applicants_elem.get_text(strip=True)
        
        # Extract time posted from meta description
        time_posted = None
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        
        if meta_tag and meta_tag.get('content'):
            date_description = meta_tag['content']
            date_match = re.match(r'Posted\s([\d:AMP\s]+)\.\s', date_description)
            time_posted = date_match.group(1) if date_match else None
        
        # Extract job description
        description_elem = soup.find('div', class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden')
        description = None
        
        if description_elem:
            description = description_elem.get_text(separator='\n')
            description = description.replace("\n", "")
        
        # Extract location
        location_elem = soup.find('span', class_='sub-nav-cta__meta-text')
        location = location_elem.get_text(strip=True) if location_elem else None
        
        # Extract company URL
        company_url_elem = soup.find('a', class_='topcard__org-name-link topcard__flavor--black-link', 
                                   attrs={'data-tracking-control-name': 'public_jobs_topcard-org-name'})
        company_url = company_url_elem.get('href') if company_url_elem else None
        
        # Create DataFrame with extracted data
        data = {
            'location': [location],
            'seniority_level': [seniority_level],
            'employment_type': [employment_type],
            'job_function': [job_function],
            'industries': [industries],
            'applicants': [applicants],
            'description': [description],
            'time_posted': [time_posted],
            'company_url': [company_url]
        }
        
        df = pd.DataFrame(data)
        
        # Reorder columns
        column_order = ['location', 'seniority_level', 'employment_type', 'job_function', 
                       'industries', 'applicants', 'description', 'time_posted', 'company_url']
        df = df[column_order]
        
        return df
    
    def get_job_details(self, job_url: str) -> pd.DataFrame:
        """
        Get detailed information for a specific job posting.
        
        Args:
            job_url: URL of the job posting
            
        Returns:
            DataFrame with job details
        """
        response = self.request_handler.get(job_url, self.headers)
        
        if response is None:
            logger.error(f"Failed to get job details from {job_url}")
            return pd.DataFrame(columns=['location', 'seniority_level', 'employment_type', 
                                       'job_function', 'industries', 'applicants', 
                                       'description', 'time_posted', 'company_url'])
        
        return self._parse_response(response.text)