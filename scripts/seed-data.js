/**
 * Seeding script to generate initial tournament data
 * Run with: node scripts/seed-data.js
 * 
 * Make sure to set up Firebase Admin credentials first
 */

const admin = require('firebase-admin');
const path = require('path');

// Initialize Firebase Admin
const serviceAccount = require('../path-to-service-account-key.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

// Team names for seeding
const teamNames = [
  'Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore',
  'Kolkata Knight Riders', 'Delhi Capitals', 'Punjab Kings',
  'Rajasthan Royals', 'Sunrisers Hyderabad', 'Gujarat Titans',
  'Lucknow Super Giants', 'Gujarat Lions', 'Rising Pune Supergiant'
];

const playerRoles = ['Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper'];

// Generate random player
function generatePlayer(index) {
  const roles = ['Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper'];
  return {
    name: `Player ${index + 1}`,
    role: roles[Math.floor(Math.random() * roles.length)]
  };
}

// Generate 11 players for a team
function generatePlayers() {
  const players = [];
  for (let i = 0; i < 11; i++) {
    players.push(generatePlayer(i));
  }
  return players;
}

async function seedData() {
  try {
    console.log('Starting data seeding...');

    // 1. Create Tournament
    const tournamentData = {
      name: 'Cricket Premier League 2024',
      startDate: admin.firestore.Timestamp.fromDate(new Date('2024-06-01')),
      endDate: admin.firestore.Timestamp.fromDate(new Date('2024-07-31')),
      location: 'Mumbai, India',
      oversGroup: 20,
      oversKnockout: 20,
      groups: ['A', 'B'],
      status: 'upcoming',
      createdBy: 'organizer-uid' // Replace with actual organizer UID
    };

    const tournamentRef = await db.collection('tournaments').add(tournamentData);
    const tournamentId = tournamentRef.id;
    console.log(`Created tournament: ${tournamentId}`);

    // 2. Create 12 Teams (6 in Group A, 6 in Group B)
    const teams = [];
    for (let i = 0; i < 12; i++) {
      const group = i < 6 ? 'A' : 'B';
      const teamData = {
        tournamentId: tournamentId,
        name: teamNames[i],
        group: group,
        captainName: `Captain ${i + 1}`,
        captainUid: `captain-uid-${i + 1}`, // Replace with actual captain UIDs
        logoUrl: '',
        players: generatePlayers(),
        substitute: {
          name: 'Substitute Player',
          role: 'All-rounder'
        }
      };

      const teamRef = await db.collection('teams').add(teamData);
      teams.push({ id: teamRef.id, ...teamData });
      console.log(`Created team: ${teamData.name} (${teamRef.id})`);
    }

    // 3. Generate 21 Matches
    // Group A: 6 teams = 15 matches (round-robin)
    // Group B: 6 teams = 15 matches (round-robin)
    // Total: 30 matches, but we'll create 21 as specified
    
    let matchNumber = 1;
    const groupATeams = teams.filter(t => t.group === 'A');
    const groupBTeams = teams.filter(t => t.group === 'B');

    // Group A matches
    for (let i = 0; i < groupATeams.length; i++) {
      for (let j = i + 1; j < groupATeams.length; j++) {
        if (matchNumber > 21) break;
        
        const matchData = {
          tournamentId: tournamentId,
          group: 'A',
          matchNumber: matchNumber++,
          team1Id: groupATeams[i].id,
          team2Id: groupATeams[j].id,
          dateTime: admin.firestore.Timestamp.fromDate(
            new Date(2024, 5, matchNumber, 10 + (matchNumber % 12), 0)
          ),
          venue: 'Stadium ' + (matchNumber % 5 + 1),
          overs: 20,
          status: 'scheduled',
          winnerTeamId: null,
          scores: {}
        };

        await db.collection('matches').add(matchData);
        console.log(`Created match ${matchData.matchNumber}: ${groupATeams[i].name} vs ${groupATeams[j].name}`);
      }
      if (matchNumber > 21) break;
    }

    // Group B matches (if we haven't reached 21)
    if (matchNumber <= 21) {
      for (let i = 0; i < groupBTeams.length; i++) {
        for (let j = i + 1; j < groupBTeams.length; j++) {
          if (matchNumber > 21) break;
          
          const matchData = {
            tournamentId: tournamentId,
            group: 'B',
            matchNumber: matchNumber++,
            team1Id: groupBTeams[i].id,
            team2Id: groupBTeams[j].id,
            dateTime: admin.firestore.Timestamp.fromDate(
              new Date(2024, 5, matchNumber, 10 + (matchNumber % 12), 0)
            ),
            venue: 'Stadium ' + (matchNumber % 5 + 1),
            overs: 20,
            status: 'scheduled',
            winnerTeamId: null,
            scores: {}
          };

          await db.collection('matches').add(matchData);
          console.log(`Created match ${matchData.matchNumber}: ${groupBTeams[i].name} vs ${groupBTeams[j].name}`);
        }
        if (matchNumber > 21) break;
      }
    }

    // 4. Initialize Points Table
    for (const group of ['A', 'B']) {
      const groupTeams = teams.filter(t => t.group === group);
      const entries = groupTeams.map(team => ({
        teamId: team.id,
        teamName: team.name,
        group: group,
        played: 0,
        won: 0,
        lost: 0,
        tied: 0,
        points: 0,
        netRunRate: 0.0,
        runsFor: 0,
        runsAgainst: 0,
        oversFor: 0.0,
        oversAgainst: 0.0
      }));

      const pointsTableData = {
        tournamentId: tournamentId,
        group: group,
        entries: entries,
        lastUpdated: admin.firestore.Timestamp.now()
      };

      await db.collection('pointsTable').doc(`${tournamentId}_${group}`).set(pointsTableData);
      console.log(`Created points table for Group ${group}`);
    }

    console.log('Data seeding completed successfully!');
    process.exit(0);
  } catch (error) {
    console.error('Error seeding data:', error);
    process.exit(1);
  }
}

seedData();

