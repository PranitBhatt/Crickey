import {
  collection,
  doc,
  getDoc,
  getDocs,
  query,
  where,
  orderBy,
  onSnapshot,
  Unsubscribe,
} from 'firebase/firestore';
import { db } from './firebase';
import { fetchWithAuthJSON } from './apiClient';

export interface PointsTableEntry {
  teamId: string;
  teamName: string;
  group: string;
  played: number;
  won: number;
  lost: number;
  tied: number;
  points: number;
  netRunRate: number;
  runsFor: number;
  runsAgainst: number;
  oversFor: number;
  oversAgainst: number;
}

export interface PointsTable {
  tournamentId: string;
  group: string;
  entries: PointsTableEntry[];
  lastUpdated: Date;
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

// Convert PointsTable from Firestore
const convertPointsTable = (doc: any): PointsTable => ({
  tournamentId: doc.tournamentId,
  group: doc.group,
  entries: doc.entries || [],
  lastUpdated: convertTimestamp(doc.lastUpdated),
});

// Get points table for a tournament group
export const getPointsTable = async (
  tournamentId: string,
  group: string
): Promise<PointsTable | null> => {
  const q = query(
    collection(db, 'pointsTable'),
    where('tournamentId', '==', tournamentId),
    where('group', '==', group)
  );
  const snapshot = await getDocs(q);
  if (snapshot.empty) return null;
  return convertPointsTable({ id: snapshot.docs[0].id, ...snapshot.docs[0].data() });
};

// Get all points tables for a tournament
export const getAllPointsTables = async (tournamentId: string): Promise<PointsTable[]> => {
  const q = query(
    collection(db, 'pointsTable'),
    where('tournamentId', '==', tournamentId),
    orderBy('group')
  );
  const snapshot = await getDocs(q);
  return snapshot.docs.map((doc) =>
    convertPointsTable({ id: doc.id, ...doc.data() })
  );
};

// Update points table (triggers recalculation)
export const updatePointsTable = async (tournamentId: string): Promise<void> => {
  await fetchWithAuthJSON('/pointsTable/update', {
    method: 'POST',
    body: JSON.stringify({ tournamentId }),
  });
};

// Subscribe to points table (real-time)
export const subscribeToPointsTable = (
  tournamentId: string,
  group: string,
  callback: (pointsTable: PointsTable | null) => void
): Unsubscribe => {
  const q = query(
    collection(db, 'pointsTable'),
    where('tournamentId', '==', tournamentId),
    where('group', '==', group)
  );
  return onSnapshot(q, (snapshot) => {
    if (snapshot.empty) {
      callback(null);
    } else {
      callback(convertPointsTable({ id: snapshot.docs[0].id, ...snapshot.docs[0].data() }));
    }
  });
};

