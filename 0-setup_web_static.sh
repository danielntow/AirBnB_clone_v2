#!/usr/bin/env bash
# Sets up web server for deployment of web_static

echo -e "\e[1;32m START\e[0m"

# Update packages
sudo apt-get update -y
sudo apt-get install -y nginx
echo -e "\e[1;32m Packages updated\e[0m"
echo

# Allow incoming NGINX HTTP connections
sudo ufw allow 'Nginx HTTP'
echo -e "\e[1;32m Allowed incoming NGINX HTTP connections\e[0m"
echo

# Create directories and add test string
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo -e "\e[1;32m Directories created\e[0m"
echo "<h1>Welcome to DS ENTERPRISE</h1>" | sudo tee /data/web_static/releases/test/index.html >/dev/null
echo -e "\e[1;32m Test string added\e[0m"

# Prevent overwrite
if [ -d "/data/web_static/current" ]; then
    echo "Path /data/web_static/current exists"
    sudo rm -rf /data/web_static/current
fi
echo -e "\e[1;32m Prevent overwrite\e[0m"

# Create symbolic link and change ownership
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data

# Update Nginx configuration
nginx_config="server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$HOSTNAME;
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
}"

echo "$nginx_config" | sudo tee /etc/nginx/sites-available/default >/dev/null
sudo ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'
echo -e "\e[1;32m Symbolic link created\e[0m"

# Restart NGINX
sudo service nginx restart
echo -e "\e[1;32m Restarted NGINX\e[0m"
