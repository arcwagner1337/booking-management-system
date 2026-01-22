from datetime import datetime
from zoneinfo import ZoneInfo

import sqlalchemy as sa
import sqlalchemy.orm as so

from app.infrastructure.database.models.shared import BaseWithDt


class NotificationStatus:
    """Notification statuses."""

    PENDING = "pending"  # Waiting for sending
    PROCESSING = "processing"  # In sending process
    SENT = "sent"  # Successfully sent
    FAILED = "failed"  # Send error


class NotificationType:
    """Notification types."""

    BOOKING_24H = "booking_24h"  # 24 hours before
    BOOKING_1H = "booking_1h"  # 1 hour before
    BOOKING_START = "booking_start"  # Booking start
    BOOKING_END = "booking_end"  # Booking end
    BOOKING_CANCEL = "booking_cancel"  # Booking cancel


class Notification(BaseWithDt):
    """Notification model."""

    __tablename__ = "notifications"

    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        index=True,
    )
    type: so.Mapped[str] = so.mapped_column(
        sa.String(20),
        nullable=False,
        index=True,
    )
    status: so.Mapped[str] = so.mapped_column(
        sa.String(20),
        default=NotificationStatus.PENDING,
        nullable=False,
        index=True,
    )

    # Relationships
    booking_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: so.Mapped[str] = so.mapped_column(
        sa.String(36),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Timestamps
    scheduled_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    processed_at: so.Mapped[datetime | None] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
    )

    # Message info
    message: so.Mapped[str | None] = so.mapped_column(
        sa.Text,
        nullable=True,
    )
    error: so.Mapped[str | None] = so.mapped_column(
        sa.Text,
        nullable=True,
    )

    # Relationships
    booking: so.Mapped["booking.id"] = so.relationship(
        "booking",
        back_populates="notifications",
    )

    @property
    def is_due(self) -> bool:
        """Check if it's time to send notification."""
        return datetime.now(ZoneInfo("UTC")) >= self.scheduled_at

    @property
    def can_be_sent(self) -> bool:
        """Check if notification can be sent."""
        return self.status == NotificationStatus.PENDING and self.is_due
