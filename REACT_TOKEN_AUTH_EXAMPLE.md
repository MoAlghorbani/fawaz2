# React Token Authentication Example

## Updated React Code for Token-Based Authentication

```javascript
import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'http://127.0.0.1:8000';

function App() {
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  const [user, setUser] = useState(null);
  const [loginStatus, setLoginStatus] = useState('');
  const [equipment, setEquipment] = useState([]);

  // Login function with token handling
  const handleLogin = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: 'admin',
          password: 'admin123'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const authToken = data.token;
        
        // Store token in localStorage
        localStorage.setItem('authToken', authToken);
        setToken(authToken);
        setUser(data.user);
        setLoginStatus('Login successful!');
        
        console.log('Login response:', data);
        console.log('Token:', authToken);
        
        // Fetch equipment data after login
        await fetchEquipment(authToken);
      } else {
        const errorData = await response.json();
        setLoginStatus('Login failed: ' + errorData.error);
        console.log('Error details:', errorData);
      }
    } catch (error) {
      setLoginStatus('Login error: ' + error);
      console.error('Login error:', error);
    }
  };

  // Logout function
  const handleLogout = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/logout/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
        },
      });

      if (response.ok) {
        // Clear token from storage and state
        localStorage.removeItem('authToken');
        setToken(null);
        setUser(null);
        setEquipment([]);
        setLoginStatus('Logged out successfully');
      }
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // Fetch equipment with token authentication
  const fetchEquipment = async (authToken = token) => {
    if (!authToken) {
      console.log('No token available');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/equipment/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${authToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setEquipment(data.results || []);
        console.log('Equipment data:', data);
      } else {
        console.error('Failed to fetch equipment:', response.status);
        if (response.status === 401) {
          // Token might be invalid, clear it
          localStorage.removeItem('authToken');
          setToken(null);
          setUser(null);
        }
      }
    } catch (error) {
      console.error('Equipment fetch error:', error);
    }
  };

  // Create new equipment
  const createEquipment = async () => {
    if (!token) return;

    try {
      const response = await fetch(`${API_BASE_URL}/api/equipment/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          serial_number: 'EQ-' + Date.now(),
          equipment_type: 'Excavator',
          model: 'CAT 320',
          status: 'active'
        }),
      });

      if (response.ok) {
        const newEquipment = await response.json();
        console.log('Created equipment:', newEquipment);
        // Refresh equipment list
        await fetchEquipment();
      } else {
        console.error('Failed to create equipment:', response.status);
      }
    } catch (error) {
      console.error('Create equipment error:', error);
    }
  };

  // Check token validity on app load
  useEffect(() => {
    const checkTokenValidity = async () => {
      if (token) {
        try {
          const response = await fetch(`${API_BASE_URL}/api/auth/user/`, {
            headers: {
              'Authorization': `Token ${token}`,
            },
          });

          if (response.ok) {
            const userData = await response.json();
            setUser(userData.user);
            await fetchEquipment();
          } else {
            // Token is invalid
            localStorage.removeItem('authToken');
            setToken(null);
          }
        } catch (error) {
          console.error('Token validation error:', error);
          localStorage.removeItem('authToken');
          setToken(null);
        }
      }
    };

    checkTokenValidity();
  }, [token]);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>🔧 Equipment Inspection System</h1>
      
      {!token ? (
        <div>
          <h2>Login Required</h2>
          <button 
            onClick={handleLogin}
            style={{
              padding: '10px 20px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            Login
          </button>
          <p style={{ marginTop: '10px', color: 'red' }}>{loginStatus}</p>
        </div>
      ) : (
        <div>
          <div style={{ marginBottom: '20px' }}>
            <h2>Welcome, {user?.username}!</h2>
            <p>Token: {token.substring(0, 20)}...</p>
            <button 
              onClick={handleLogout}
              style={{
                padding: '8px 16px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '3px',
                cursor: 'pointer'
              }}
            >
              Logout
            </button>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <h3>Equipment Management</h3>
            <button 
              onClick={createEquipment}
              style={{
                padding: '8px 16px',
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '3px',
                cursor: 'pointer',
                marginRight: '10px'
              }}
            >
              Add Equipment
            </button>
            <button 
              onClick={() => fetchEquipment()}
              style={{
                padding: '8px 16px',
                backgroundColor: '#17a2b8',
                color: 'white',
                border: 'none',
                borderRadius: '3px',
                cursor: 'pointer'
              }}
            >
              Refresh List
            </button>
          </div>

          <div>
            <h4>Equipment List ({equipment.length} items)</h4>
            {equipment.length > 0 ? (
              <ul style={{ listStyle: 'none', padding: 0 }}>
                {equipment.map((item) => (
                  <li 
                    key={item.equipment_id}
                    style={{
                      padding: '10px',
                      margin: '5px 0',
                      backgroundColor: '#f8f9fa',
                      border: '1px solid #dee2e6',
                      borderRadius: '5px'
                    }}
                  >
                    <strong>{item.equipment_type}</strong> - {item.serial_number}
                    <br />
                    <small>Model: {item.model} | Status: {item.status}</small>
                  </li>
                ))}
              </ul>
            ) : (
              <p style={{ color: '#666' }}>No equipment found. Try adding some!</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
```

## Key Features of Token Authentication

### 1. **Automatic Token Storage**
- Tokens are stored in `localStorage` for persistence
- Automatically included in all API requests

### 2. **Token Validation**
- Checks token validity on app load
- Handles invalid/expired tokens gracefully

### 3. **Secure API Requests**
- All API calls include `Authorization: Token your-token-here` header
- Proper error handling for authentication failures

### 4. **Session Management**
- Login stores token and user data
- Logout clears token and resets state
- Token validation ensures user stays logged in

### 5. **Error Handling**
- 401 responses automatically clear invalid tokens
- User-friendly error messages
- Graceful degradation when not authenticated

## Testing Steps

1. **Start the Django server**: `python manage.py runserver`
2. **Run your React app**: `npm start`
3. **Click Login** - Should receive and store token
4. **Try API operations** - Equipment list, create, etc.
5. **Click Logout** - Should clear token and deny further access

## Security Notes

- Tokens don't expire by default (you can configure expiration)
- Tokens are deleted on logout for better security
- Use HTTPS in production
- Consider implementing token refresh for long-running applications