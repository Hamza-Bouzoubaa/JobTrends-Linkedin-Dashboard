# LinkedIn Job Trends Scraper

A professional LinkedIn job scraping and analytics tool for tracking job market trends across different cities and positions. This tool provides comprehensive insights into job markets through data collection, analysis, and visualization.

<img width="1759" height="618" alt="Capture d'écran 2025-09-20 132016" src="https://github.com/user-attachments/assets/89e5552a-921e-4b07-b2fe-48f55072ffdc" />
<img width="1798" height="681" alt="Capture d'écran 2025-09-20 132036" src="https://github.com/user-attachments/assets/35bbc6a0-7d33-41cc-bb74-ed310d766b04" />
<img width="1774" height="719" alt="Capture d'écran 2025-09-20 132029" src="https://github.com/user-attachments/assets/1d7b65f5-8a3c-4214-8f70-64f5c37fdf21" />




## 🚀 Features

- **Automated Job Scraping**: Scrape job listings from LinkedIn across multiple cities and positions
- **Detailed Job Information**: Extract comprehensive job details including seniority level, employment type, company information
- **Company Intelligence**: Gather company details including size, industry, and location
- **Interactive Dashboard**: Beautiful Streamlit-based dashboard for data visualization
- **Trend Analysis**: Track job market trends over time with interactive charts
- **Multi-City Comparison**: Compare job markets across different cities
- **Professional Architecture**: Clean, modular codebase with proper separation of concerns

## 📊 Dashboard Features

- **Job Trends Over Time**: Interactive line charts showing job posting trends
- **City Metrics**: Real-time metrics comparing job counts across cities
- **Seniority Level Analysis**: Pie charts showing distribution of seniority levels
- **Employment Type Breakdown**: Analysis of full-time, part-time, contract positions
- **Industry Distribution**: Insights into job distribution across industries
- **Company Size Analysis**: Breakdown of jobs by company size categories



## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hamza-bouzoubaa/JobTrends-Linkedin-Scraper.git
   cd JobTrends-Linkedin-Scraper
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package** (optional):
   ```bash
   pip install -e .
   ```

## 🚀 Usage

### Running the Scraper

To scrape job data:

```bash
python run_scraper.py
```

Or using the installed package:

```bash
linkedin-scraper
```

### Running the Dashboard

To start the interactive dashboard:

```bash
python run_dashboard.py
```

Or using the installed package:

```bash
linkedin-dashboard
```

Then open your browser and navigate to `http://localhost:8501`

### Configuration

Edit `config/settings.py` to customize:

- **Default Cities**: Cities to scrape data for
- **Job Positions**: Job titles to monitor
- **Scraping Limits**: Maximum number of jobs to scrape
- **Request Settings**: Retry logic and rate limiting

## 📁 Data Structure

The scraper organizes data in the following structure:

```
data/raw/
├── Software Engineer/
│   ├── Software Engineer in Toronto.csv
│   ├── Software Engineer in Montreal.csv
│   └── TotalJobs/
│       └── TotalJobs.csv
└── Internship/
    ├── Internship in Toronto.csv
    └── TotalJobs/
        └── TotalJobs.csv
```

## 🔧 Configuration Options

### Default Cities
- Ottawa
- Toronto
- Montreal
- Vancouver
- Calgary
- Edmonton

### Default Job Positions
- Software Engineer
- Internship

### Scraping Settings
- Maximum retries: 5
- Request delay: 5 seconds
- Rate limit delay: 15 seconds
- Default job limit: 1000 per city

## 📊 Dashboard Components

### Main Features
1. **City Selection**: Choose from available cities
2. **Report Selection**: Select from available job reports
3. **Time Period Filter**: Filter by posting date (24h, Week, Month, Total)
4. **Interactive Charts**: Hover and zoom capabilities
5. **Real-time Metrics**: Live job count comparisons

### Chart Types
- **Line Charts**: Job trends over time
- **Pie Charts**: Distribution analysis
- **Metrics**: Key performance indicators


### Development Setup

For development, install additional dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest tests/
```

Format code:

```bash
black src/ tests/
```

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Please respect LinkedIn's Terms of Service and robots.txt file. Use responsibly and consider implementing appropriate delays between requests to avoid overwhelming their servers.


### Getting Help

If you encounter issues:

1. Check the [Issues](https://github.com/hamza-bouzoubaa/JobTrends-Linkedin-Scraper/issues) page
2. Create a new issue with detailed information
3. Contact the author via email


**Made with ❤️ by Hamza Bouzoubaa**
