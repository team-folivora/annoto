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
RUN sudo apt install -y python3 python3-pip

# Setup node
COPY --chown=a static/.nvmrc .nvmrc
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.2/install.sh | bash
RUN nvm install && \
    nvm use

# Create directories
RUN mkdir /home/a/annoto && \
    mkdir /home/a/annoto/api && \
    mkdir /home/a/annoto/static

# Install dependencies for api
WORKDIR /home/a/annoto/api
COPY --chown=a /api/requirements.txt requirements.txt
COPY --chown=a /api/requirements-dev.txt requirements-dev.txt
RUN pip install -r requirements-dev.txt

# Install dependencies for static
WORKDIR /home/a/annoto/static
COPY --chown=a /static/package.json package.json
COPY --chown=a /static/package-lock.json package-lock.json
RUN npm install

# Cleanup
RUN rm -r /home/a/.cache && \
    rm -r /home/a/.npm

# Prepare for run
EXPOSE 5000
EXPOSE 3000
WORKDIR /home/a/annoto
COPY --chown=a / .
ENTRYPOINT "./entrypoint.sh"
