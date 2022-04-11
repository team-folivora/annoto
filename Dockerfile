FROM debian

SHELL ["/bin/bash", "--login", "-c"]

RUN apt update && \
    apt install -y sudo curl tmux && \
    apt install -y libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb

# Setup user
RUN useradd -ms /bin/bash a && \
    adduser a sudo && \
    passwd -d a && \
    echo "" > /home/a/.bashrc
USER a
WORKDIR /home/a

# Setup python
RUN sudo apt install -y python3 python3-pip && \
    pip install virtualenv

# Setup node
COPY --chown=a static/.nvmrc .nvmrc
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.2/install.sh | bash
RUN nvm install && \
    nvm use && \
    npm install -g cypress@9.5.2

# Create directories
RUN mkdir /home/a/annoto && \
    mkdir /home/a/annoto/api && \
    mkdir /home/a/annoto/static && \
    mkdir /home/a/.annoto

# Setup .bashrc
RUN printf "[ -f ~/annoto/api/venv/bin/activate ] || python3 -m virtualenv ~/annoto/api/venv\nsource ~/annoto/api/venv/bin/activate\n" >> /home/a/.bashrc

# Copy fixtures
WORKDIR /home/a/.annoto
COPY --chown=a /api/mod/fixtures /home/a/.annoto

# Copy entrypoint
WORKDIR /home/a/annoto
COPY --chown=a /entrypoint.sh entrypoint.sh

EXPOSE 5000
EXPOSE 3000
ENTRYPOINT "./entrypoint.sh"
