from fastapi import APIRouter
from .routes.user import user
from .routes.roles import user_roles
from .routes.user import auth
from .routes.party_route import party_router
from app.api.v1.routes.team.teams import team_router
from app.api.v1.routes.team.team_user import user_team_router
from app.api.v1.routes.opt_in import opt_in_base_router
from app.api.v1.routes.notifications import notifications_base_router

version_router = APIRouter(prefix="/v1")
version_router.include_router(user.user_router)
version_router.include_router(auth.auth_router)
version_router.include_router(user_roles.user_role_router)
version_router.include_router(party_router)
version_router.include_router(team_router)
version_router.include_router(user_team_router)
version_router.include_router(opt_in_base_router)
version_router.include_router(notifications_base_router)
