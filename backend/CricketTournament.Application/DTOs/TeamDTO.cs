namespace CricketTournament.Application.DTOs;

public class PlayerDTO
{
    public string Name { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
}

public class TeamDTO
{
    public string? Id { get; set; }
    public string TournamentId { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string Group { get; set; } = string.Empty;
    public string CaptainName { get; set; } = string.Empty;
    public string CaptainUid { get; set; } = string.Empty;
    public string LogoUrl { get; set; } = string.Empty;
    public List<PlayerDTO> Players { get; set; } = new();
    public PlayerDTO? Substitute { get; set; }
}

