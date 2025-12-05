import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getMessaging, getToken, onMessage } from "firebase/messaging";

// Firebase configuration using VITE_ env variables (required by Vite + Vercel)
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};


console.log("FIREBASE CONFIG:", firebaseConfig);
// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Services
export const auth = getAuth(app); 
export const db = getFirestore(app);

// Messaging (only if running in a browser)
let messaging: ReturnType<typeof getMessaging> | null = null;

if (typeof window !== "undefined" && "Notification" in window) {
  try {
    messaging = getMessaging(app);
  } catch (err) {
    console.warn("Firebase messaging is not supported:", err);
  }
}

// Request notification permission
export const requestNotificationPermission = async (): Promise<string | null> => {
  if (!messaging) return null;

  try {
    const permission = await Notification.requestPermission();
    if (permission !== "granted") return null;

    const token = await getToken(messaging, {
      vapidKey: import.meta.env.VITE_FIREBASE_VAPID_KEY,
    });

    return token;
  } catch (error) {
    console.error("Error getting notification token:", error);
    return null;
  }
};

// Foreground message listener
export const onMessageListener = () =>
  new Promise((resolve) => {
    if (!messaging) resolve(null);
    else onMessage(messaging, (payload) => resolve(payload));
  });

export default app;
