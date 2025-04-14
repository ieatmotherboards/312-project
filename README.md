# CSE 312 Group Project
## Usage
First, maek sure you have docker open
Next, run
`docker run -d -p 27017:27017 mongo:latest`
to start the database. Lastly, run 
`docker-compose up --build --force-recreate`
and head to 
`http://127.0.0.1:5000/`
to check out the site.