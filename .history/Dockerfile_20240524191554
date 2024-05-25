FROM python:3.9-slim

WORKDIR /voice_assistant/app

COPY app /voice_assistant/app

RUN mkdir -p /voice_assistant/logs

ENV LOG_FILE_PATH="/voice_assistant/logs/interaction.log"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libasound2-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    espeak \
    libespeak1 \
    python3-pyaudio \
    alsa-utils \
    pulseaudio \
    libpulse0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r /voice_assistant/app/requirements.txt

CMD ["python", "/voice_assistant/app/assistant.py"]
