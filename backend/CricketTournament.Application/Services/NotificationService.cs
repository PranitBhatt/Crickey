using CricketTournament.Application.Interfaces;
using CricketTournament.Domain.Interfaces;
using FCM.Net;
using Microsoft.Extensions.Configuration;

namespace CricketTournament.Application.Services;

public class NotificationService : INotificationService
{
    private readonly IFirestoreRepository _firestoreRepository;
    private readonly IConfiguration _configuration;
    private readonly Server _fcmServer;

    public NotificationService(IFirestoreRepository firestoreRepository, IConfiguration configuration)
    {
        _firestoreRepository = firestoreRepository;
        _configuration = configuration;
        var serverKey = _configuration["FCM:ServerKey"];
        _fcmServer = new Server(serverKey ?? string.Empty);
    }

    public async Task SendNotificationAsync(string token, string title, string body, Dictionary<string, string>? data = null)
    {
        try
        {
            var message = new Message
            {
                To = token,
                Notification = new FCM.Net.Notification
                {
                    Title = title,
                    Body = body
                },
                Data = data ?? new Dictionary<string, string>()
            };

            await _fcmServer.SendAsync(message);
        }
        catch (Exception ex)
        {
            // Log error but don't throw
            Console.WriteLine($"Error sending notification: {ex.Message}");
        }
    }

    public async Task SendNotificationToTeamAsync(string teamId, string title, string body, Dictionary<string, string>? data = null)
    {
        // Get team captain's FCM token from users collection
        var team = await _firestoreRepository.GetDocumentAsync<Dictionary<string, object>>("teams", teamId);
        if (team == null || !team.ContainsKey("captainUid")) return;

        var captainUid = team["captainUid"].ToString();
        if (string.IsNullOrEmpty(captainUid)) return;

        var user = await _firestoreRepository.GetDocumentAsync<Dictionary<string, object>>("users", captainUid);
        if (user == null || !user.ContainsKey("fcmToken")) return;

        var token = user["fcmToken"].ToString();
        if (!string.IsNullOrEmpty(token))
        {
            await SendNotificationAsync(token, title, body, data);
        }
    }
}

