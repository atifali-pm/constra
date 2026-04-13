# Constra development image.
#
# Layout:
#   - Debian-based Python 3.12 slim base (matches the highest row of the CI
#     matrix so Docker-based dev and CI catch the same issues).
#   - Qt 6 runtime libraries installed via apt so PySide6 wheels have
#     everything they need for both offscreen (tests) and xcb (visual)
#     platforms.
#   - A non-root "dev" user created with a UID/GID that defaults to 1000
#     (the standard first-user id on Ubuntu desktops). Override at build
#     time with --build-arg UID=... --build-arg GID=... if the host user
#     differs — this keeps files created inside the container owned by
#     the host user when /app is bind-mounted.
#   - Project dependencies pre-installed into the image so `docker compose
#     run` starts fast. The source tree is mounted over /app at runtime,
#     and the editable install's .pth file keeps resolving to the mounted
#     code.

FROM python:3.12-slim-bookworm

ARG UID=1000
ARG GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# System packages:
#   - Qt 6 runtime: libgl1, libegl1, libxkbcommon0, libdbus-1-3,
#     libxcb-cursor0, libfontconfig1, libx11-xcb1 and friends.
#   - Mesa + DRI for software/hardware OpenGL (used by VTK in later
#     milestones; harmless to have now).
#   - Fonts so Qt text renders sanely.
#   - git + build-essential for the occasional pip package that needs
#     to compile from sdist.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        ca-certificates \
        curl \
        # Qt / X11
        libglib2.0-0 \
        libgl1 \
        libegl1 \
        libopengl0 \
        libglx-mesa0 \
        libdbus-1-3 \
        libxkbcommon0 \
        libxkbcommon-x11-0 \
        libxcb-cursor0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-util1 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
        libx11-xcb1 \
        libxrender1 \
        libxi6 \
        libsm6 \
        libice6 \
        libfontconfig1 \
        libfreetype6 \
        libdrm2 \
        # GLX / Mesa
        libglu1-mesa \
        mesa-utils \
        # Fonts
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Create a matching-UID dev user. Using groupadd/useradd with --no-log-init
# avoids the slow lastlog padding issue on some hosts.
RUN groupadd --gid ${GID} dev \
    && useradd --uid ${UID} --gid ${GID} --shell /bin/bash --create-home --no-log-init dev

WORKDIR /app

# Install the project with dev extras. We first copy only pyproject.toml
# and a minimal package skeleton so Docker can cache the heavy dependency
# layer (PySide6 is ~250MB) independently of source-file churn.
COPY --chown=dev:dev pyproject.toml README.md LICENSE /app/
RUN mkdir -p /app/src/constra \
    && echo '__version__ = "0.0.0"' > /app/src/constra/__init__.py \
    && pip install --upgrade pip \
    && pip install -e ".[dev,docs]" \
    && rm -rf /app/src

# Copy the real source in. At runtime the compose file bind-mounts the
# whole repo on top of /app so edits on the host are live.
COPY --chown=dev:dev . /app

USER dev

# Qt environment defaults. QT_QPA_PLATFORM is left unset here so the
# container picks xcb (visual) by default; override to "offscreen" for
# tests. QT_X11_NO_MITSHM avoids shared-memory issues across the X
# socket boundary.
ENV QT_X11_NO_MITSHM=1 \
    PATH=/home/dev/.local/bin:/usr/local/bin:/usr/bin:/bin

CMD ["bash"]
