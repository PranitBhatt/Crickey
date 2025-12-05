namespace CricketTournament.Domain.Entities;

public class MatchScore
{
    public int Runs { get; set; }
    public int Wickets { get; set; }
    public double Overs { get; set; }
}

public class Match
{
    public string Id { get; set; } = string.Empty;
    public string TournamentId { get; set; } = string.Empty;
    public string Group { get; set; } = string.Empty;
    public int MatchNumber { get; set; }
    public string Team1Id { get; set; } = string.Empty;
    public string Team2Id { get; set; } = string.Empty;
    public DateTime DateTime { get; set; }
    public string Venue { get; set; } = string.Empty;
    public int Overs { get; set; }
    public string Status { get; set; } = "scheduled";
    public string? WinnerTeamId { get; set; }
    public Dictionary<string, MatchScore>? Scores { get; set; }
}

public class BallByBall
{
    public int BallNumber { get; set; }
    public int OverNumber { get; set; }
    public string Batsman { get; set; } = string.Empty;
    public string Bowler { get; set; } = string.Empty;
    public int Runs { get; set; }
    public bool IsWicket { get; set; }
    public int Extras { get; set; }
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
}

