# CSE 312 Group Project
## Usage
First, make sure you have docker open
Next, run 
`docker compose up`
to start the Docker container (also opening the database) and head to 
`http://localhost:8080/`
to check out the site.

When you're making changes, you need to recreate the docker image. Do this with
`docker compose up --build --force-recreate`
