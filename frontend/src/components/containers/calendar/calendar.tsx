// import { selectedDate, setSelectedDate, setSelectedResource, setActiveTab } from '../../../App.tsx'
import { useBookingContext } from "../bookingContext/bookingContext.tsx";
import Button from "../../small/button/button.tsx";

export const Calendar = () => {
  const {
    selectedDate,
    setSelectedDate,
    setSelectedResource,
    setActiveTab,
    calendarDays,
    bookings,
  } = useBookingContext();

  const getSelectedDayNumber = () => {
    const match = selectedDate.match(/\d+/);
    return match ? match[0] : null;
  };

  const selectedDayNumber = getSelectedDayNumber();
  // console.log(bookings);
  return (
    <div style={{ padding: "16px" }}>
      {/* Заголовок */}
      <div style={{ marginBottom: "24px" }}>
        <h1
          style={{ fontSize: "28px", fontWeight: "700", marginBottom: "8px" }}
        >
          Календарь
        </h1>
        <p style={{ color: "#6b7280", fontSize: "14px" }}>
          Расписание бронирований
        </p>
      </div>
      {/* Текущий месяц */}
      <div
        style={{
          backgroundColor: "#1f2937",
          borderRadius: "16px",
          padding: "20px",
          marginBottom: "24px",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "20px",
          }}
        >
          <Button
            variant="primary"
            size="lg"
            width="responsive"
            shape="text"
            onClick={() => { }}
            label="←"
          />
          <h2 style={{ fontSize: "18px", fontWeight: "600" }}>Январь 2024</h2>
          <Button
            variant="primary"
            size="lg"
            width="responsive"
            shape="text"
            onClick={() => { }}
            label="→"
          />
        </div>
        {/* Дни недели */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(7, 1fr)",
            gap: "8px",
            marginBottom: "16px",
            textAlign: "center",
          }}
        >
          {["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"].map((day) => (
            <div key={day} style={{ color: "#6b7280", fontSize: "14px" }}>
              {day}
            </div>
          ))}
        </div>
        {/* Числа месяца с бронированиями */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(7, 1fr)",
            gap: "8px",
            textAlign: "center",
          }}
        >
          {calendarDays.map((day, index) => {
            const dayString = day ? `${day} янв` : "";
            const hasBooking =
              dayString &&
              bookings.some((booking) => booking.date === dayString);
            if (!day) return null;
            const isSelected = day === selectedDayNumber;
            return (
              <Button
                key={index}
                disabled={isSelected}
                label={day}
                size="md"
                onClick={() => { if (day) { setSelectedDate(`${day} янв`); } }}
                className={`relative ${hasBooking ? "btn-active" : ""}`}
              >
                {hasBooking && (
                  <div
                    style={{
                      position: "absolute",
                      bottom: "4px",
                      left: "50%",
                      transform: "translateX(-50%)",
                      width: "4px",
                      height: "4px",
                      backgroundColor: "#000000",
                      borderRadius: "50%",
                    }}
                  ></div>
                )}
              </Button>
            );
          })}
        </div>
      </div>
      {/* Предстоящие бронирования на выбранную дату */}
      <div>
        <h2 style={{ fontSize: "16px", fontWeight: "600", marginBottom: "16px" }}>
          Бронирования на {selectedDate}
        </h2>
        {bookings
          .filter(
            (booking, index: number) => booking.date === selectedDate || (selectedDate === booking.date && bookings[index].active)
          )
          .map((booking) => (
            <div
              key={booking.id}
              style={{
                backgroundColor: "#1f2937",
                borderRadius: "16px",
                padding: "20px",
                marginBottom: "16px",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start",
                  marginBottom: "12px",
                }}
              >
                <div>
                  <h3
                    style={{
                      fontSize: "18px",
                      fontWeight: "600",
                      marginBottom: "4px",
                    }}
                  >
                    {booking.title}
                  </h3>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "8px",
                      marginBottom: "8px",
                    }}
                  >
                    <span
                      style={{
                        backgroundColor: "#374151",
                        color: "#9ca3af",
                        padding: "2px 8px",
                        borderRadius: "12px",
                        fontSize: "12px",
                        fontWeight: "500",
                      }}
                    >
                      {booking.type}
                    </span>
                    <span style={{ color: "#9ca3af", fontSize: "14px" }}>
                      •
                    </span>
                    <span style={{ color: "#9ca3af", fontSize: "14px" }}>
                      {booking.capacity}
                    </span>
                  </div>
                  {booking.time && (
                    <div
                      style={{
                        color: "#3b82f6",
                        fontSize: "14px",
                        fontWeight: "500",
                      }}
                    >
                      ⏰ {booking.time}
                    </div>
                  )}
                </div>
                <div style={{ textAlign: "right" }}>
                  <div
                    style={{
                      fontSize: "20px",
                      fontWeight: "700",
                      marginBottom: "8px",
                    }}
                  >
                    {booking.price.toLocaleString("ru-RU")} ₽
                  </div>
                  <Button
                    label={"Подробнее"}
                    onClick={() => {
                      setSelectedResource(booking);
                      setActiveTab("Ресурсы");
                    }}
                    variant="info"
                    size="md"
                  ></Button>
                </div>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
};
