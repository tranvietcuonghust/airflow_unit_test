docker build -t my-airflow image .
docker compose up -d
docker exec -it your-airflow-container bash
    airflow tasks test my_simple_dag extract_stock_old_yfinance
    -> this run venv with yfinance==0.2.27 which still have get_shares_full() function -> it should print out a table
    airflow tasks test my_simple_dag extract_stock_new_yfinance
    -> this run venv with yfinance==0.2.3 which doesn't have get_shares_full() function -> it should print out error