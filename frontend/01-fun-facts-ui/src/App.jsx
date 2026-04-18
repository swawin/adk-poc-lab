import { Navigate, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import FunFactsPage from './pages/FunFactsPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/fun-facts" element={<FunFactsPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
