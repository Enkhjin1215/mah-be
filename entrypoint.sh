#!/bin/sh

# Wait for MySQL database...
echo "Waiting for MySQL database..."
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for MySQL at $DB_HOST:$DB_PORT..."
  sleep 1
done
echo "MySQL database is ready!"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  echo "Waiting for Redis at $REDIS_HOST:$REDIS_PORT..."
  sleep 1
done
echo "Redis is ready!"

# Run database migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput


echo "Starting Django development server..."
exec "$@"