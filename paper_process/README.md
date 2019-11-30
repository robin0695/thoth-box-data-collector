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

