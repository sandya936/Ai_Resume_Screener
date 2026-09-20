import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
import app.db.models

async def check():
    db_url = "sqlite+aiosqlite:///./agentx.db"
    print(f"Testing connection with {db_url}...")
    engine = create_async_engine(db_url, echo=False)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Successfully created/verified SQLite database tables!")
    except Exception as e:
        print(f"DB Error: {e}", file=sys.stderr)
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check())
