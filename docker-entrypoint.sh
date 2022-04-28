
echo "Check if mysql is available."

python /testdb.py

if [ ! -f /.initdj ] ;then
    python manage.py makemigrations
    python manage.py migrate

    # CU="from django.contrib.auth.models import User;"
    # CU="${CU} User.objects.create_superuser('admin', 'admin@example.com', 'pass')"
    # CU="${CU} if User.objects.filter(username='admin').count() == 0 else None"
    python manage.py shell
    touch /.initdj
fi

exec "$@"