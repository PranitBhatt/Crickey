/**
 * API client with Firebase authentication token injection.
 * All backend API calls should use apiFetch() instead of direct fetch/axios.
 * 
 * This is the central API wrapper that automatically attaches Firebase ID tokens
 * to all requests for authenticated endpoints.
 */
import { auth } from '../services/firebase';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

export interface FetchOptions extends RequestInit {
  skipAuth?: boolean; // Set to true for public endpoints that don't require auth
}

/**
 * Fetch with automatic Firebase ID token injection.
 * Automatically includes Authorization header with Bearer token for authenticated requests.
 * 
 * @param url - API endpoint URL (can be relative or absolute)
 * @param options - Fetch options (same as standard fetch, plus skipAuth flag)
 * @returns Promise<Response>
 * 
 * @example
 * const response = await apiFetch('/api/tournaments', {
 *   method: 'POST',
 *   body: JSON.stringify(data),
 * });
 */
export const apiFetch = async (
  url: string,
  options: FetchOptions = {}
): Promise<Response> => {
  const { skipAuth = false, headers = {}, ...restOptions } = options;

  // Get Firebase ID token if auth is required
  let authToken: string | null = null;
  if (!skipAuth) {
    const currentUser = auth.currentUser;
    if (currentUser) {
      try {
        authToken = await currentUser.getIdToken();
      } catch (error) {
        console.error('Error getting ID token:', error);
        // Continue without token - backend will return 401
      }
    }
  }

  // Build full URL if relative
  const fullUrl = url.startsWith('http') ? url : `${API_BASE_URL}${url.startsWith('/') ? '' : '/'}${url}`;

  // Prepare headers
  const requestHeaders: HeadersInit = {
    'Content-Type': 'application/json',
    ...headers,
  };

  // Add Authorization header if token is available
  if (authToken) {
    requestHeaders['Authorization'] = `Bearer ${authToken}`;
  }

  // Make the request
  const response = await fetch(fullUrl, {
    ...restOptions,
    headers: requestHeaders,
  });

  // Handle 401 Unauthorized
  if (response.status === 401) {
    console.error('Unauthorized request - token may be invalid or expired');
    // Optionally: trigger logout or token refresh
  }

  return response;
};

/**
 * Convenience wrapper that parses JSON response and handles errors.
 * 
 * @param url - API endpoint URL
 * @param options - Fetch options
 * @returns Promise<T> - Parsed JSON response
 * 
 * @example
 * const data = await apiFetchJSON<Tournament>('/api/tournaments/123');
 */
export const apiFetchJSON = async <T = any>(
  url: string,
  options: FetchOptions = {}
): Promise<T> => {
  const response = await apiFetch(url, options);

  if (!response.ok) {
    const errorText = await response.text();
    let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
    
    try {
      const errorJson = JSON.parse(errorText);
      errorMessage = errorJson.detail || errorJson.message || errorMessage;
    } catch {
      errorMessage = errorText || errorMessage;
    }

    throw new Error(errorMessage);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return null as T;
  }

  return response.json() as Promise<T>;
};

