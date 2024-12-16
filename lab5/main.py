import asyncio

import app
from store import setup_db

if __name__ == "__main__":
    asyncio.run(setup_db())
    app.run()
