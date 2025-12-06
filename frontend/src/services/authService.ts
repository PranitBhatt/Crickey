import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User,
  updateProfile,
} from 'firebase/auth';
import { auth, db } from './firebase';
import { doc, getDoc, setDoc, updateDoc } from 'firebase/firestore';
import { apiFetchJSON } from '../utils/api';

export interface UserProfile {
  uid: string;
  name: string;
  email: string;
  role: 'organizer' | 'captain';
  teamId: string | null;
  phone: string;
}

// Sign in with email and password
export const signIn = async (email: string, password: string): Promise<User> => {
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  return userCredential.user;
};

// Sign up with email and password
export const signUp = async (
  email: string,
  password: string,
  name: string,
  role: 'organizer' | 'captain',
  phone: string
): Promise<User> => {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  
  await updateProfile(userCredential.user, { displayName: name });
  
  // Create user profile in Firestore
  const userProfile: UserProfile = {
    uid: userCredential.user.uid,
    name,
    email,
    role,
    teamId: null,
    phone,
  };
  
  await setDoc(doc(db, 'users', userCredential.user.uid), userProfile);
  
  return userCredential.user;
};

// Sign out
export const signOutUser = async (): Promise<void> => {
  await signOut(auth);
};

// Get current user
export const getCurrentUser = (): User | null => {
  return auth.currentUser;
};

// Get user profile from Firestore
export const getUserProfile = async (uid: string): Promise<UserProfile | null> => {
  const docRef = doc(db, 'users', uid);
  const docSnap = await getDoc(docRef);
  if (docSnap.exists()) {
    return docSnap.data() as UserProfile;
  }
  return null;
};

// Update user profile
export const updateUserProfile = async (uid: string, updates: Partial<UserProfile>): Promise<void> => {
  const docRef = doc(db, 'users', uid);
  await updateDoc(docRef, updates);
};

// Validate Firebase token with backend
export const validateToken = async (idToken: string): Promise<boolean> => {
  try {
    const response = await apiFetchJSON<{ valid: boolean }>('/auth/validateToken', {
      method: 'POST',
      body: JSON.stringify({ token: idToken }),
      skipAuth: true, // This endpoint validates the token itself
    });
    return response.valid === true;
  } catch (error) {
    return false;
  }
};

// Auth state observer
export const onAuthStateChange = (callback: (user: User | null) => void) => {
  return onAuthStateChanged(auth, callback);
};

