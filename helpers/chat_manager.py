import asyncio

from fastapi import WebSocket

from .connection_manager import ConnectionManager
from .queue import Queue


class ChatManager(ConnectionManager):
    def __init__(self):
        super().__init__()
        self.active_chats: Dict[WebSocket, WebSocket] = {}
        self.queue: List[WebSocket] = Queue()

    async def start_chat(self, user: WebSocket):
        # Add user to queue
        self.queue.add(user)

        # If queue has more than one user, start chat with first two users in queue
        user1, user2 = self.queue.get_first_two()
        if user1 is not None:
            # Add users to chat
            self.active_chats[user1] = user2
            self.active_chats[user2] = user1
            # Tell users that chat has started
            await asyncio.gather(
                user1.send_json({"action": "chat_started"}),
                user2.send_json({"action": "chat_started"}),
            )

    async def send_message(self, message: str, sender: WebSocket):
        recipient = self.active_chats[sender]
        await recipient.send_json({"action": "message_received", "message": message})

    async def end_chat(self, user: WebSocket) -> bool:
        # Remove user from active_chats
        user2 = self.active_chats.pop(user, None)
        # Remove other user from active_chats
        if user2 is not None:
            self.active_chats.pop(user2, None)
            # Tell other user that chat has ended
            await user2.send_json({"action": "chat_ended"})
            return True
        return False

    async def disconnect(self, user: WebSocket):
        # End chat if user is in one
        chat_ended = await self.end_chat(user)
        # Remove user from queue if user is in it
        if not chat_ended:
            self.queue.remove(user)
        # Remove user from active_connections
        super().disconnect(user)
