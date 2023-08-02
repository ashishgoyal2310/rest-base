# Prerequisite

- python:3.9
- Docker

## Deploy/Run as Docker Container

- docker build . -t myimage
- docker run myimage:latest
- docker run --name web_cont -p 38000:8000 -e APP_ENV=local myimage:latest python manage.py runserver 0.0.0.0:8000

    ### Run redis as container
    - docker run -d --name redis_cont redis

    ### RUN webapp(local) as container with redis link
    - docker run -d --name web_cont -p 38000:8000 -e APP_ENV=local --link redis_cont:redis_cont -e REDIS_HOST=redis_cont myimage:latest python manage.py runserver 0.0.0.0:8000

    ### RUN celery(local) as container with redis link
    - docker run -d --name celery_cont -e APP_ENV=local --link redis_cont:redis_cont -e REDIS_HOST=redis_cont myimage:latest celery -A config.celery:app worker -l INFO -f ./logs/celery.log --concurrency=3

    ### Run mysql as container
    - docker run -d --name mysql_cont -p 33306:3306 -v /opt/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=[ROOT_PASSWORD] mysql:8.0

        ### Docker mysql commands
        - docker exec -it mysql_cont mysql -p[ROOT_PASSWORD]
        - docker exec mysql_cont mysql -p[ROOT_PASSWORD] -e 'CREATE DATABASE mission; CREATE USER "[DB_USER]"@"%" IDENTIFIED BY "[DB_PASSWORD]"; GRANT ALL PRIVILEGES ON *.* TO "[DB_USER]"@"%";'
        - docker exec mysql_cont mysql -p[ROOT_PASSWORD] -e 'SHOW DATABASES; SELECT user,host,Super_priv FROM mysql.user; SHOW GRANTS FOR "[DB_USER]";'

    ### RUN webapp(dev) as container
    - docker run -d --name web_cont -p 38000:8000 -e APP_ENV=dev --link redis_cont:redis_cont -e REDIS_HOST=redis_cont --link mysql_cont:mysql_cont -e DB_HOST=mysql_cont -e DB_PORT=33306 -e DB_USER=[DB_USER] -e DB_PASSWORD=[DB_PASSWORD] -e DB_NAME=mission myimage:latest python manage.py runserver 0.0.0.0:8000


- eval $(echo -e $(cat root))
