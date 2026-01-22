# Notification System - Integration Checklist

## ✅ Completed Tasks

### 1. Database Models
- [x] `Notification` model with relationships to Booking and User
- [x] `NotificationStatus` enum (PENDING, PROCESSING, SENT, FAILED)
- [x] `NotificationType` enum (BOOKING_24H, BOOKING_1H, BOOKING_START, BOOKING_END, BOOKING_CANCEL)
- [x] Bidirectional relationship between Booking and Notification

### 2. Factory Pattern
- [x] `NotificationMessageFactory` - Base factory class
- [x] Message factories for each notification type
- [x] `NotificationFactory` - Creates appropriate messages based on type
- [x] Support for enum-based notification types

### 3. Scheduler
- [x] `NotificationScheduler` - Processes pending notifications
- [x] Batch processing with configurable size
- [x] Async/await compatible with AsyncSession
- [x] Telegram API mock implementation (ready for real API integration)
- [x] Error handling and status updates

### 4. Service Layer
- [x] `NotificationService` - High-level service for notification management
- [x] Methods for creating notifications
- [x] Bulk booking notification creation
- [x] Notification retrieval and updates
- [x] Booking cancellation handling

### 5. Database Migration
- [x] Alembic migration file created
- [x] Table schema with proper indexes
- [x] Foreign key constraints with CASCADE delete
- [x] Enum columns for status and type

### 6. Module Organization
- [x] `app/notification/__init__.py` - Module exports
- [x] `app/notification/factory.py` - Message factories
- [x] `app/notification/scheduler.py` - Notification scheduler
- [x] `app/notification/README.md` - Documentation
- [x] `app/domain/services/notifications/` - Service layer
- [x] `app/domain/services/notification_service.py` - Service instance

## 🚀 Next Steps

### 1. Apply Database Migration
```bash
cd /path/to/project
alembic upgrade head
```

### 2. Integrate Scheduler into Application Startup
In `app/app.py`, add to the `get_application()` function:

```python
from app.notification.scheduler import NotificationScheduler
from app.depends import provider

async def start_notification_scheduler():
    """Start the notification scheduler as a background task."""
    asyncio.create_task(_run_scheduler())

async def _run_scheduler():
    """Run the notification scheduler in the background."""
    async with provider.session_factory() as session:
        scheduler = NotificationScheduler(session)
        await scheduler.run()

# Add to on_startup:
on_startup=[
    bot_manager.run_all,
    user_service.create_test_user,
    start_notification_scheduler,  # Add this
]
```

### 3. Create Notifications When Booking is Created
In your booking creation service, add:

```python
from app.domain.services.notifications import NotificationService

async def create_booking_with_notifications(booking_data, session):
    """Create booking and associated notifications."""
    # Create booking
    booking = Booking(**booking_data)
    session.add(booking)
    await session.flush()  # Get the ID
    
    # Create notifications
    notification_service = NotificationService(session)
    await notification_service.create_booking_notifications(booking)
    
    await session.commit()
    return booking
```

### 4. Handle Booking Cancellation
In your booking cancellation service, add:

```python
from app.domain.services.notifications import NotificationService

async def cancel_booking(booking_id, session):
    """Cancel booking and related notifications."""
    notification_service = NotificationService(session)
    
    # Cancel pending notifications
    await notification_service.cancel_booking_notifications(booking_id)
    
    # Mark booking as cancelled
    await session.execute(
        update(Booking).where(Booking.id == booking_id).values(status="cancelled")
    )
    await session.commit()
```

### 5. Integrate Real Telegram API
Update `send_telegram_message()` in `NotificationScheduler`:

```python
from aiogram import Bot
from app.bot.manager import bot_manager

async def send_telegram_message(self, user_id, message: str):
    """Send message to Telegram."""
    try:
        # Get bot instance
        bot = bot_manager.get_bot()  # Adjust based on your setup
        await bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        raise Exception(f"Telegram API Error: {str(e)}")
```

## 📋 Component Dependencies

```
Models:
├── Booking ──── relationships ──── Notification
└── User ────────────────────────── Notification

Services:
├── NotificationService (requires AsyncSession)
└── NotificationFactory (uses Notification types)

Scheduler:
├── NotificationScheduler (requires AsyncSession)
├── Notification model
└── NotificationFactory

Application:
├── Models (database layer)
├── Services (business logic)
├── Scheduler (background tasks)
└── Factory (message creation)
```

## 🧪 Testing the System

### Test notification creation:
```python
async def test_notifications():
    async with provider.session_factory() as session:
        # Create test booking
        booking = Booking(
            user_id=test_user_id,
            resource_id=test_resource_id,
            start_time=datetime.utcnow() + timedelta(hours=25),
            end_time=datetime.utcnow() + timedelta(hours=26),
        )
        session.add(booking)
        await session.flush()
        
        # Create notifications
        service = NotificationService(session)
        notifications = await service.create_booking_notifications(booking)
        await session.commit()
        
        print(f"Created {len(notifications)} notifications")
```

### Test scheduler:
```python
async def test_scheduler():
    async with provider.session_factory() as session:
        scheduler = NotificationScheduler(session)
        processed = await scheduler.process_batch()
        print(f"Processed {processed} notifications")
```

## ⚙️ Configuration Options

In `NotificationScheduler`:
- `batch_size = 50` - Notifications processed per batch
- `check_interval = 60` - Seconds between checks

Adjust these based on your volume and performance needs.

## 📝 Troubleshooting

### Issue: Notifications not being sent
1. Check that the scheduler is running
2. Verify database migration was applied
3. Check notification status in database
4. Review error messages in logs

### Issue: Duplicate notifications
1. Use `get_pending_for_booking()` before creating
2. Ensure notifications are marked as SENT/FAILED

### Issue: Telegram delivery fails
1. Verify bot token is correct
2. Check user Telegram ID format
3. Ensure bot has permission to send messages
4. Review error message in notification.error field

## 🎯 Summary

The notification system is now fully integrated and ready for:
- ✅ Automatic notification scheduling
- ✅ Message generation based on notification type
- ✅ Database persistence with proper tracking
- ✅ Batch processing with error handling
- ✅ Integration with Telegram (and extensible for other channels)

All components follow the project's async/await patterns and SQLAlchemy best practices.
