#!/usr/bin/env bash
# Bash script that sets up a web server for deployment

# Install Nginx if it is not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt update
    sudo apt install -y nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Welcome to web_static!
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Remove existing symbolic link if it exists and create a new one
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Disable other default server configurations
sudo find /etc/nginx/sites-enabled -type l -exec sudo rm -f {} \;

# Ensure there's only one default server block
nginx_config="/etc/nginx/sites-available/default"
sudo tee $nginx_config > /dev/null <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF

# Enable the default configuration
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Start or restart Nginx service
if [ "$(pgrep -c nginx)" -eq 0 ]; then
    sudo systemctl start nginx
else
    sudo systemctl restart nginx
fi

echo "Web server setup is complete."
