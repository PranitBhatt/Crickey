namespace CricketTournament.Application.Interfaces;

public interface INotificationService
{
    Task SendNotificationAsync(string token, string title, string body, Dictionary<string, string>? data = null);
    Task SendNotificationToTeamAsync(string teamId, string title, string body, Dictionary<string, string>? data = null);
}

