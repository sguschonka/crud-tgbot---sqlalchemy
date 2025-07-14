from .form import router as form_router
from .profile import router as profile_router
from .start import router as start_router

routers = (start_router, form_router, profile_router)
