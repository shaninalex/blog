import os
from app import create_app

app = create_app()

DEBUG = bool(int(os.getenv("DEBUG")))

app.run(
    debug=DEBUG,
    host="0.0.0.0",
    port=5000
)
