FROM python:3.11.0-slim
WORKDIR /app
COPY . . 
# RUN apt-get update && \
#     apt-get install -y wget && \
#     wget https://github.com/jgm/pandoc/releases/download/2.14.0.3/pandoc-2.14.0.3-1-amd64.deb \
#     dpkg -i pandoc-2.14.0.3-1-amd64.deb && \
#     rm pandoc-2.14.0.3-1-amd64.deb && \
#     apt-get clean
RUN pip install -r requirements.txt
ENTRYPOINT ["fastapi", "run", "src/main.py", "--port", "80"]