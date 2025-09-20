"""
HTTP request handling utilities with retry logic and rate limiting
"""

import time
import requests
from typing import Optional, Dict, Any
from .logger import get_logger

logger = get_logger(__name__)


class RequestHandler:
    """
    Handles HTTP requests with retry logic and rate limiting.
    """
    
    def __init__(
        self,
        max_retries: int = 5,
        base_delay: int = 5,
        rate_limit_delay: int = 15,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize request handler.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay between retries in seconds
            rate_limit_delay: Delay for rate limit errors in seconds
            headers: Default headers for requests
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.rate_limit_delay = rate_limit_delay
        self.headers = headers or {}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def handle_response(self, response: requests.Response, current_trial: int = 0) -> bool:
        """
        Handle HTTP response and determine if retry is needed.
        
        Args:
            response: HTTP response object
            current_trial: Current trial number
            
        Returns:
            True if successful, False if retry needed, None if max retries reached
        """
        status = response.status_code
        
        if status == 200:
            logger.debug("Request successful")
            return True
        
        elif current_trial < self.max_retries:
            logger.warning(f"Request failed with status {status}, retrying...")
            
            if status == 429:  # Rate limited
                delay = self.rate_limit_delay * current_trial
                logger.info(f"Rate limited, waiting {delay} seconds")
                time.sleep(delay)
            else:
                delay = self.base_delay * current_trial
                logger.info(f"Request failed, waiting {delay} seconds")
                time.sleep(delay)
            
            return False
        
        else:
            logger.error("Max retries reached")
            return None
    
    def make_request(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        current_trial: int = 0
    ) -> Optional[requests.Response]:
        """
        Make HTTP request with retry logic.
        
        Args:
            url: Request URL
            method: HTTP method
            headers: Additional headers
            data: Request data
            current_trial: Current trial number
            
        Returns:
            Response object or None if failed
        """
        request_headers = {**self.headers}
        if headers:
            request_headers.update(headers)
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=request_headers)
            elif method.upper() == "POST":
                response = self.session.post(url, headers=request_headers, data=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            result = self.handle_response(response, current_trial)
            
            if result is True:
                return response
            elif result is False:
                return self.make_request(url, method, headers, data, current_trial + 1)
            else:
                return None
                
        except requests.RequestException as e:
            logger.error(f"Request exception: {e}")
            if current_trial < self.max_retries:
                delay = self.base_delay * current_trial
                time.sleep(delay)
                return self.make_request(url, method, headers, data, current_trial + 1)
            else:
                return None
    
    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        """Make GET request."""
        return self.make_request(url, "GET", headers)
    
    def post(self, url: str, data: Optional[Dict[str, Any]] = None, 
             headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        """Make POST request."""
        return self.make_request(url, "POST", headers, data)