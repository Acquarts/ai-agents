# Dockerfile for City Views Finder - Streamlit on Cloud Run
# Optimized for Cloud Run deployment with monitoring support

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_cloudrun.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_cloudrun.txt

# Copy application files
COPY streamlit_app.py .
COPY agent_resource_name.txt .

# Copy agent folder (if needed for reference)
COPY my_agent/ ./my_agent/

# Create .streamlit config directory
RUN mkdir -p .streamlit

# Create Streamlit config
RUN echo "\
[server]\n\
port = 8080\n\
address = \"0.0.0.0\"\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
\n\
[theme]\n\
primaryColor = \"#1f77b4\"\n\
backgroundColor = \"#ffffff\"\n\
secondaryBackgroundColor = \"#f0f2f6\"\n\
textColor = \"#262730\"\n\
" > .streamlit/config.toml

# Expose port
EXPOSE 8080

# Run the application
CMD streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
