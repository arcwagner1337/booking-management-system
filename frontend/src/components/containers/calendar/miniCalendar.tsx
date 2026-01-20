import { useBookingContext } from '../bookingContext/bookingContext.tsx'

export const renderMiniCalendar = () => {

    const { setSelectedDate, calendarDays, selectedDate, } = useBookingContext();

    return(
    <div style={{ marginBottom: '32px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h2 style={{ fontSize: '16px', fontWeight: '600' }}>Календарь</h2>
            <span style={{ color: '#3b82f6', fontWeight: '500' }}>{selectedDate}</span>
        </div>

        {/* Дни недели */}
        <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(7, 1fr)',
            gap: '8px',
            marginBottom: '16px',
            textAlign: 'center'
        }}>
            {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map(day => (
                <div key={day} style={{ color: '#6b7280', fontSize: '14px' }}>{day}</div>
            ))}
        </div>

        {/* Числа */}
        <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(7, 1fr)',
            gap: '8px',
            textAlign: 'center'
        }}>
            {calendarDays.map((day, index) => (

                
                <div
                    key={index}
                    style={{
                        padding: '8px',
                        borderRadius: '8px',
                        backgroundColor: day === '15' ? '#3b82f6' : 'transparent',
                        color: day === '15' ? '#ffffff' : day ? '#9ca3af' : 'transparent',
                        fontWeight: day === '15' ? '600' : '400',
                        cursor: day ? 'pointer' : 'default'
                    }}
                    onClick={() => day && setSelectedDate(`${day} янв`)}
                >
                    {day}
                </div>
            ))}
        </div>
    </div>
    )
};