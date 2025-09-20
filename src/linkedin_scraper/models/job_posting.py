"""
Job posting data model
"""

import pandas as pd
from typing import Optional, Dict, Any


class JobPosting:
    """
    Represents a LinkedIn job posting with all relevant details.
    """
    
    def __init__(
        self,
        title: str,
        job_link: str,
        company: Optional[str] = None,
        location: Optional[str] = None,
        date_posted: Optional[str] = None,
        time_posted: Optional[str] = None,
        description: Optional[str] = None,
        seniority_level: Optional[str] = None,
        employment_type: Optional[str] = None,
        job_function: Optional[str] = None,
        industries: Optional[str] = None,
        applicants: Optional[str] = None,
        company_url: Optional[str] = None,
        company_size: Optional[str] = None,
        founded: Optional[str] = None,
        company_type: Optional[str] = None,
        industry: Optional[str] = None,
        headquarters: Optional[str] = None
    ):
        """
        Initialize a JobPosting object.
        
        Args:
            title: Job title
            job_link: URL to the job posting
            company: Company name
            location: Job location
            date_posted: Date when job was posted
            time_posted: Time when job was posted
            description: Job description
            seniority_level: Required seniority level
            employment_type: Type of employment (full-time, part-time, etc.)
            job_function: Job function/category
            industries: Industry sectors
            applicants: Number of applicants
            company_url: URL to company page
            company_size: Company size
            founded: Year company was founded
            company_type: Type of company
            industry: Company industry
            headquarters: Company headquarters location
        """
        self.title = title
        self.company = company
        self.location = location
        self.date_posted = date_posted
        self.job_link = job_link
        self.description = description
        self.seniority_level = seniority_level
        self.employment_type = employment_type
        self.job_function = job_function
        self.industries = industries
        self.applicants = applicants
        self.company_url = company_url
        self.time_posted = time_posted
        self.company_size = company_size
        self.founded = founded
        self.company_type = company_type
        self.industry = industry
        self.headquarters = headquarters

    def __str__(self) -> str:
        """String representation of the job posting."""
        return f"""
        Title: {self.title}
        Company: {self.company}
        Location: {self.location}
        Date Posted: {self.date_posted}
        Time Posted: {self.time_posted}
        Seniority Level: {self.seniority_level}
        Employment Type: {self.employment_type}
        Job Function: {self.job_function}
        Industries: {self.industries}
        Applicants: {self.applicants}
        Link: {self.job_link}
        Company URL: {self.company_url}
        Company Size: {self.company_size}
        Founded: {self.founded}
        Type: {self.company_type}
        Industry: {self.industry}
        Headquarters: {self.headquarters}
        Description: {self.description}
        """
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job posting to dictionary."""
        return self.__dict__
    
    def to_df(self) -> pd.DataFrame:
        """Convert job posting to pandas DataFrame."""
        return pd.DataFrame([self.__dict__])
    
    def is_empty(self) -> bool:
        """Check if the job posting is empty (no essential data)."""
        essential_fields = [self.title, self.company, self.location, 
                          self.date_posted, self.job_link, self.description]
        return all(field is None for field in essential_fields)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobPosting':
        """Create JobPosting instance from dictionary."""
        return cls(**data)
    
    @classmethod
    def from_df(cls, df: pd.DataFrame, index: int = 0) -> 'JobPosting':
        """Create JobPosting instance from DataFrame row."""
        if df.empty or index >= len(df):
            raise ValueError("Invalid DataFrame or index")
        
        row = df.iloc[index]
        return cls(**row.to_dict())