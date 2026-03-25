from pathlib import Path
from copy import deepcopy
from django.conf import settings
from django.core.management import call_command
from django.db import connections
from django.utils.text import slugify


HOSPITAL_DB_DIRNAME = 'hospital_databases'


def _build_hospital_alias(code):
	normalized = slugify((code or '').strip()) or 'hopital'
	return f"hopital_{normalized}"


def _build_hospital_db_name(code):
	normalized = slugify((code or '').strip()) or 'hopital'
	return f"{normalized}.sqlite3"


def _build_hospital_db_path(database_name):
	db_dir = Path(settings.BASE_DIR) / HOSPITAL_DB_DIRNAME
	db_dir.mkdir(parents=True, exist_ok=True)
	return db_dir / database_name


def register_hospital_connection(alias, db_path):
	db_path = str(db_path)
	# Reprendre la configuration normalisee de la base par defaut
	# pour conserver toutes les cles attendues par Django (TIME_ZONE, etc.).
	default_settings = deepcopy(connections['default'].settings_dict)
	default_settings['ENGINE'] = 'django.db.backends.sqlite3'
	default_settings['NAME'] = db_path
	default_settings['TIME_ZONE'] = default_settings.get('TIME_ZONE', settings.TIME_ZONE)

	# En test, eviter tout suffixe temporaire sur la base dediee.
	if isinstance(default_settings.get('TEST'), dict):
		default_settings['TEST']['NAME'] = None

	connections.databases[alias] = default_settings


def ensure_hospital_database(hopital):
	alias = hopital.database_alias or _build_hospital_alias(hopital.code)
	database_name = hopital.database_name or _build_hospital_db_name(hopital.code)
	db_path = _build_hospital_db_path(database_name)

	# Keep dedicated DB metadata aligned on the hospital record.
	fields_to_update = []
	if hopital.database_alias != alias:
		hopital.database_alias = alias
		fields_to_update.append('database_alias')
	if hopital.database_name != database_name:
		hopital.database_name = database_name
		fields_to_update.append('database_name')
	if fields_to_update:
		hopital.save(update_fields=fields_to_update)

	register_hospital_connection(alias, db_path)
	call_command('migrate', database=alias, interactive=False, verbosity=0)

	return {
		'alias': alias,
		'database_name': database_name,
		'database_path': str(db_path),
	}

