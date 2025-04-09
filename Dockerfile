FROM python:3.13.3-slim

WORKDIR /app

COPY . .

EXPOSE 3000/udp
EXPOSE 3000
EXPOSE 5000/udp
EXPOSE 5000
# Run the main.py script
CMD ["python", "main.py"]