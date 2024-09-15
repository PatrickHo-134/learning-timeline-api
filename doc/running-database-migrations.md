Running Migrations on Production Database on Heroku
===================================================

This guide provides step-by-step instructions for creating and applying migrations to the production database on Heroku, including creating a backup and rolling back the database if necessary.

Table of Contents
-----------------

1.  [Create Migrations in Local Environment](#create-migrations-in-local-environment)
2.  [Backup Production Database](#backup-production-database)
3.  [Apply Migration on Production Using Terminal](#apply-migration-on-production-using-terminal)
4.  [Rollback the Database if Necessary](#rollback-the-database-if-necessary)

1\. Create Migrations in Local Environment
------------------------------------------

Before applying any migrations to the production database, you need to create and test them in your local environment.

### Steps:

1.  **Update Your Models:**

    -   Modify your Django models as needed (e.g., changing table names, adding/removing fields).

2.  **Create Migrations:**

    -   Run the following command to generate the migration files:

        ```bash
        python manage.py makemigrations
        ```

3.  **Apply Migrations Locally:**

    -   Test the migrations in your local environment to ensure they work as expected:

        ```bash
        python manage.py migrate
        ```

4.  **Verify Locally:**

    -   Check that the changes have been applied correctly in your local database.
    -   Ensure the application runs without issues.

2\. Backup Production Database
------------------------------

Before applying the migration to the production database, it's critical to create a backup to avoid data loss in case something goes wrong.

### Steps:

1.  **Log in to Heroku:**

    -   Ensure you are logged in to the Heroku CLI:

        ```bash
        heroku login
        ```

2.  **Create a Backup:**

    -   Use the `pg:backups` command to create a backup of your production database:

        ```bash
        heroku pg:backups:capture --app learning-timeline-api
        ```

3.  **Download the Backup:**

    -   You can download the backup for safekeeping using:

        ```bash
        heroku pg:backups:download --app learning-timeline-api
        ```

3\. Apply Migration on Production Using Terminal
------------------------------------------------

After creating a backup, you can safely apply the migration to the production database.

### Steps:

1.  **Push Your Code to Heroku:**

    -   Commit your changes locally and push the updated code to Heroku:

        ```bash
        git add .
        git commit -m "Applied migrations"
        git push heroku main  # Or the appropriate branch you're deploying
        ```

2.  **Run Migrations on Heroku:**

    -   Run the migrations on the production database using:

        ```bash
        heroku run python manage.py migrate --app learning-timeline-api
        ```

3.  **Verify the Migration:**

    -   Check that the migrations were applied successfully and that the application is running correctly.

4\. Rollback the Database if Necessary
--------------------------------------

If something goes wrong during the migration process, you can roll back the database to the last known good state.

### Steps:

1.  **List Available Backups:**

    -   List all available backups using:

        ```bash
        heroku pg:backups --app learning-timeline-api
        ```

2.  **Restore the Backup:**

    -   Use the `pg:backups:restore` command to restore the backup:

        ```bash
        heroku pg:backups:restore <backup-name> DATABASE_URL --app learning-timeline-api
        ```

    -   Replace `<backup-name>` with the name or ID of the backup you want to restore.

3.  **Verify the Restore:**

    -   Check that the database has been restored correctly and that the application is back to its previous state.

* * * * *

### Notes

-   **Downtime:** During migrations, especially complex ones, there might be some downtime. Plan your deployment during off-peak hours if possible.
-   **Testing:** Always test migrations thoroughly in a staging environment before applying them to production.

This guide should help you safely manage your production database migrations on Heroku.