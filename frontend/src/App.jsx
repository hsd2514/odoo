import { useState } from 'react';
import Login from './components/Login';
import SignUp from './components/SignUp';

function App() {
  const [currentPage, setCurrentPage] = useState('login');

  const navigateToSignUp = () => {
    setCurrentPage('signup');
  };

  const navigateToLogin = () => {
    setCurrentPage('login');
  };

  return (
    <div className="App">
      {currentPage === 'login' ? (
        <Login onNavigateToSignUp={navigateToSignUp} />
      ) : (
        <SignUp onNavigateToLogin={navigateToLogin} />
      )}
    </div>
  );
}

export default App;
