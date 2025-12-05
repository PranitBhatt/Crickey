// This component is handled by react-hot-toast
// Just export a helper function for consistency
import toast from 'react-hot-toast';

export const showToast = {
  success: (message: string) => toast.success(message),
  error: (message: string) => toast.error(message),
  info: (message: string) => toast(message),
  loading: (message: string) => toast.loading(message),
};

export { Toaster } from 'react-hot-toast';

