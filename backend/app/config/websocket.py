import os
import asyncio
import redis.asyncio as redis
from fastapi import WebSocket, WebSocketDisconnect
from app.config.settings import settings
from app.adapters.log_adapter import LogAdapter

async def websocket_broadcaster(websocket: WebSocket, job_id: str):
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe(job_id)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=5)
            if message:
                await websocket.send_text(message['data'])
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        LogAdapter.error(f"WebSocket Error in job {job_id}: {e}")
    finally:
        await pubsub.unsubscribe(job_id)
        await pubsub.close()
        await r.close()