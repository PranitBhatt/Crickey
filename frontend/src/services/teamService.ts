import {
  collection,
  doc,
  getDoc,
  getDocs,
  query,
  where,
  orderBy,
  Timestamp,
  onSnapshot,
  Unsubscribe,
} from 'firebase/firestore';
import { db } from './firebase';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

export interface Player {
  name: string;
  role: string;
}

export interface Team {
  id: string;
  tournamentId: string;
  name: string;
  group: 'A' | 'B';
  captainName: string;
  captainUid: string;
  logoUrl: string;
  players: Player[];
  substitute: Player | null;
}

export interface TeamDTO {
  tournamentId: string;
  name: string;
  group: 'A' | 'B';
  captainName: string;
  captainUid: string;
  logoUrl: string;
  players: Player[];
  substitute: Player | null;
}

// Convert Team from Firestore
const convertTeam = (doc: any): Team => ({
  id: doc.id,
  tournamentId: doc.tournamentId,
  name: doc.name,
  group: doc.group,
  captainName: doc.captainName,
  captainUid: doc.captainUid,
  logoUrl: doc.logoUrl || '',
  players: doc.players || [],
  substitute: doc.substitute || null,
});

// Get all teams for a tournament
export const getTeams = async (tournamentId: string): Promise<Team[]> => {
  const q = query(
    collection(db, 'teams'),
    where('tournamentId', '==', tournamentId),
    orderBy('group'),
    orderBy('name')
  );
  const snapshot = await getDocs(q);
  return snapshot.docs.map((doc) => convertTeam({ id: doc.id, ...doc.data() }));
};

// Get team by ID
export const getTeam = async (id: string): Promise<Team | null> => {
  const docRef = doc(db, 'teams', id);
  const docSnap = await getDoc(docRef);
  if (docSnap.exists()) {
    return convertTeam({ id: docSnap.id, ...docSnap.data() });
  }
  return null;
};

// Get team by captain UID
export const getTeamByCaptain = async (captainUid: string): Promise<Team | null> => {
  const q = query(collection(db, 'teams'), where('captainUid', '==', captainUid));
  const snapshot = await getDocs(q);
  if (snapshot.empty) return null;
  return convertTeam({ id: snapshot.docs[0].id, ...snapshot.docs[0].data() });
};

// Create team
export const createTeam = async (team: TeamDTO): Promise<string> => {
  const response = await axios.post(`${API_BASE_URL}/teams`, team);
  return response.data.id;
};

// Update team
export const updateTeam = async (id: string, team: Partial<TeamDTO>): Promise<void> => {
  await axios.put(`${API_BASE_URL}/teams/${id}`, team);
};

// Delete team
export const deleteTeam = async (id: string): Promise<void> => {
  await axios.delete(`${API_BASE_URL}/teams/${id}`);
};

// Subscribe to teams (real-time)
export const subscribeToTeams = (
  tournamentId: string,
  callback: (teams: Team[]) => void
): Unsubscribe => {
  const q = query(
    collection(db, 'teams'),
    where('tournamentId', '==', tournamentId),
    orderBy('group'),
    orderBy('name')
  );
  return onSnapshot(q, (snapshot) => {
    const teams = snapshot.docs.map((doc) =>
      convertTeam({ id: doc.id, ...doc.data() })
    );
    callback(teams);
  });
};

