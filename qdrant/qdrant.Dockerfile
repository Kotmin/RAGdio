FROM qdrant/qdrant:v1.13.3

USER root
RUN apt update && apt install -y curl
# USER 1000
