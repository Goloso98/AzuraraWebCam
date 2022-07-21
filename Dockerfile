FROM python:3.9-alpine

WORKDIR /app
COPY server.py .

USER "azurara"
RUN pip3 install requests

EXPOSE 1234
CMD [ "python3", "server.py" ] 
