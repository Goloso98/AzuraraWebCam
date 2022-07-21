FROM python:3.9-alpine

WORKDIR /app
COPY server.py .

EXPOSE 1234
CMD [ "python3", "server.py" ] 
