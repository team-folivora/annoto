FROM debian

SHELL ["/bin/bash", "--login", "-c"]

RUN apt update && \
    apt install -y sudo curl tmux

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
    nvm use

# Create directories
RUN mkdir /home/a/annoto && \
    mkdir /home/a/annoto/api && \
    mkdir /home/a/annoto/static && \
    mkdir /home/a/.annoto

# Copy fixtures
WORKDIR /home/a/.annoto
COPY --chown=a /api/mod/tests/fixtures /home/a/.annoto

# Copy entrypoint
WORKDIR /home/a/annoto
COPY --chown=a /entrypoint.sh entrypoint.sh

EXPOSE 5000
EXPOSE 3000
ENTRYPOINT "./entrypoint.sh"
