import { createContext, useContext, useState, type ReactNode } from 'react';
import { type FilterType, type BookingItem, type TimeSlot } from '../../../views/main-page/main-page.tsx'


interface BookingContextType {
  activeTab: 'Ресурсы' | 'Календарь' | 'Профиль';
  setActiveTab: (tab: 'Ресурсы' | 'Календарь' | 'Профиль') => void;
  selectedFilter: FilterType;
  setSelectedFilter: (filter: FilterType) => void;
  selectedDate: string;
  setSelectedDate: (date: string) => void;
  selectedTimeSlot: string | null;
  setSelectedTimeSlot: (timeSlot: string | null) => void;

  selectedResource: BookingItem | null;
  setSelectedResource: (resource: BookingItem | null) => void;

  filters: FilterType[];
  bookings: BookingItem[];
  timeSlots: TimeSlot[];
  calendarDays: string[];

  handleResourceClick: (resource: BookingItem) => void;
  handleBackClick: () => void;
  handleConfirmBooking: () => void;

}

//  контекст
const BookingContext = createContext<BookingContextType | undefined>(undefined);

//провайдер
export const BookingProvider = ({ children }: { children: ReactNode }) => {

  const [activeTab, setActiveTab] = useState<'Ресурсы' | 'Календарь' | 'Профиль'>('Ресурсы');
  const [selectedFilter, setSelectedFilter] = useState<FilterType>('Все');
  const [selectedDate, setSelectedDate] = useState<string>("1 янв");
  const [selectedTimeSlot, setSelectedTimeSlot] = useState<string | null>(null);
  const [selectedResource, setSelectedResource] = useState<BookingItem | null>(null);
  const filters: FilterType[] = ['Все', 'Площадки', 'Работа', 'Здоровье', 'Авто', 'Жильё'];
  const bookings: BookingItem[] = [
    {
      id: '0',
      title: 'Loft Noir',
      type: 'Площадка',
      capacity: '30–50 гостей',
      location: 'Центр',
      rating: 4.8,
      timeLeft: '4ч',
      price: 2900,
      date: '15 янв',
      time: '19:10–23:10',
      active: true
    },
    {
      id: '1',
      title: 'Loft Noir',
      type: 'Площадка',
      capacity: '30–50 гостей',
      location: 'Центр',
      rating: 4.8,
      timeLeft: '4ч',
      price: 2900,
      date: '26 янв',
      time: '19:15–23:15',
      active: true
    },
    {
      id: '2',
      title: 'Cowork Pulse',
      type: 'Работа',
      capacity: 'Дневной доступ',
      location: 'Центр',
      rating: 4.7,
      timeLeft: '8ч',
      price: 1200,
      date: '30 янв',
      time: '19:27–23:47',
      active: true
    },
    {
      id: '3',
      title: 'Hall Obsidian',
      type: 'Площадка',
      capacity: '80–120 гостей',
      location: 'Набережная',
      rating: 4.9,
      timeLeft: '6ч',
      price: 5400,
      date: '8 янв',
      time: '18:00–23:00',
      active: true
    },
    {
      id: '4',
      title: 'Noir Suites',
      type: 'Жильё',
      capacity: '1 ночь',
      location: 'Набережная',
      rating: 4.9,
      timeLeft: '2ч',
      price: 5600,
      date: '9 янв',
      time: '19:05–23:05',
      active: true
    },
    {
      id: '5',
      title: 'Noir 222 Suites',
      type: 'Работа',
      capacity: '1 ночь',
      location: 'Набережная',
      rating: 4.9,
      timeLeft: '2ч',
      price: 5600,
      date: '',
      time: '19:00–23:00',
      active: true
    }
  ];

  const timeSlots: TimeSlot[] = [
    { time: '18:00', available: true },
    { time: '18:30', available: true },
    { time: '19:00', available: true },
    { time: '19:30', available: true },
    { time: '20:00', available: true },
    { time: '20:30', available: true },
    { time: '21:00', available: true }
  ];

  const calendarDays = [
    '1', '2', '3', '4', '5', '6', '7',
    '8', '9', '10', '11', '12', '13', '14',
    '15', '16', '17', '18', '19', '20', '21',
    '22', '23', '24', '25', '26', '27', '28',
    '29', '30', '31',
  ];

  const handleResourceClick = (resource: BookingItem) => {
    setSelectedResource(resource);
  };

  const handleBackClick = () => {
    setSelectedResource(null);
  };

  const handleConfirmBooking = () => {
    alert("Забронировано успешно!")
    if (selectedTimeSlot && selectedResource) {
      alert(`Бронирование подтверждено: ${selectedResource.title} на ${selectedTimeSlot}`);
      setSelectedResource(null);
      setSelectedTimeSlot(null);
    }
  };

  const value: BookingContextType = {
    activeTab, setActiveTab,
    selectedFilter, setSelectedFilter,
    selectedDate, setSelectedDate,
    selectedTimeSlot, setSelectedTimeSlot,
    selectedResource, setSelectedResource,

    filters,
    bookings,
    timeSlots,
    calendarDays,

    handleResourceClick,
    handleBackClick,
    handleConfirmBooking,
  };



  return (
    <BookingContext.Provider value={value}>
      {children}
    </BookingContext.Provider>
  );
};


// eslint-disable-next-line react-refresh/only-export-components
export const useBookingContext = () => {
  const context = useContext(BookingContext);
  if (context === undefined) {
    throw new Error('useBookingContext must be used within a BookingProvider');
  }
  return context;
};