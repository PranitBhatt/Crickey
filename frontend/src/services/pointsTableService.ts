import { pointsService, type PointsTable } from './pointsService';

// Re-export PointsTableEntry for backward compatibility (PointsTable is already imported above)
export type { PointsTableEntry } from './pointsService';

// Get points table for a tournament group
export const getPointsTable = async (
  tournamentId: number,
  group: string
): Promise<PointsTable | null> => {
  try {
    return await pointsService.get(tournamentId, group);
  } catch (error) {
    console.error('Error fetching points table:', error);
    return null;
  }
};

// Get all points tables for a tournament
export const getAllPointsTables = async (tournamentId: number): Promise<PointsTable[]> => {
  try {
    return await pointsService.getAll(tournamentId);
  } catch (error) {
    console.error('Error fetching points tables:', error);
    return [];
  }
};

// Update points table (triggers recalculation)
export const updatePointsTable = async (tournamentId: number, group: string): Promise<void> => {
  await pointsService.calculate(tournamentId, group);
};

