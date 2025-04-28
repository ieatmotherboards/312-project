# CSE 312 Group Project
## Docker Deployment Note
This repository uses two different `docker-compose wait` scripts to account for architecture differences between dev and prod. This commit has the version from our homework, but the deployed code is utilizing the version built for aarch64 systems. These changes can be noted in the [Dockerfile](https://github.com/ieatmotherboards/312-project/blob/main/Dockerfile).
## Usage (localhost)
First, make sure you have docker open. Next, run\
`docker compose up`\
to start the Docker container and head to\
`http://localhost:8080/`\
to check out the site.\
**!!! When you're making changes, you need to recreate the docker image. Do this with**\
`docker compose up --build --force-recreate`\
**!!!**
## Usage (deployed)
Head to https://kris-schindler-fan-club.cse312.dev/ to check out the site!