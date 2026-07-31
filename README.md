# Hotel Registration CRUD App (Flask)

A simple Flask web application to Create, Read, Update, and Delete hotel registration records, using SQLite as the database.

## Features
- Add new hotel records (name, owner, address, city, rooms, phone)
- View all registered hotels in a table
- Edit existing hotel details inline
- Delete hotel records
- Auto-creates the `instance/example.db` SQLite database and `hotels` table on first run
- Safe to re-run: if the database/table already exists, it will not be recreated or overwritten (`CREATE TABLE IF NOT EXISTS`)
