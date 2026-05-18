FROM python:3.12-slim

WORKDIR /app
COPY . .

CMD ["python", "-m", "src.report", "data/normal-network.csv", "data/beacon-sample.csv"]
