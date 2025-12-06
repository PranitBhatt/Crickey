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
import { apiFetchJSON } from '../utils/api';

export interface MatchScore {
  runs: number;
  wickets: number;
  overs: number;
}

export interface BallByBall {
  ballNumber: number;
  overNumber: number;
  batsman: string;
  bowler: string;
  runs: number;
  isWicket: boolean;
  extras: number;
  timestamp: Date;
}

export interface Match {
  id: string;
  tournamentId: string;
  group: string;
  matchNumber: number;
  team1Id: string;
  team2Id: string;
  dateTime: Date;
  venue: string;
  overs: number;
  status: 'scheduled' | 'live' | 'completed';
  winnerTeamId: string | null;
  scores: {
    [teamId: string]: MatchScore;
  };
}

export interface MatchDTO {
  tournamentId: string;
  group: string;
  matchNumber: number;
  team1Id: string;
  team2Id: string;
  dateTime: string;
  venue: string;
  overs: number;
  status: 'scheduled' | 'live' | 'completed';
}

export interface ScoreUpdateDTO {
  teamId: string;
  runs: number;
  wickets: number;
  overs: number;
}

export interface BallByBallDTO {
  ballNumber: number;
  overNumber: number;
  batsman: string;
  bowler: string;
  runs: number;
  isWicket: boolean;
  extras: number;
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

// Convert Match from Firestore
const convertMatch = (doc: any): Match => ({
  id: doc.id,
  tournamentId: doc.tournamentId,
  group: doc.group,
  matchNumber: doc.matchNumber,
  team1Id: doc.team1Id,
  team2Id: doc.team2Id,
  dateTime: convertTimestamp(doc.dateTime),
  venue: doc.venue,
  overs: doc.overs,
  status: doc.status,
  winnerTeamId: doc.winnerTeamId || null,
  scores: doc.scores || {},
});

// Convert BallByBall from Firestore
const convertBallByBall = (doc: any): BallByBall => ({
  ballNumber: doc.ballNumber,
  overNumber: doc.overNumber,
  batsman: doc.batsman,
  bowler: doc.bowler,
  runs: doc.runs,
  isWicket: doc.isWicket,
  extras: doc.extras,
  timestamp: convertTimestamp(doc.timestamp),
});

// Get all matches for a tournament
export const getMatches = async (tournamentId: string): Promise<Match[]> => {
  const q = query(
    collection(db, 'matches'),
    where('tournamentId', '==', tournamentId),
    orderBy('matchNumber')
  );
  const snapshot = await getDocs(q);
  return snapshot.docs.map((doc) => convertMatch({ id: doc.id, ...doc.data() }));
};

// Get match by ID
export const getMatch = async (id: string): Promise<Match | null> => {
  const docRef = doc(db, 'matches', id);
  const docSnap = await getDoc(docRef);
  if (docSnap.exists()) {
    return convertMatch({ id: docSnap.id, ...docSnap.data() });
  }
  return null;
};

// Get live matches
export const getLiveMatches = async (tournamentId: string): Promise<Match[]> => {
  const q = query(
    collection(db, 'matches'),
    where('tournamentId', '==', tournamentId),
    where('status', '==', 'live'),
    orderBy('matchNumber')
  );
  const snapshot = await getDocs(q);
  return snapshot.docs.map((doc) => convertMatch({ id: doc.id, ...doc.data() }));
};

// Get matches by team
export const getMatchesByTeam = async (teamId: string): Promise<Match[]> => {
  const q = query(
    collection(db, 'matches'),
    where('team1Id', '==', teamId)
  );
  const snapshot1 = await getDocs(q);
  
  const q2 = query(
    collection(db, 'matches'),
    where('team2Id', '==', teamId)
  );
  const snapshot2 = await getDocs(q2);
  
  const allMatches = [
    ...snapshot1.docs.map((doc) => convertMatch({ id: doc.id, ...doc.data() })),
    ...snapshot2.docs.map((doc) => convertMatch({ id: doc.id, ...doc.data() })),
  ];
  
  return allMatches.sort((a, b) => a.matchNumber - b.matchNumber);
};

// Create match
export const createMatch = async (match: MatchDTO): Promise<string> => {
  const response = await apiFetchJSON<{ id: string }>('/matches', {
    method: 'POST',
    body: JSON.stringify(match),
  });
  return response.id;
};

// Update match
export const updateMatch = async (id: string, match: Partial<MatchDTO>): Promise<void> => {
  await apiFetchJSON(`/matches/${id}`, {
    method: 'PUT',
    body: JSON.stringify(match),
  });
};

// Update match score
export const updateMatchScore = async (matchId: string, score: ScoreUpdateDTO): Promise<void> => {
  await apiFetchJSON(`/matches/${matchId}/score`, {
    method: 'POST',
    body: JSON.stringify(score),
  });
};

// Add ball-by-ball entry
export const addBallByBall = async (matchId: string, ball: BallByBallDTO): Promise<void> => {
  await apiFetchJSON(`/matches/${matchId}/ball`, {
    method: 'POST',
    body: JSON.stringify(ball),
  });
};

// Get ball-by-ball data for a match
export const getBallByBall = async (matchId: string): Promise<BallByBall[]> => {
  const ballByBallRef = collection(db, 'matches', matchId, 'ballByBall');
  const q = query(ballByBallRef, orderBy('overNumber'), orderBy('ballNumber'));
  const snapshot = await getDocs(q);
  return snapshot.docs.map((doc) => convertBallByBall(doc.data()));
};

// Subscribe to matches (real-time)
export const subscribeToMatches = (
  tournamentId: string,
  callback: (matches: Match[]) => void
): Unsubscribe => {
  const q = query(
    collection(db, 'matches'),
    where('tournamentId', '==', tournamentId),
    orderBy('matchNumber')
  );
  return onSnapshot(q, (snapshot) => {
    const matches = snapshot.docs.map((doc) =>
      convertMatch({ id: doc.id, ...doc.data() })
    );
    callback(matches);
  });
};

// Subscribe to live matches (real-time)
export const subscribeToLiveMatches = (
  tournamentId: string,
  callback: (matches: Match[]) => void
): Unsubscribe => {
  const q = query(
    collection(db, 'matches'),
    where('tournamentId', '==', tournamentId),
    where('status', '==', 'live'),
    orderBy('matchNumber')
  );
  return onSnapshot(q, (snapshot) => {
    const matches = snapshot.docs.map((doc) =>
      convertMatch({ id: doc.id, ...doc.data() })
    );
    callback(matches);
  });
};

// Subscribe to single match (real-time)
export const subscribeToMatch = (
  matchId: string,
  callback: (match: Match | null) => void
): Unsubscribe => {
  const docRef = doc(db, 'matches', matchId);
  return onSnapshot(docRef, (docSnap) => {
    if (docSnap.exists()) {
      callback(convertMatch({ id: docSnap.id, ...docSnap.data() }));
    } else {
      callback(null);
    }
  });
};

// Subscribe to ball-by-ball (real-time)
export const subscribeToBallByBall = (
  matchId: string,
  callback: (balls: BallByBall[]) => void
): Unsubscribe => {
  const ballByBallRef = collection(db, 'matches', matchId, 'ballByBall');
  const q = query(ballByBallRef, orderBy('overNumber'), orderBy('ballNumber'));
  return onSnapshot(q, (snapshot) => {
    const balls = snapshot.docs.map((doc) => convertBallByBall(doc.data()));
    callback(balls);
  });
};

