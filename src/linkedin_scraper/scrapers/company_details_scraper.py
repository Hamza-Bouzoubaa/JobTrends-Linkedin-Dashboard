"""
LinkedIn company details scraper
"""

import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional

from ..utils.request_handler import RequestHandler
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CompanyDetailsScraper:
    """
    Scrapes detailed information from LinkedIn company pages.
    """
    
    def __init__(self, request_handler: Optional[RequestHandler] = None):
        """
        Initialize company details scraper.
        
        Args:
            request_handler: Custom request handler (optional)
        """
        self.request_handler = request_handler or RequestHandler()
        
        # LinkedIn-specific headers
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'lang=v=2&lang=en-us; bcookie="v=2&7aafa9fa-80bb-4ce9-8e58-258f7098a230"; JSESSIONID=ajax:7091056752031294795; bscookie="v=1&202409192328445eee63e6-ebb7-42ff-875d-0fa354080d90AQEYBL-g0GHt3qgVmskTAwIKrBcSU_UB"; _gcl_au=1.1.2089583266.1726788524; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; lidc="b=VGST09:s=V:r=V:a=V:p=V:g=3000:u=1:x=1:i=1726788752:t=1726875152:v=2:sig=AQGjYHcYWON2_plKudYDAzzdNRZGutip"; _uetsid=e99c613076de11ef9b4663fa46f07827; _uetvid=e99c9de076de11ef99a55f1b4a8d232b; aam_uuid=13676313366740523261239266915417371647; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19986%7CMCMID%7C13122036689852649411296453458398429236%7CMCAAMLH-1727400769%7C7%7CMCAAMB-1727400769%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1726803169s%7CNONE%7CvVersion%7C5.1.1; bcookie="v=2&de48fc50-3246-4850-898b-88edb58255af"; lang=v=2&lang=en-us; lidc="b=VGST07:s=V:r=V:a=V:p=V:g=3060:u=1:x=1:i=1726862006:t=1726948406:v=2:sig=AQH7qeonWJpC1ySI_F9AHYUpVZZXu5nL"; JSESSIONID=ajax:6123196309613059981',
            'dnt': '1',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
    
    def _parse_response(self, response_text: str) -> pd.DataFrame:
        """
        Parse company details from HTML response.
        
        Args:
            response_text: HTML response text
            
        Returns:
            DataFrame with company details
        """
        soup = BeautifulSoup(response_text, 'html.parser')
        data = {}
        
        # Find company information elements
        elements = soup.find_all('div', class_='mb-2 flex papabear:mr-3 mamabear:mr-3 babybear:flex-wrap')
        
        for element in elements:
            key_elem = element.find('dt')
            value_elem = element.find('dd')
            
            if key_elem and value_elem:
                key = key_elem.get_text(strip=True)
                value = value_elem.get_text(strip=True)
                
                # Normalize key names
                normalized_key = key.replace(' ', '_').lower()
                data[normalized_key] = value
        
        # Create DataFrame
        df = pd.DataFrame([data])
        
        return df
    
    def get_company_details(self, company_url: str) -> pd.DataFrame:
        """
        Get detailed information for a specific company.
        
        Args:
            company_url: URL of the company page
            
        Returns:
            DataFrame with company details
        """
        response = self.request_handler.get(company_url, self.headers)
        
        if response is None:
            logger.error(f"Failed to get company details from {company_url}")
            return pd.DataFrame()
        
        return self._parse_response(response.text)