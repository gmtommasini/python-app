# python-app
Python application with Flask and api to be hosted on PythonAnywhere
- https://gmtommasini.pythonanywhere.com/
- https://gmtommasini.pythonanywhere.com/qr_code
- https://gmtommasini.pythonanywhere.com/api/music

Since PythonAnywhere does not seem to have a ci-cd pipeline on the free version (at least from now),
after the push to GitHub, go into the PythonAnywhere console and git pull there.
After the Pull, reload the application.

At this moment I just found out that free accounts on pythonanywhere have a block on requests, and then I can't web scrap.
Furthermore, pythonanywhere has no real enviroment variables setup.
From now on, I'll try to move this to AWS, or maybe GCP... T__T


<hr>

# Docker

From the root (Dockerfile location), build the image:
```shell
docker build -t python-app .
```

Run the Docker Container:
```shell
docker run -p 5000:5000 python-app
```

