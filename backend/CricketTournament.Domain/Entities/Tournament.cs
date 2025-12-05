namespace CricketTournament.Domain.Entities;

public class Tournament
{
    public string Id { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public DateTime StartDate { get; set; }
    public DateTime EndDate { get; set; }
    public string Location { get; set; } = string.Empty;
    public int OversGroup { get; set; }
    public int OversKnockout { get; set; }
    public List<string> Groups { get; set; } = new();
    public string Status { get; set; } = "upcoming";
    public string CreatedBy { get; set; } = string.Empty;
}

