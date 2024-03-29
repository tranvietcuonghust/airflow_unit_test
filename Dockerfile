FROM apache/airflow:2.7.3-python3.10


COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
ENV PIP_USER=false

# Create directories for our virtual environments
RUN mkdir -p /home/airflow/yfinance_venv/venv1 /home/airflow/yfinance_venv/venv2

# ENV VENV1=/home/airflow/yfinance_venv/venv1
# ENV VENV2=/home/airflow/yfinance_venv/venv2

# Create virtual environments and upgrade pip and setuptools
RUN python3 -m venv /home/airflow/yfinance_venv/venv1
RUN /home/airflow/yfinance_venv/venv1/bin/pip install --no-cache-dir yfinance==0.2.27 -r /requirements.txt
RUN python3 -m venv /home/airflow/yfinance_venv/venv2
RUN /home/airflow/yfinance_venv/venv2/bin/pip install --no-cache-dir yfinance==0.2.3 -r /requirements.txt

ENV PIP_USER=true
# COPY --chown=airflow:root . /opt/airflow/