using CricketTournament.Application.DTOs;
using CricketTournament.Application.Interfaces;
using CricketTournament.Domain.Interfaces;
using System.Linq;

namespace CricketTournament.Application.Services;

public class PointsTableService : IPointsTableService
{
    private readonly IPointsTableRepository _pointsTableRepository;
    private readonly IMatchRepository _matchRepository;
    private readonly ITeamRepository _teamRepository;

    public PointsTableService(
        IPointsTableRepository pointsTableRepository,
        IMatchRepository matchRepository,
        ITeamRepository teamRepository)
    {
        _pointsTableRepository = pointsTableRepository;
        _matchRepository = matchRepository;
        _teamRepository = teamRepository;
    }

    public async Task UpdatePointsTableAsync(string tournamentId)
    {
        var teams = await _teamRepository.GetByTournamentIdAsync(tournamentId);
        var matches = await _matchRepository.GetByTournamentIdAsync(tournamentId);
        var completedMatches = matches.Where(m => m.Status == "completed").ToList();

        var groups = teams.Select(t => t.Group).Distinct();

        foreach (var group in groups)
        {
            var groupTeams = teams.Where(t => t.Group == group).ToList();
            var groupMatches = completedMatches.Where(m => m.Group == group).ToList();

            var entries = new List<PointsTableEntryDTO>();

            foreach (var team in groupTeams)
            {
                var teamMatches = groupMatches.Where(m => m.Team1Id == team.Id || m.Team2Id == team.Id).ToList();
                var played = teamMatches.Count;
                var won = teamMatches.Count(m => m.WinnerTeamId == team.Id);
                var lost = teamMatches.Count(m => m.WinnerTeamId != null && m.WinnerTeamId != team.Id);
                var tied = teamMatches.Count(m => m.WinnerTeamId == null);

                var runsFor = 0;
                var runsAgainst = 0;
                var oversFor = 0.0;
                var oversAgainst = 0.0;

                foreach (var match in teamMatches)
                {
                    if (match.Scores == null) continue;

                    var isTeam1 = match.Team1Id == team.Id;
                    var teamScore = isTeam1 ? match.Scores.GetValueOrDefault(match.Team1Id) : match.Scores.GetValueOrDefault(match.Team2Id);
                    var opponentScore = isTeam1 ? match.Scores.GetValueOrDefault(match.Team2Id) : match.Scores.GetValueOrDefault(match.Team1Id);

                    if (teamScore != null)
                    {
                        runsFor += teamScore.Runs;
                        oversFor += teamScore.Overs;
                    }

                    if (opponentScore != null)
                    {
                        runsAgainst += opponentScore.Runs;
                        oversAgainst += opponentScore.Overs;
                    }
                }

                var netRunRate = CalculateNetRunRate(runsFor, runsAgainst, oversFor, oversAgainst);
                var points = (won * 2) + tied;

                entries.Add(new PointsTableEntryDTO
                {
                    TeamId = team.Id,
                    TeamName = team.Name,
                    Group = group,
                    Played = played,
                    Won = won,
                    Lost = lost,
                    Tied = tied,
                    Points = points,
                    NetRunRate = netRunRate,
                    RunsFor = runsFor,
                    RunsAgainst = runsAgainst,
                    OversFor = oversFor,
                    OversAgainst = oversAgainst
                });
            }

            var pointsTable = new PointsTableDTO
            {
                TournamentId = tournamentId,
                Group = group,
                Entries = entries,
                LastUpdated = DateTime.UtcNow
            };

            await _pointsTableRepository.UpsertAsync(tournamentId, group, pointsTable);
        }
    }

    public async Task<PointsTableDTO?> GetPointsTableAsync(string tournamentId, string group)
    {
        return await _pointsTableRepository.GetAsync(tournamentId, group);
    }

    public async Task<List<PointsTableDTO>> GetAllPointsTablesAsync(string tournamentId)
    {
        return await _pointsTableRepository.GetAllAsync(tournamentId);
    }

    private static double CalculateNetRunRate(int runsFor, int runsAgainst, double oversFor, double oversAgainst)
    {
        if (oversFor == 0 && oversAgainst == 0) return 0;
        if (oversFor == 0) return -999.0;
        if (oversAgainst == 0) return 999.0;

        var runRateFor = runsFor / oversFor;
        var runRateAgainst = runsAgainst / oversAgainst;
        return runRateFor - runRateAgainst;
    }
}

