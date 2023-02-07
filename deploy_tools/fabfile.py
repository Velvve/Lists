from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/Velvve/Lists'


def deploy():
    """развернуть"""
    site_folder = f'/home/{env.user}/site/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_lates_source(source_folder)
    _update_setting(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    """Создать структуру каталога, если нужно"""
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_lates_source(source_folder):
    """Получить самый свежий исходный код"""
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_setting(source_folder, site_name):
    """Обновить настройки"""
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG=True", 'DEBUG=False')
    sed(settings_path,
        'ALLOWED_HOST = .+$',
        f'ALLOWED_HOST = ["{site_name}"]')
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = '2xr2-^*7o$d_pljuyk2r83c@ko!_*1n+z=gcbfu80smye&5^'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\n from .secret_key import SECRET_KEY')
    append(settings_path, "CSRF_TRUSTED_ORIGINS = ['http://beautiful-list.site', 'http://127.0.0.1:8000/']")


def _update_virtualenv(source_folder):
    """Обновить виртуальную среду"""
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.10 -m pip venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/ requirements.txt')


def _update_static_files(source_folder):
    """Обновить статические файлы"""
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )


def _update_database(source_folder):
    """Обновить базу данных"""
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )
