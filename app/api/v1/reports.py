from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models.db_helper import db_helper
from core.models.user import User
from core.schemas.report import ReportFilter
from core.services.report_service import ReportService
from .fastapi_users import current_user

router = APIRouter(
    prefix=settings.api.v1.reports
)

@router.post("/report/")
async def get_report(
        filters: ReportFilter,
        db: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(current_user),
):
    report = await ReportService.get_report(
        db, user.id, filters.start_date, filters.end_date
    )
    return report
