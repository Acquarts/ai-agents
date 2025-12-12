FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT:-8501} --server.headless=true --browser.gatherUsageStats=false"]

