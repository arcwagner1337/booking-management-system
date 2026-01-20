import asyncio

import uvicorn

from app import get_application
from app.domain.services.feedback.tasks import run_review_reminders

app = get_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, log_level="error")  # noqa: S104
    asyncio.run(run_review_reminders())
