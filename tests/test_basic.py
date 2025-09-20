"""
Basic tests for LinkedIn Job Trends Scraper
"""

import pytest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.linkedin_scraper.models.job_posting import JobPosting
from src.linkedin_scraper.utils.logger import setup_logger
from src.linkedin_scraper.dashboard.dashboard_functions import JOB_DATE_OPTIONS


def test_job_posting_creation():
    """Test JobPosting model creation."""
    job = JobPosting(
        title="Software Engineer",
        job_link="https://linkedin.com/jobs/123",
        company="Test Company",
        location="Toronto"
    )
    
    assert job.title == "Software Engineer"
    assert job.company == "Test Company"
    assert job.location == "Toronto"
    assert job.job_link == "https://linkedin.com/jobs/123"


def test_job_posting_to_dict():
    """Test JobPosting to_dict method."""
    job = JobPosting(
        title="Software Engineer",
        job_link="https://linkedin.com/jobs/123"
    )
    
    job_dict = job.to_dict()
    assert isinstance(job_dict, dict)
    assert job_dict['title'] == "Software Engineer"


def test_job_posting_empty_check():
    """Test JobPosting is_empty method."""
    job = JobPosting(title="Test", job_link="https://test.com")
    assert not job.is_empty()
    
    empty_job = JobPosting(title=None, job_link=None)
    assert empty_job.is_empty()


def test_logger_setup():
    """Test logger setup."""
    logger = setup_logger("test_logger")
    assert logger is not None
    assert logger.name == "test_logger"




if __name__ == "__main__":
    pytest.main([__file__])