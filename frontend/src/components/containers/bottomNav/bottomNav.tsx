
// import { activeTab, setActiveTab } from '../../../App.tsx'
import { useBookingContext } from '../bookingContext/bookingContext.tsx'

export const BottomNav = () => {
    const {activeTab, setActiveTab} = useBookingContext();
    return (
        <div className="fixed bottom-0 left-0 right-0 flex justify-around p-3 border-t border-base-300 bg-base-200">
            {(['Ресурсы', 'Календарь', 'Профиль'] as const).map((tab) => (
                <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    style={{
                        backgroundColor: 'transparent',
                        border: 'none',
                        color: activeTab === tab ? '#3b82f6' : '#6b7280',
                        fontSize: '14px',
                        fontWeight: activeTab === tab ? '600' : '400',
                        cursor: 'pointer',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        gap: '4px'
                    }}
                >
                    <div>{tab === 'Ресурсы' ? '📱' : tab === 'Календарь' ? '📅' : '👤'}</div>
                    <span>{tab}</span>
                </button>
            ))}
        </div>
    );
};
