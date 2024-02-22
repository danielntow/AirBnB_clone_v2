#!/usr/bin/env bash
# sets up web server for deployment of web_static

echo -e "\e[1;32m START\e[0m"
#--Update packages
sudo apt-get -y update
sudo apt-get -y install nginx
echo -e "\e[1;32m Packages updated\e[0m"
echo

sudo ufw allow 'Nginx HTTP'
sudo -e "\e[1;32m Allow incomming NGINX HTTP connections\e[0m"
echo

sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo -e "\e[1;32m directories created"
echo "<h1>Welcome to DS ENTERPRIE</h1>" >/data/web_static/releases/test/index.html
echo -e "\e[1;32m Test string added\e[0m"

if [ -d "/data/web_static/current" ]; then
    echo "path /data/web_static/current exists"
    sudo rm -rf /data/web_static/current
fi
echo -e "\e[1;32m prevent overwrite\e[0m"

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data

printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 http://cuberule.com/;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" >/etc/nginx/sites-available/default
sudo ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'
echo -e "\e[1;32m Symbolic link created\e[0m"

sudo service nginx restart
echo -e "\e[1;32m restart NGINX\e[0m"
