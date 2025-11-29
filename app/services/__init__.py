"""Service layer for business logic.

Services handle all database operations and business rules.
Routes should only call services, never access ORM directly.

Example:
    # app/services/item_service.py
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession
    from ..models import Item

    async def get_items(db: AsyncSession) -> list[Item]:
        result = await db.execute(select(Item))
        return result.scalars().all()

    async def create_item(db: AsyncSession, name: str) -> Item:
        item = Item(name=name)
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item
"""
