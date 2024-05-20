from typing import Annotated, Tuple

from fastapi import WebSocket


class Queue:
    def __init__(self):
        self.queue: List[WebSocket] = []
        # Use list because maximum length of 2 expected

    def add(self, user: WebSocket):
        if user not in self.queue:
            self.queue.append(user)

    def get_first_two(self) -> Annotated[Tuple[WebSocket], 2] | Annotated[Tuple[None], 2]:
        # If queue has more than one user
        if len(self.queue) > 1:
            # Remove first two users from queue
            return self.queue.pop(0), self.queue.pop(0)
        return None, None

    def remove(self, user: WebSocket):
        try:
            self.queue.remove(user)
        except ValueError:
            pass
