# Prerequisite

- python:3.9
- Docker

## Deploy/Run as Docker Container

- docker build . -t myimage
- docker run myimage:latest
- docker run --name web_cont -p 38000:8000 -e APP_ENV=local myimage:latest python manage.py runserver 0.0.0.0:8000
- docker exec web_cont python manage.py migrate
- docker exec -it web_cont python manage.py createsuperuser

## Run on Local Environment

- redis for cache and celery broker and will use sqlite DB so no need to run mysql container.

    ### Run redis as container
    - docker run -d --name redis_cont redis

    ### Run webapp(local) as container with redis link
    - docker run -d --name web_cont -p 38000:8000  
        -e APP_ENV=local  
        -v ./logs:/app/logs -v ./db:/app/db  
        --link redis_cont:redis_cont -e REDIS_HOST=redis_cont  
        myimage:latest python manage.py runserver 0.0.0.0:8000 

    ### Run celery(local) as container with redis link
    - docker run -d --name celery_cont  
        -e APP_ENV=local  
        -v ./logs:/app/logs -v ./db:/app/db  
        --link redis_cont:redis_cont -e REDIS_HOST=redis_cont  
        myimage:latest celery -A config.celery:app worker -l INFO -f ./logs/celery.log --concurrency=3

## Run on Dev/QA/UAT Environment

- redis for cache & celery broker and mysql DB.

    ### Run redis as container
    - docker run -d --name redis_cont redis

    ### Run mysql as container
    - docker run -d --name mysql_cont -p 3306:3306 -v /opt/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=[ROOT-PASSWORD] -e MYSQL_DATABASE=mission mysql:8.0

        ### Docker mysql commands
        - docker exec -it mysql_cont mysql -p[ROOT-PASSWORD]
        - docker exec mysql_cont mysql -p[ROOT-PASSWORD] -e 'CREATE USER "DevUser"@"%" IDENTIFIED BY "DevPassword";'
        - docker exec mysql_cont mysql -p[ROOT-PASSWORD] -e 'GRANT ALL PRIVILEGES ON *.* TO "DevUser"@"%";'
        - docker exec mysql_cont mysql -p[ROOT-PASSWORD] -e 'SHOW DATABASES; SELECT user,host,Super_priv FROM mysql.user; SHOW GRANTS FOR "DevUser";'

    ### Run webapp(dev) as container with redis and mysql link
    - docker run -d --name web_cont -p 38000:8000  
        -e APP_ENV=dev  
        -v ./logs:/app/logs -v ./db:/app/db  
        --link redis_cont:redis_cont -e REDIS_HOST=redis_cont  
        --link mysql_cont:mysql_cont -e DB_HOST=mysql_cont -e DB_PORT=3306 -e DB_USER=DevUser -e DB_PASSWORD=DevPassword -e DB_NAME=mission  
        myimage:latest python manage.py runserver 0.0.0.0:8000

    ### Run celery(dev) as container with redis and mysql link
    - docker run -d --name celery_cont  
        -e APP_ENV=dev  
        -v ./logs:/app/logs -v ./db:/app/db  
        --link redis_cont:redis_cont -e REDIS_HOST=redis_cont  
        --link mysql_cont:mysql_cont -e DB_HOST=mysql_cont -e DB_PORT=3306 -e DB_USER=DevUser -e DB_PASSWORD=DevPassword -e DB_NAME=mission  
        myimage:latest celery -A config.celery:app worker -l INFO -f ./logs/celery.log --concurrency=3
