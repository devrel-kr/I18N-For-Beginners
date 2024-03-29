# install docker & docker-compose
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
sudo curl -SL https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose


# Clone the weblate-docker repo
git clone https://github.com/WeblateOrg/docker-compose.git weblate-docker
cd weblate-docker


# Create a docker-compose.override.yml file with your settings. See Docker environment variables for full list of environment variables.
echo -n "WEBLATE_EMAIL_HOST : "
read WEBLATE_EMAIL_HOST
echo -n "WEBLATE_EMAIL_HOST_USER : "
read WEBLATE_EMAIL_HOST_USER
echo -n "WEBLATE_EMAIL_HOST_PASSWORD : "
read WEBLATE_EMAIL_HOST_PASSWORD
echo -n "WEBLATE_SERVER_EMAIL : "
read WEBLATE_SERVER_EMAIL
echo -n "WEBLATE_DEFAULT_FROM_EMAIL : "
read WEBLATE_DEFAULT_FROM_EMAIL
echo -n "WEBLATE_SITE_DOMAIN : "
read WEBLATE_SITE_DOMAIN
echo -n "WEBLATE_ADMIN_PASSWORD : "
read WEBLATE_ADMIN_PASSWORD
echo -n "WEBLATE_ADMIN_EMAIL : "
read WEBLATE_ADMIN_EMAIL
echo \
"version: '3'
services:
  weblate:
    ports:
      - 80:8080
    environment:
      WEBLATE_EMAIL_HOST: $WEBLATE_EMAIL_HOST
      WEBLATE_EMAIL_HOST_USER: $WEBLATE_EMAIL_HOST_USER
      WEBLATE_EMAIL_HOST_PASSWORD: $WEBLATE_EMAIL_HOST_PASSWORD
      WEBLATE_SERVER_EMAIL: $WEBLATE_SERVER_EMAIL
      WEBLATE_DEFAULT_FROM_EMAIL: $WEBLATE_DEFAULT_FROM_EMAIL
      WEBLATE_SITE_DOMAIN: $WEBLATE_SITE_DOMAIN
      WEBLATE_ADMIN_PASSWORD: $WEBLATE_ADMIN_PASSWORD
      WEBLATE_ADMIN_EMAIL: $WEBLATE_ADMIN_EMAIL
" > docker-compose.override.yml


# Start Weblate containers
sudo docker-compose up
