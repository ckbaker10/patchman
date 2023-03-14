
´´´
mkdir -p /var/www/patchman
docker cp patchman:/build/patchman/static /var/www/patchman/
chown -R root:www-data /var/www/patchman
´´´