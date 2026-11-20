import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Debug activé uniquement si FLASK_DEBUG=1 (jamais en production)
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
