# mail_trace_viewer

A Python/Flask web app that analyzes email headers and displays:
- the SMTP path of messages,
- server geolocation,
- IP reputation with AbuseIPDB,
- an interactive logical map and geographic map.

## 🚀 Requirements
- Docker
- Free API key from [AbuseIPDB](https://www.abuseipdb.com/register)

## 🛠️ Build and Deploy with Docker

### 1. Export the environment variable:
```bash
export ABUSEIPDB_API_KEY=your_api_key
```

### 2. Build the Docker image:
```bash
docker build -t mail_trace_viewer .
```

### 3. Start the container:
```bash
docker run -d -p 8080:8080 --env ABUSEIPDB_API_KEY=$ABUSEIPDB_API_KEY mail_trace_viewer
```

### 4. Access the app:
Open your browser at [http://localhost:8080](http://localhost:8080)

## 🧪 Features
- Advanced parsing of the `Received:` field
- IPv4, IPv6, hostname support with DNS lookup
- AbuseIPDB API with colored reputation (green/red)
- Block logical map + Leaflet geographic map
- Export to JSON

## 📦 Docker
The Docker image:
- Uses `oraclelinux:9-slim` with verified digest
- Python 3.12
- Non-privileged user `appuser`
- Exposes port 8080
- No residual `pip`, `setuptools`, or build tools

## 🧾 Useful notes
- `.dockerignore` helps keep the image small
- Uses `ENTRYPOINT` to launch the app
- Fallback for failed DNS resolutions included

## 📜 License

Distributed under [GNU GPLv3](LICENSE)
