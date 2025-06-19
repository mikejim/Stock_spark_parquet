FROM python:3.10-slim

# Install Java (if needed for Spark)
RUN apt-get update && apt-get install -y default-jdk curl && rm -rf /var/lib/apt/lists/*

# Set Java environment variables (if Spark is used in this image)
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir requests
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Tell Docker what to run on container start
CMD ["python", "-u",  "producer/stream_producer.py"]
#CMD ["python", "-c", "print('🔥 Producer container is alive'); import time; time.sleep(30)"]

