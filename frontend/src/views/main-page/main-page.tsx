// import reactLogo from './assets/react.svg'
// import reactLogo from '../../assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'
import {
  ResourceDetails,
  ResourcesScreen,
} from '../../components/containers/resource/resource.tsx';
import { Calendar } from '../../components/containers/calendar/calendar.tsx';
import { RenderProfileScreen } from '../../components/containers/profile/profile.tsx';
import { BottomNav } from '../../components/containers/bottomNav/bottomNav.tsx';
//import {BottomNav} from '../../components/containers/bottomNav/bottomNav.tsx'
// import {type  FilterType,  type BookingItem , type TimeSlot} from '../../App.tsx'
// import {activeTab, setSelectedResource,  selectedTimeSlot, selectedResource} from '../../App.tsx'
import { useBookingContext } from '../../components/containers/bookingContext/bookingContext.tsx';
import { motion, AnimatePresence } from 'framer-motion';

const pageVariants = {
  initial: { opacity: 0, x: 10 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -10 },
};

export interface BookingItem {
  id: string;
  title: string;
  type: 'Площадка' | 'Работа' | 'Жильё';
  capacity?: string;
  location: string;
  rating: number;
  timeLeft?: string;
  price: number;
  date?: string;
  time?: string;
  active?: boolean;
}

export interface TimeSlot {
  time: string;
  available: boolean;
}

export type FilterType =
  | 'Все'
  | 'Площадки'
  | 'Работа'
  | 'Здоровье'
  | 'Авто'
  | 'Жильё';

export function MainPage() {
  // Основной стиль приложения
  const appStyle: React.CSSProperties = {
    backgroundColor: '#0a0a0a',
    color: '#ffffff',
    minHeight: '100vh',
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  };
  const { activeTab, selectedResource } = useBookingContext();
  return (
    <div style={appStyle}>
      {/* Контент в зависимости от выбранного таба */}
      <div style={{ paddingBottom: '80px' }}>
        <AnimatePresence mode="wait">

           <motion.div
            key={selectedResource ? 'details' : activeTab} // Ключ заставляет анимацию срабатывать при смене
            initial="initial"
            animate="animate"
            exit="exit"
            variants={pageVariants}
            transition={{ duration: 0.2 }}
          >
            {selectedResource ? (
              <ResourceDetails />
            ) : activeTab === 'Ресурсы' ? (
              <ResourcesScreen />
            ) : activeTab === 'Календарь' ? (
              <Calendar />
            ) : (
              /* Вызываем как компонент, а не функцию */
              <RenderProfileScreen /> 
            )}
          </motion.div>


          {/* {selectedResource
            ? ResourceDetails()
            : activeTab === 'Ресурсы'
              ? ResourcesScreen()
              : activeTab === 'Календарь'
                ? Calendar()
                : renderProfileScreen()} */}
        </AnimatePresence>
      </div>
      {/* Нижняя навигация */}
      {!selectedResource && BottomNav()}
    </div>
  );
}
