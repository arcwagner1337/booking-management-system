"""
API endpoints for room (resource) management.

Structure:
- create.py  - POST   /api/rooms       - create a room
- read.py    - GET    /api/rooms       - list rooms (admin only)
               GET    /api/rooms/{id}  - get room details
- update.py  - PATCH  /api/rooms/{id}  - partial update
- delete.py  - DELETE /api/rooms/{id}  - delete room
"""

from fastapi import APIRouter

from .create import router as create_router
from .delete import router as delete_router
from .read import router as read_router
from .update import router as update_router

router = APIRouter(prefix="/rooms", tags=["Rooms"])

# Include all routers
router.include_router(create_router)
router.include_router(read_router)
router.include_router(update_router)
router.include_router(delete_router)
