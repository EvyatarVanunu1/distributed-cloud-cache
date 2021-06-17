import os

from node.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host=os.getenv("NODE_HOST", "0.0.0.0"), port=os.getenv("NODE_PORT", 80))