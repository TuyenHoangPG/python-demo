# Rest API with Python Flask and PostgresSQL

This is simple REST API example for Flask framework with Postgres Database.

## Module

- Integrate with Postgresql

- Login/Register

- CRUD

- Advanced feature: Queue, cache, ...

- Deploy

### Project structure

The project code base is mainly located within the `src` folder. This folder is divided in:

- `api` - containing all versions of api. Each version contain code base of each modules like models, controllers, routers, etc.
- `shared` - containing common module for the project like configs, constant, etc.
- `test` - containing unit test for all function, using Pytest (Not implement yet).
- `migrations` - containing all database migration files

```
.
├── src
│   ├── api                                   # Contain api versioning
│   │   ├── v1                                # Code base of each version
│   │   │   ├── controllers                   # Controllers
│   │   │   │   └── user_controller.py
│   │   │   ├── dtos                          # Data Transfer Objects
│   │   │   │   └── user_dto.py
│   │   │   ├── logs                          # Save logs file
│   │   │   │
│   │   │   ├── middlewares                   # Middlewares code base
│   │   │   │   └── __init__.py
│   │   │   ├── models                        # Data model - communicate with database
│   │   │   │   └── user_model.py
│   │   │   ├── routes                        # Routes config
│   │   │   │   └── user_route.py
│   │   │   ├── validations                   # Data validation schema
│   │   │   │   └── auth_validation.py
│   │   │   └── __init__.py                   # Register all route
│   │   │
│   │   └── app.py                            # Serve Flask app
│   │
│   └── shared                                # Contains all shared datas
│       ├── configs                           # Configs
│       ├── constants                         # Constants
│       └── utils                             # Utility code base
│
├── test                                      # Unit test code base (PyTest)
├── migrations                                # Contain all database migration files

```

## Local Run

### Prepare env and package

- Create file .env simular with file `dev.env.example` in folder `environments`
- Replace **DATABASE_URL** and **SECRET_KEY** with your environment
- Install packages using `pipenv`

```
# pipenv shell
# pipenv install
```

- Or install packages using requirements

```
# python3 -m venv venv
# source venv/bin/activate
# pip3 install -r requirements.txt
```

### Run App

- Run Flask App

```
# export FLASK_APP=src/app.py
# flask run
```

- Run service worker (please make sure that you started **Redis** before)

```
# python3 -u src/worker.py
```

### Setup Database

- Install posgresql
- Run migration if folder `migrations` is already exist

```
# flask db upgrade
```

- If you want to create new migration file

```
# flask db migrate -m "[Message]"
# flask db upgrade
```

- For new project setup, run the following command

```
# flask db init
# flask db migrate -m "[Message]"
# flask db upgrade
```

## Deployment

This is simple document to deploy this app to EC2 instance

### Create an EC2 instance

- You need to get public IPv4 and key pair file, ex: 54.196.178.131 and demo-key.cer

### SSH to this instance

- Run command:

```
# ssh -i [key-pair-file] ubuntu@[public-ip]
```

- If you get an error: `It is required that your private key files are NOT accessible by others. This private key will be ignored`. Try this:

```
# chmod 400 [key-pair-file]
```

### Install some service

We need some services to serve this app like Python, Git, PM2, Redis, Postgres, Nginx.

### Clone project, install package, run with PM2

- To clone project, run the following command

```
# mkdir project && cd project
# git clone https://github.com/TuyenHoangPG/python-demo.git
# cd python-demo

```

- Install package, see step **Prepare env and package** above
- Run with PM2

```
# export FLASK_APP=src/app
# pm2 start "flask run" --name="api"
# pm2 start "python3 -u src/worker.py" --name="service-worker"
```

Config Nginx

- To check web server status, if status is active, you can see Nginx page default when access url `http:[public-ip]`

```
# systemctl status nginx
```

- Setup server block

  - Create the directory for your_domain as follows, using the -p flag to create any necessary parent directories:

  ```
  # sudo mkdir -p /var/www/your_domain/html
  ```

  - Next, assign ownership of the directory with the $USER environment variable:

  ```
  # sudo chown -R $USER:$USER /var/www/your_domain/html
  ```

  - In order for Nginx to serve this content, it’s necessary to create a server block with the correct directives. Let’s make a new one at /etc/nginx/sites-available/your_domain:

  ```
  # sudo nano /etc/nginx/sites-available/your_domain
  ```

  - Paste in the following configuration block, which is similar to the default, but updated for our new directory and domain name:

  ```
  # Basic example
  server {
    listen 80;
    listen [::]:80;
    server_name [your_domain];
    access_log /var/log/nginx/[your_domain]-access.log;
    error_log /var/log/nginx/[your_domain]-error.log;
    client_max_body_size 50M;
    proxy_connect_timeout       1200;
    proxy_send_timeout          1200;
    proxy_read_timeout          1200;
    send_timeout                1200;
    location / {
        proxy_pass    http://127.0.0.1:5000/;
    }
  }
  ```

  - Next, let’s enable the file by creating a link from it to the sites-enabled directory, which Nginx reads from during startup:

  ```
  # sudo ln -s /etc/nginx/sites-available/your_domain /etc/nginx/sites-enabled/
  ```

  - To avoid a possible hash bucket memory problem that can arise from adding additional server names, it is necessary to adjust a single value in the /etc/nginx/nginx.conf file. Open the file:

  ```
  # sudo nano /etc/nginx/nginx.conf
  ```

  - Find the server_names_hash_bucket_size directive and remove the # symbol to uncomment the line. If you are using nano, you can quickly search for words in the file by pressing CTRL and w.
  - Next, test to make sure that there are no syntax errors in any of your Nginx files:

  ```
  # sudo nginx -t
  ```

  - If there aren’t any problems, restart Nginx to enable your changes:

  ```
  # sudo systemctl restart nginx
  ```

Add https with certbot and nginx

```
# sudo apt install certbot python3-certbot-nginx

# sudo certbot —nginx -d your-domain.com -d www.your-domain.com
```
