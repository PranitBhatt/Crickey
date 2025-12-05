namespace CricketTournament.Application.DTOs;

public class PointsTableEntryDTO
{
    public string TeamId { get; set; } = string.Empty;
    public string TeamName { get; set; } = string.Empty;
    public string Group { get; set; } = string.Empty;
    public int Played { get; set; }
    public int Won { get; set; }
    public int Lost { get; set; }
    public int Tied { get; set; }
    public int Points { get; set; }
    public double NetRunRate { get; set; }
    public int RunsFor { get; set; }
    public int RunsAgainst { get; set; }
    public double OversFor { get; set; }
    public double OversAgainst { get; set; }
}

public class PointsTableDTO
{
    public string TournamentId { get; set; } = string.Empty;
    public string Group { get; set; } = string.Empty;
    public List<PointsTableEntryDTO> Entries { get; set; } = new();
    public DateTime LastUpdated { get; set; }
}

