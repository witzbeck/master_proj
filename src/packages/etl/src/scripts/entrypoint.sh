#!/bin/bash

# Execute the database initialization script
python /app/init_db.py

# Check the INITIALIZE_SERVER environment variable
if [ "$INITIALIZE_SERVER" = "true" ]; then
    echo "Initializing server..."
    # Placeholder for server initialization logic (e.g., start a web server)
    # For demonstration, we'll start a simple HTTP server
    python -m http.server 8000
else
    echo "Exiting gracefully after completing analytics operations."
    exit 0
fi
