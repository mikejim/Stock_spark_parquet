FROM python:3.10-slim

# Install Java and tools
RUN apt-get update && \
    apt-get install -y default-jdk curl && \
    rm -rf /var/lib/apt/lists/*

# Dynamically set JAVA_HOME
RUN export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java)))) && \
    echo "export JAVA_HOME=$JAVA_HOME" >> /etc/environment

# Manually set JAVA_HOME again just to be sure
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt


