import os

from orchestrator.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=os.getenv("ORC_PORT", 80))