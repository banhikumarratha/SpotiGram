from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.models import Connection, ConnectionStatus, UserAccount
import uuid
from datetime import datetime

class SocialService:
    def __init__(self, session: AsyncSession, publisher=None):
        self.session = session
        self.publisher = publisher

    async def follow_user(self, follower_id: str, followed_id: str):
        if follower_id == followed_id:
            raise ValueError("Cannot follow yourself")
            
        result = await self.session.execute(
            select(Connection).where(
                Connection.follower_id == follower_id,
                Connection.followed_id == followed_id
            )
        )
        connection = result.scalar_one_or_none()
        
        if connection:
            if connection.status == ConnectionStatus.ACTIVE:
                raise ValueError("Already following")
            elif connection.status == ConnectionStatus.BLOCKED:
                raise ValueError("Cannot follow blocked user")
            connection.status = ConnectionStatus.ACTIVE
        else:
            connection = Connection(follower_id=follower_id, followed_id=followed_id, status=ConnectionStatus.ACTIVE)
            self.session.add(connection)
            
        await self.session.commit()
        
        if self.publisher:
            event = {
                "headers": {
                    "event_id": str(uuid.uuid4()),
                    "correlation_id": "none",
                    "idempotency_key": str(uuid.uuid4()),
                    "timestamp": datetime.utcnow().isoformat(),
                    "version": "v1"
                },
                "payload": {
                    "follower_id": follower_id,
                    "followed_id": followed_id
                }
            }
            await self.publisher.publish(event)
            
        return {"status": "success", "follower": follower_id, "followed": followed_id}
