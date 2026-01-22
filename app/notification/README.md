# Notification System Integration

## Overview

The notification system is now fully integrated into the booking management system. It automatically creates, schedules, and sends notifications for bookings.

## Components

### 1. **Models** (`app/infrastructure/database/models/`)
- `Notification` - Main notification model with statuses and types
- `NotificationStatus` - Enum for notification states (PENDING, PROCESSING, SENT, FAILED)
- `NotificationType` - Enum for notification types (BOOKING_24H, BOOKING_1H, BOOKING_START, BOOKING_END, BOOKING_CANCEL)

### 2. **Factory** (`app/notification/factory.py`)
- `NotificationFactory` - Creates notification messages based on type
- Message factories for each notification type with customized content

### 3. **Scheduler** (`app/notification/scheduler.py`)
- `NotificationScheduler` - Manages notification queue and processing
- Handles batch processing of pending notifications
- Integrates with Telegram API (mock implementation)

### 4. **Service** (`app/domain/services/notifications/`)
- `NotificationService` - High-level service for notification management
- Methods for creating, retrieving, and updating notifications
- Bulk operations for booking-related notifications

## Database Schema

The `notifications` table includes:
- `id` - Primary key
- `type` - Notification type (enum)
- `status` - Current status (enum)
- `booking_id` - Foreign key to bookings table
- `user_id` - Foreign key to users table (UUID)
- `scheduled_at` - When notification should be sent
- `processed_at` - When notification was processed
- `created_at` - When notification was created
- `message` - Notification message text
- `error` - Error message if failed

Indexes on: `status`, `type`, `scheduled_at`

## Running Database Migration

To apply the notifications table migration:

```bash
# From the project root
alembic upgrade head
```

## Usage Examples

### Create Notifications for a Booking
```python
from app.domain.services.notifications import NotificationService
from app.infrastructure.database.models.booking import Booking

# Get service instance
service = NotificationService(session)

# Create all notifications for a booking
notifications = await service.create_booking_notifications(booking)
```

### Start the Scheduler
```python
from app.notification.scheduler import NotificationScheduler
from app.depends import provider

# Get session
async with provider.session_factory() as session:
    scheduler = NotificationScheduler(session)
    await scheduler.run()  # Runs in infinite loop
```

### Retrieve Pending Notifications
```python
# Get all pending notifications ready to send
notifications = await service.get_pending_notifications(limit=50)
```

### Mark as Processed
```python
# Mark as sent
await service.mark_as_sent(notification, "Message text")

# Mark as failed
await service.mark_as_failed(notification, "Error message")
```

## Notification Types and Timing

1. **BOOKING_24H** - Sent 24 hours before booking start
2. **BOOKING_1H** - Sent 1 hour before booking start
3. **BOOKING_START** - Sent at booking start time
4. **BOOKING_END** - Sent 5 minutes before booking end
5. **BOOKING_CANCEL** - Can be sent when booking is cancelled

## Configuration

The scheduler configuration in `NotificationScheduler`:
- `batch_size` - Number of notifications to process per batch (default: 50)
- `check_interval` - Seconds between checks (default: 60)

These can be adjusted in `app/notification/scheduler.py`

## Telegram Integration

Currently, the Telegram sending is a mock implementation. To integrate with real Telegram API:

1. Update `send_telegram_message()` method in `NotificationScheduler`
2. Use aiogram bot instance
3. Handle rate limiting and error retries

Example:
```python
async def send_telegram_message(self, user_id: int, message: str):
    """Send message to Telegram."""
    try:
        await bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        raise Exception(f"Telegram API Error: {str(e)}")
```

## Error Handling

The system includes comprehensive error handling:
- Failed notifications are marked with error message
- Automatic rollback on exceptions
- Logging of all operations
- Retry mechanism via scheduler loop

## Future Enhancements

- [ ] Email notifications support
- [ ] SMS notifications support
- [ ] Multiple notification channels per user
- [ ] Custom notification templates
- [ ] Notification preferences per user
- [ ] Notification delivery analytics
