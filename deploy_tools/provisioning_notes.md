Обеспечение работы нового сайта
===============================
## Необходимые пакеты;
* nginx
* Python 3.10
* virtualenv + pip
  * Git
   В Ubuntu/Debian
      sudo add-apt-repository ppa:fkrull/deadsnakes
      sudo apt-get install nginx git python python 3.10-venv

## Конфигурация виртуального узла Nginx

* см. nginx.template.conf
* заменить SITENAME

## Служба Systemd

* см. gunicorn-systemd.template.service
* заменить SITENAME