import asyncio
import logging
from typing import Dict, Optional

from fastapi import APIRouter, HTTPException

from .bridge_models import BridgeCommand, BridgeResult
from .logging_utils import PerformanceLogger

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/internal", tags=["bridge"])


class BridgeManager:
    def __init__(self):
        self.command_queue: asyncio.Queue[BridgeCommand] = asyncio.Queue()
        self.pending_results: Dict[str, asyncio.Future] = {}

    async def execute_command(self, command: BridgeCommand, timeout: float = 30.0) -> BridgeResult:
        """Push a command to the queue and await its result.
        """
        with PerformanceLogger("BRIDGE_EXEC", f"Queuing command {command.id} type={command.type}"):
            future = asyncio.Future()
            self.pending_results[command.id] = future
            await self.command_queue.put(command)
            logger.info(f"Command {command.id} put in queue. Queue size: {self.command_queue.qsize()}")

            try:
                logger.info(f"Waiting for result of command {command.id} (timeout={timeout}s)...")
                result = await asyncio.wait_for(future, timeout=timeout)
                return result
            except asyncio.TimeoutError:
                logger.error(f"Command {command.id} timed out.")
                if command.id in self.pending_results:
                    del self.pending_results[command.id]
                raise HTTPException(status_code=504, detail="Command execution timed out")

    async def get_next_command(self, timeout: float = 20.0) -> Optional[BridgeCommand]:
        """Wait for a command to be available.
        Called by the Addon (long polling).
        """
        try:
            # We wait for a command.
            command = await asyncio.wait_for(self.command_queue.get(), timeout=timeout)
            return command
        except asyncio.TimeoutError:
            return None

    def resolve_result(self, result: BridgeResult):
        logger.info(f"Resolving result for command {result.command_id}")
        if result.command_id in self.pending_results:
            future = self.pending_results.pop(result.command_id)
            if not future.done():
                future.set_result(result)
        else:
            logger.warning(f"Received result for unknown or timed-out command: {result.command_id}")


bridge_manager = BridgeManager()


@router.post("/get_command")
async def get_command():
    """Long polling endpoint for the Addon to fetch commands.
    """
    # Timeout slightly less than client timeout to return "no_command"
    # logger.info("Bridge: Client polling for command...") # Too verbose for loop
    command = await bridge_manager.get_next_command(timeout=10.0)
    if command:
        logger.info(f"Bridge: Sending command {command.id} to client.")
        # pydantic model_dump in v2
        return {"status": "command", "command": command.model_dump()}
    else:
        return {"status": "no_command"}


@router.post("/post_result")
async def post_result(result: BridgeResult):
    """Endpoint for the Addon to post execution results.
    """
    logger.info(f"Bridge: Received result for command {result.command_id}. Status: {result.status}")
    bridge_manager.resolve_result(result)
    return {"status": "received"}


def get_bridge_manager():
    return bridge_manager
