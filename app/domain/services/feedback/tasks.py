from app.depends import provider
from app.domain.services.feedback.reminder import send_review_reminders


async def run_review_reminders():
    async for session in provider.get_session():
        await send_review_reminders(session)
