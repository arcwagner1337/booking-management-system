  export const renderProfileScreen = () => (
    <div style={{ padding: '16px' }}>
      {/* Заголовок */}
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '28px', fontWeight: '700', marginBottom: '8px' }}>Профиль</h1>
        <p style={{ color: '#6b7280', fontSize: '14px' }}>Личный кабинет</p>
      </div>

      {/* Настройки */}
      <div style={{ marginBottom: '32px' }}>
        <h2 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>Настройки</h2>
        <div style={{
          backgroundColor: '#1f2937',
          borderRadius: '16px',
          padding: '20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              backgroundColor: '#3b82f6',
              borderRadius: '20px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: '600'
            }}>
              A
            </div>
            <div>
              <div style={{ fontSize: '16px', fontWeight: '600', marginBottom: '4px' }}>Asta</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#10b981', fontSize: '14px' }}>
                <div style={{ width: '8px', height: '8px', backgroundColor: '#10b981', borderRadius: '50%' }}></div>
                уведомления включены
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Активные бронирования */}
      <div style={{ marginBottom: '32px' }}>
        <div style={{ display: 'flex', marginBottom: '16px' }}>
          <button
            style={{
              padding: '8px 16px',
              backgroundColor: '#3b82f6',
              border: 'none',
              color: '#ffffff',
              borderRadius: '20px',
              fontSize: '14px',
              fontWeight: '500',
              marginRight: '12px'
            }}
          >
            Активные
          </button>
          <button
            style={{
              padding: '8px 16px',
              backgroundColor: 'transparent',
              border: '1px solid #4b5563',
              color: '#9ca3af',
              borderRadius: '20px',
              fontSize: '14px',
              fontWeight: '500'
            }}
          >
            История
          </button>
        </div>

        {/* Активное бронирование */}
        <div style={{
          backgroundColor: '#1f2937',
          borderRadius: '16px',
          padding: '20px',
          marginBottom: '16px'
        }}>
          <div style={{ marginBottom: '12px' }}>
            <div style={{ fontSize: '18px', fontWeight: '600', marginBottom: '4px' }}>Loft Noir</div>
            <div style={{ color: '#9ca3af', fontSize: '14px' }}>15 янв • 19:00–23:00</div>
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              style={{
                flex: 1,
                padding: '12px',
                backgroundColor: 'transparent',
                border: '1px solid #4b5563',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '14px',
                fontWeight: '500',
                cursor: 'pointer'
              }}
            >
              Открыть
            </button>
            <button
              style={{
                flex: 1,
                padding: '12px',
                backgroundColor: '#ef4444',
                border: 'none',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '14px',
                fontWeight: '500',
                cursor: 'pointer'
              }}
            >
              Отменить
            </button>
          </div>
        </div>
      </div>

      {/* Кнопка выхода */}
      <button
        style={{
          width: '100%',
          padding: '16px',
          backgroundColor: 'transparent',
          border: '1px solid #4b5563',
          borderRadius: '12px',
          color: '#ef4444',
          fontSize: '16px',
          fontWeight: '600',
          cursor: 'pointer'
        }}
      >
        Выйти
      </button>
    </div>
  );