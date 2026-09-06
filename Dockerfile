FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       ca-certificates \
       nodejs \
       npm \
       git \
    && rm -rf /var/lib/apt/lists/*

# Install Deno
RUN curl -fsSL https://deno.land/install.sh | sh

ENV DENO_INSTALL=/root/.deno
ENV PATH="/root/.deno/bin:${PATH}"

# Install bgutil PO Token Provider
RUN git clone --depth 1 \
    https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git \
    /opt/bgutil-ytdlp-pot-provider

WORKDIR /opt/bgutil-ytdlp-pot-provider/server

RUN npm ci
RUN npm run build

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["sh", "-c", "node /opt/bgutil-ytdlp-pot-provider/server/build/main.js --host 127.0.0.1 --port 4416 & uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"]
