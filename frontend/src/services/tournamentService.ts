import {
  collection,
  doc,
  getDoc,
  getDocs,
  addDoc,
  updateDoc,
  deleteDoc,
  query,
  where,
  orderBy,
  Timestamp,
  onSnapshot,
  Unsubscribe,
} from 'firebase/firestore';
import { db } from './firebase';
import { apiFetchJSON } from '../utils/api';

export interface Tournament {
  id: string;
  name: string;
  startDate: Date;
  endDate: Date;
  location: string;
  oversGroup: number;
  oversKnockout: number;
  groups: string[];
  status: 'upcoming' | 'ongoing' | 'completed';
  createdBy: string;
}

export interface TournamentDTO {
  name: string;
  startDate: string;
  endDate: string;
  location: string;
  oversGroup: number;
  oversKnockout: number;
  groups: string[];
  status: 'upcoming' | 'ongoing' | 'completed';
  createdBy: string;
}

// Convert Firestore timestamp to Date
const convertTimestamp = (timestamp: any): Date => {
  if (timestamp?.toDate) {
    return timestamp.toDate();
  }
  if (timestamp instanceof Date) {
    return timestamp;
  }
  return new Date(timestamp);
};

// Convert Tournament from Firestore
const convertTournament = (doc: any): Tournament => ({
  id: doc.id,
  name: doc.name,
  startDate: convertTimestamp(doc.startDate),
  endDate: convertTimestamp(doc.endDate),
  location: doc.location,
  oversGroup: doc.oversGroup,
  oversKnockout: doc.oversKnockout,
  groups: doc.groups || [],
  status: doc.status,
  createdBy: doc.createdBy,
});

// Get all tournaments
export const getTournaments = async (): Promise<Tournament[]> => {
  const q = query(collection(db, 'tournaments'), orderBy('startDate', 'desc'));
  const snapshot = await getDocs(q);
  return snapshot.docs.map((doc) => convertTournament({ id: doc.id, ...doc.data() }));
};

// Get tournament by ID
export const getTournament = async (id: string): Promise<Tournament | null> => {
  const docRef = doc(db, 'tournaments', id);
  const docSnap = await getDoc(docRef);
  if (docSnap.exists()) {
    return convertTournament({ id: docSnap.id, ...docSnap.data() });
  }
  return null;
};

// Create tournament
export const createTournament = async (tournament: TournamentDTO): Promise<string> => {
  const response = await apiFetchJSON<{ id: string }>('/tournaments', {
    method: 'POST',
    body: JSON.stringify(tournament),
  });
  return response.id;
};

// Update tournament
export const updateTournament = async (id: string, tournament: Partial<TournamentDTO>): Promise<void> => {
  await apiFetchJSON(`/tournaments/${id}`, {
    method: 'PUT',
    body: JSON.stringify(tournament),
  });
};

// Delete tournament
export const deleteTournament = async (id: string): Promise<void> => {
  await apiFetchJSON(`/tournaments/${id}`, {
    method: 'DELETE',
  });
};

// Subscribe to tournaments (real-time)
export const subscribeToTournaments = (
  callback: (tournaments: Tournament[]) => void
): Unsubscribe => {
  const q = query(collection(db, 'tournaments'), orderBy('startDate', 'desc'));
  return onSnapshot(q, (snapshot) => {
    const tournaments = snapshot.docs.map((doc) =>
      convertTournament({ id: doc.id, ...doc.data() })
    );
    callback(tournaments);
  });
};

// Subscribe to single tournament (real-time)
export const subscribeToTournament = (
  id: string,
  callback: (tournament: Tournament | null) => void
): Unsubscribe => {
  const docRef = doc(db, 'tournaments', id);
  return onSnapshot(docRef, (docSnap) => {
    if (docSnap.exists()) {
      callback(convertTournament({ id: docSnap.id, ...docSnap.data() }));
    } else {
      callback(null);
    }
  });
};

