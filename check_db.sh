#!/usr/bin/env bash
set -e -x

echo 'Creating database...'
createdb quast

echo 'Setting up the database...'
psql -U postgres -d quast -a -f setup.sql -v "ON_ERROR_STOP=1"

echo 'Populating the database...'
psql -U postgres -d quast -a -f populate.sql -v "ON_ERROR_STOP=1"

echo 'Destructing the database...'
psql -U postgres -d quast -a -f destruct.sql -v "ON_ERROR_STOP=1"

echo 'All tables: '
psql -U postgres -d quast -c "\dt"
