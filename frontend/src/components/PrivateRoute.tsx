import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useEffect } from 'react';

interface PrivateRouteProps {
  children: React.ReactNode;
  requiredRole?: 'organizer' | 'captain';
}

export const PrivateRoute = ({ children, requiredRole }: PrivateRouteProps) => {
  const { user, profile, loading, loadProfile } = useAuthStore();

  useEffect(() => {
    if (user && !profile) {
      loadProfile(user.uid);
    }
  }, [user, profile, loadProfile]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && profile?.role !== requiredRole) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <>{children}</>;
};

