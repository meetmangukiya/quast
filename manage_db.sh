set -e -x

while [ $# != 0 ]
do
    case $1 in
        ("create") createdb quast;;
        ("setup") psql -U postgres -d quast -a -f sql/setup.sql -v "ON_ERROR_STOP=1";;
        ("populate") psql -U postgres -d quast -a -f sql/populate.sql -v "ON_ERROR_STOP=1";;
        ("destruct") psql -U postgres -d quast -a -f sql/destruct.sql -v "ON_ERROR_STOP=1";;
        ("drop") dropdb quast;;
    esac
    shift;
done
