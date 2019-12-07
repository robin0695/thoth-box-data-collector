# download paper
After we install pymysql, when we run the command `scrapy crawl sanity_spyder`, it will raise an error:
jango.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3

To solve this problem, we need to manually remove this constrain in the python source code:
/Users/weiwang/Workspaces/projects/thoth_box/thoth_env/lib/python3.7/site-packages/django/db/backends/mysql/base.py in line 36.

Another bug in File "/Users/weiwang/Workspaces/projects/thoth_box/thoth_env/lib/python3.7/site-packages/django/db/backends/mysql/operations.py", line 146, in last_executed_query
`query = query.decode(errors='replace')`
AttributeError: 'str' object has no attribute 'decode'

Fix: change the decode to encode 



# Paper Process commands

start the celery worker and beat process

1. `cd ROOT_FOLDER`
2. `celery -A config worker -l info`
3. `celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`

## Tasks

- process_paper: main_task, download and process the pdf files. It is scheduled to run every 10 minutes.
- pdf2html: transform the pdf to html
- pdf2text: extract the text data from pdf

## Config Solr
- start solr: `$SOLR_HOME/bin/solr start`
- create a core: `$SOLR_HOME/bin/solr create -c thoth_box -n basic_config` the core conf will locate in $SOLR_HOME/server/solr/thoth_box/conf
- create the schema.xml using haystack: `python manage.py build_solr_schema --configure-directory=$SOLR_HOME/server/solr/thoth_box/conf --filename=schema.xml`
- create the index: `python manage.py rebuild_index`

