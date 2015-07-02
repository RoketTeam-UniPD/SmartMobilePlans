TecWeb_UniPD
============

# Introduzione
All'interno di questo repository viene ospitato il progetto di "Tecnologie Web" relativo al corso di studi 2014-2015 in Informatica presso l'Università di Padova.


# Installazione sistema di sviluppo
```
## Aggiornamento di sistema
sudo apt-get update
sudo apt-get dist-upgrade 


## Installazione perl
sudo apt-get install perl


## Installazione Apache Web Server
sudo apt-get install apache2


## Aggiunto al file di configurazione la riga: ServerName localhost
sudo nano /etc/apache2/apache2.conf
sudo apache2ctl restart


## Installazione moduli PHP5 e Perl per Apache
sudo apt-get install php5 libapache2-mod-php5 libapache2-mod-perl2


## Abilitazione modulo CGI, Perl e PHP5
sudo a2enmod cgi
sudo a2enmod perl
sudo a2enmod php5
sudo apache2ctl restart


## Inserito nel file di configurazione di Apache: sudo nano /etc/apache2/sites-enabled/000-default.conf 

	DocumentRoot /var/www/public_html

	<Directory "/var/www/public_html">
		Options Indexes FollowSymLinks MultiViews
		AllowOverride None
		Order allow,deny
		Allow from all
	</Directory>

	ScriptAlias "/cgi-bin/" "/var/www/cgi-bin/"
	<Directory "/var/www/cgi-bin">
		AllowOverride None
		Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
		AddHandler cgi-script .cgi .pl
		Order allow,deny
		Allow from all
	</Directory>


## Riavvio server Apache
service apache2 restart


## Applicazione permessi alla cartella di esecuzione
sudo chgrp -R www-data /var/www

sudo chmod -R g+w /var/www
sudo chmod g+s /var/www

sudo usermod -d /var/www luca
sudo usermod -a -G www-data  luca

sudo chown -R www-data:www-data /var/www
sudo chmod -R 755 /var/www


## Creazione collegamenti repository e web server
sudo ln -s /repo/tecweb/public_html /var/www/
sudo ln -s /repo/tecweb/data /var/www/
sudo ln -s /repo/tecweb/cgi-bin /var/www/


## Installazione librerie necessarie Perl
sudo apt-get install libapache-session-perl libapache-sessionx-perl libcgi-session-expiresessions-perl libcgi-session-perl libcrypt-ssleay-perl libimage-info-perl libimage-metadata-jpeg-perl libimager-perl libimage-size-perl liblwp-protocol-http-socketunix-perl liblwpx-paranoidagent-perl libnet-dns-perl libnet-smtpauth-perl libnet-smtp-ssl-perl librrds-perl libtemplate-perl libtime-local-perl libunicode-map8-perl libunicode-string-perl libuser-simple-perl libwww-perl libxml-dom-xpath-perl libxml-libxml-iterator-perl libxml-libxslt-perl libxml-nodefilter-perl libxml-simpleobject-enhanced-perl libxml-simpleobject-libxml-perl libxml-simpleobject-perl libxml-smart-perl libxml-twig-perl libxml-xpath-perl libxml-xslt-perl xml-twig-tools libxml-writer-perl libxml-handler-yawriter-perl libhtml-tidy-perl libhtml-lint-perl imagemagick php5-imagick libimage-magick-perl libdatetime-perl libdatetime-format-mail-perl


## Reload Apache
sudo service apache2 graceful
```