### Backup database with Postgresql installed by Docker
docker run --network="host" -e PGPASSWORD=secretpassword -v ~/postgres_backups:/backup postgres:16.4 pg_dump -h localhost -U postgres -d learning_note_app -F c -f /backup/note_app_before_13.tar

### Restoring using backup file
docker run --network="host" -e PGPASSWORD=secretpassword -v ~/postgres_backups:/backup postgres:16.4 pg_restore -h localhost -U postgres -d backup_note_app /backup/note_app_before_13.tar