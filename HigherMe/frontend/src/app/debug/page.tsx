'use client';

import { useState } from 'react';
import { ApiClient } from '@/lib/api';

export default function DebugPage() {
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testRegistration = async () => {
    setLoading(true);
    setResult('');
    
    try {
      const username = `testuser${Date.now()}`;
      const email = `test${Date.now()}@example.com`;
      const password = 'password123';
      
      console.log('Attempting registration with:', { username, email, password });
      
      const response = await ApiClient.register(username, email, password);
      
      console.log('Registration response:', response);
      setResult(JSON.stringify(response, null, 2));
    } catch (error: any) {
      console.error('Registration error:', error);
      setResult(`Error: ${error.message}\nStatus: ${error.status || 'Unknown'}`);
    } finally {
      setLoading(false);
    }
  };

  const testDirectFetch = async () => {
    setLoading(true);
    setResult('');
    
    try {
      const username = `directtest${Date.now()}`;
      const email = `direct${Date.now()}@example.com`;
      const password = 'password123';
      
      console.log('Testing direct fetch...');
      
      const response = await fetch('http://localhost:8000/api/v1/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });
      
      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`HTTP ${response.status}: ${errorData.detail || 'Unknown error'}`);
      }
      
      const data = await response.json();
      console.log('Response data:', data);
      setResult(JSON.stringify(data, null, 2));
    } catch (error: any) {
      console.error('Direct fetch error:', error);
      setResult(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold">API Debug Page</h1>
        
        <div className="space-y-4">
          <button
            onClick={testRegistration}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded disabled:opacity-50"
          >
            {loading ? 'Testing...' : 'Test ApiClient Registration'}
          </button>
          
          <button
            onClick={testDirectFetch}
            disabled={loading}
            className="bg-green-600 hover:bg-green-700 px-6 py-2 rounded disabled:opacity-50 ml-4"
          >
            {loading ? 'Testing...' : 'Test Direct Fetch'}
          </button>
        </div>
        
        <div className="bg-gray-800 p-4 rounded">
          <h2 className="text-xl font-semibold mb-2">Result:</h2>
          <pre className="whitespace-pre-wrap text-sm">{result}</pre>
        </div>
        
        <div className="bg-gray-800 p-4 rounded">
          <h2 className="text-xl font-semibold mb-2">Instructions:</h2>
          <p>Open browser developer tools (F12) and check the Console and Network tabs for detailed information.</p>
        </div>
      </div>
    </div>
  );
}
