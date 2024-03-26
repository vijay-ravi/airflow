from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import yfinance as yf
from bs4 import BeautifulSoup
import requests

def fetch_financial_data():
    # Fetch financial data for a specific ticker using yfinance
    ticker = yf.Ticker("AAPL")
    hist = ticker.history(period="1mo")  # Example: Fetch one month of historical data
    print(hist.head())  # Log the first few rows of the data

def scrape_web_data():
    # Use requests and BeautifulSoup to scrape financial news
    url = "https://finance.yahoo.com/quote/AAPL/news?p=AAPL"  # Example URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Extract and print the headlines of the news articles
    headlines = soup.find_all('h3', class_='Mb(5px)')
    for headline in headlines:
        print(headline.text)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'financial_data_collection',
    default_args=default_args,
    description='A simple DAG to fetch financial data and scrape web data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

t1 = PythonOperator(
    task_id='fetch_financial_data',
    python_callable=fetch_financial_data,
    dag=dag,
)

t2 = PythonOperator(
    task_id='scrape_web_data',
    python_callable=scrape_web_data,
    dag=dag,
)

t1 >> t2  # Set task dependency
