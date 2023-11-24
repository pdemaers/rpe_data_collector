FROM python:3.10.7
EXPOSE 8501
RUN pip install -r requirements.txt
WORKDIR /financials
COPY . ./
ENTRYPOINT [ "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0" ]