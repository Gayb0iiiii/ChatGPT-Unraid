FROM python:3.11

WORKDIR /app

# Install system tools required for system context gathering
RUN apt-get update && apt-get install -y \
    procps iproute2 net-tools \
    sysstat lsof docker.io \
    curl htop coreutils \
    && rm -rf /var/lib/apt/lists/*

COPY backend/ /app/
COPY templates/ /app/templates/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
