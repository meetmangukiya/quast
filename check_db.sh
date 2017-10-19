#!/usr/bin/env bash
set -e -x

echo 'Creating database...'
./manage_db.sh create

echo 'Setting up the database...'
./manage_db.sh setup

echo 'All tables: '
psql -U postgres -d quast -c "\dt"

echo 'Populating the database...'
./manage_db.sh populate

echo 'Destructing the database...'
./manage_db.sh destruct

echo 'All tables: '
psql -U postgres -d quast -c "\dt"

echo 'Dropping the database...'
./manage_db.sh drop

