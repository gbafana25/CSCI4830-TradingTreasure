# Trading Treasure

software dev. group project

- Admin user creds: Username: admin, p/w: admin
- regular user "n": Username: n, p/w: testSDF9

## Nginx/Gunicorn installation
- TODO: add actual instructions, enable SSL (letsencrypt/certbot), sources:
    - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu
    - make sure permissions are set correctly (ubuntu:www-data): https://stackoverflow.com/questions/55093622/gunicorn-socket-failed-with-result-service-start-limit-hit
    - make sure static paths set in `nginx.conf` and `trading_treasure/settings.py` correctly (are good now): https://realpython.com/django-nginx-gunicorn/#incorporating-nginx
