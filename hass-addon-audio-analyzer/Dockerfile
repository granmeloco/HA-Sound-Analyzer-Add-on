ARG BUILD_FROM=ghcr.io/home-assistant/$BUILD_ARCH-base:latest
FROM $BUILD_FROM

# Systempakete inkl. Pulse-Tools
RUN apk add --no-cache \
    python3 py3-pip ffmpeg \
    alsa-utils alsa-plugins-pulse \
    pulseaudio-utils \
    libsndfile portaudio

# Virtuelle Umgebung für Python (um PEP 668 zu umgehen)
RUN python3 -m venv /venv \
 && /venv/bin/pip install --upgrade pip \
 && /venv/bin/pip install --no-cache-dir \
      numpy scipy soundfile sounddevice paho-mqtt

ENV PATH="/venv/bin:${PATH}"

WORKDIR /app
COPY run.sh /run.sh
RUN chmod a+x /run.sh
COPY wp_audio_trigger.py /app/wp_audio_trigger.py

VOLUME /data
CMD [ "/run.sh" ]
