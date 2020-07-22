### Docker apache2

* C-Styled files
* `.htaccess`
```
AuthType Basic
AuthName "Restricted Content"
AuthUserFile /var/www/html/.htpasswd
Require valid-user
```