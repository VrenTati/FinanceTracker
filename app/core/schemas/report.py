from datetime import date
from typing import Optional

from pydantic import BaseModel

class ReportFilter(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
