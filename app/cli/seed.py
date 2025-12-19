"""
CLI commands for loading seed data.
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.db.session import get_session
from app.services.seed_service import SeedService


async def load_all():
    """Load all seed data."""
    async for session in get_session():
        service = SeedService(session)
        counts = await service.load_all()
        print("Seed data loaded:")
        for key, count in counts.items():
            print(f"  {key}: {count}")
        break


async def load_schools():
    """Load drafting schools only."""
    async for session in get_session():
        service = SeedService(session)
        count = await service.load_drafting_schools()
        print(f"Loaded {count} drafting schools")
        break


async def load_blocks():
    """Load blocks only."""
    async for session in get_session():
        service = SeedService(session)
        count = await service.load_blocks()
        print(f"Loaded {count} blocks")
        break


async def load_measurements():
    """Load measurement categories only."""
    async for session in get_session():
        service = SeedService(session)
        count = await service.load_measurement_categories()
        print(f"Loaded {count} measurement categories")
        break


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m app.cli.seed <command>")
        print("Commands: load-all, load-schools, load-blocks, load-measurements")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "load-all":
        asyncio.run(load_all())
    elif command == "load-schools":
        asyncio.run(load_schools())
    elif command == "load-blocks":
        asyncio.run(load_blocks())
    elif command == "load-measurements":
        asyncio.run(load_measurements())
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()







