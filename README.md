# Trading Treasure

software dev. group project

- Admin user creds: Username: admin, p/w: admin
- regular user "n": Username: n, p/w: testSDF9

## Nginx/Gunicorn installation instructions
- after creating an aws instance and cloning project, install packages:
    `sudo apt-get update`
    `sudo apt-get install nginx gunicorn python3-venv`
- **NOTE**: in gunicorn and nginx config files, it assumes the project is located at `/home/ubuntu/prod_app`. The project directory was changed for brevity.
- inside project dir, create venv
    `python3 -m venv env`
    `source env/bin/activate`
    `pip3 install django gunicorn`
- collect static files, paths should already be set in django and nginx settings, so  just run:
    `python3 manage.py collectstatic`
    `deactivate` (exit venv)
- copy the gunicorn config files (`gunicorn.service` and `gunicorn.socket`) into the `/etc/systemd/system` folder
    - change their permissions:
        `sudo chown ubuntu:www-data /etc/systemd/system/gunicorn.service`
        `sudo chown ubuntu:www-data /etc/systemd/system/gunicorn.socket`
        
- start and enable gunicorn socket
    `sudo systemctl start gunicorn.socket`
    `sudo systemctl enable gunicorn.socket`
    - make sure it didn't break with `sudo systemctl status gunicorn.socket`
    - test output with `curl --unix-socket /run/gunicorn.socket localhost`
- start gunicorn service
    `sudo systemctl daemon-reload` <- required every time `/etc/systemd/system/gunicorn.service` is changed
    `sudo systemctl start gunicorn.service`
- in `/etc/nginx/nginx.conf`, add to the top of the file: `user ubuntu www-data;`
    - there is a copy of nginx.conf in `nginx_gunicorn_stuff` as well
- in `nginx_gunicorn_stuff/prod_app`, change the `server_name` to whatever the IPv4 auto-assigned DNS address is
- copy `nginx_gunicorn_stuff/prod_app` into `/etc/nginx/sites-available/`
- you can run `sudo nginx -t` to make sure there are no errors with the config
- start nginx: `sudo systemctl restart nginx`
- the site should now be visible at the AWS instance's DNS address

- TODO: enable SSL (letsencrypt/certbot)
- sources:
    - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu
    - make sure permissions are set correctly (ubuntu:www-data): https://stackoverflow.com/questions/55093622/gunicorn-socket-failed-with-result-service-start-limit-hit
    - make sure static paths set in `nginx.conf` and `trading_treasure/settings.py` correctly (are good now): https://realpython.com/django-nginx-gunicorn/#incorporating-nginx

## Setting up Stripe
- 1st (for local dev. and ec2 instance), follow these instructions for installing stripe: https://docs.stripe.com/stripe-cli?install-method=apt 
- then also install `stripe` and `dotenv` python dependency
- on the command line run `stripe login`, login through browser (copy link if needed), **for EC2 instance use tradingtreasure gmail account**
- run `stripe listen --forward-to (address)/webhook`, webhook token value should be updated in settings.py

## Running tests
- change into `tests-standalone/` directory
- run `pytest -q run_all_tests.py`