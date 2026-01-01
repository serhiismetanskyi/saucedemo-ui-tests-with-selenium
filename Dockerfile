FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN mkdir -p /etc/apt/keyrings \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | grep -o '"version":"[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*"' | head -1 | cut -d'"' -f4) \
    && wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O chromedriver-linux64.zip \
    && unzip -q chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip chromedriver-linux64

# Install uv via pip for parity with other projects
RUN python -m pip install --upgrade pip && \
    pip install uv

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
RUN uv sync

# Copy project files
COPY . .

# Set environment variables
ENV HEADLESS=headless \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Run tests by default
CMD ["uv", "run", "python", "-m", "pytest", "tests", "--html=./reports/test_report.html", "--self-contained-html"]


