apache24:
  pkg.installed: []
  service.running:
    - enable: True
    - reload: True
    - require:
      - pkg: apache24
      - pkg: ap24-mod_wsgi4
      - pkg: py27-bottle
    - watch:
      - file: /usr/local/etc/apache24/httpd.conf
      - file: /usr/local/www/apache24/hooks/hooks.wsgi
      - file: /usr/local/etc/apache24/extra/httpd-vhosts.conf
      - file: /usr/local/etc/apache24/modules.d/270_mod_wsgi.conf

/usr/local/etc/apache24/httpd.conf:
  file.managed:
    - source: salt://apache24/templates/httpd.conf

/usr/local/etc/apache24/extra/httpd-vhosts.conf:
  file.managed:
    - source: salt://apache24/templates/httpd-vhosts.conf

ap24-mod_wsgi4:
  pkg.installed

/usr/local/www/apache24/hooks/hooks.wsgi:
  file.managed:
    - makedirs: True
    - source: salt://apache24/scripts/hooks.wsgi

/usr/local/etc/apache24/modules.d/270_mod_wsgi.conf:
  file.managed:
    - source: salt://apache24/templates/270_mod_wsgi.conf

/usr/local/www/apache24/hooks/repositories:
  file.directory:
    - makedirs: True
    - user: www
    - group: www
    - mode: 755

py27-bottle:
  pkg.installed

cgit:
  pkg.installed

/usr/local/etc/cgitrc:
  file.managed:
    - template: jinja
    - source: salt://apache24/templates/cgitrc

/usr/local/www/apache24/hooks/replication.map:
  file.managed:
    - source: salt://apache24/replication.map
