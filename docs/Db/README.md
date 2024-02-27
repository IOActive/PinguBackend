mongo-schema-export.py --uri mongodb://127.0.0.1:27017/ --database pingu_db

mongo-schema-import.py --uri mongodb://127.0.0.1:27017/ --databases pingu_db --verbose --delete-col
