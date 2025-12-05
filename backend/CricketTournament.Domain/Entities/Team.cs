namespace CricketTournament.Domain.Entities;

public class Player
{
    public string Name { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
}

public class Team
{
    public string Id { get; set; } = string.Empty;
    public string TournamentId { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string Group { get; set; } = string.Empty;
    public string CaptainName { get; set; } = string.Empty;
    public string CaptainUid { get; set; } = string.Empty;
    public string LogoUrl { get; set; } = string.Empty;
    public List<Player> Players { get; set; } = new();
    public Player? Substitute { get; set; }
}

