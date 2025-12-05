using CricketTournament.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace CricketTournament.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class NotificationsController : ControllerBase
{
    private readonly INotificationService _service;

    public NotificationsController(INotificationService service)
    {
        _service = service;
    }

    [HttpPost("send")]
    public async Task<IActionResult> SendNotification([FromBody] SendNotificationRequest request)
    {
        await _service.SendNotificationAsync(
            request.Token,
            request.Title,
            request.Body,
            request.Data
        );
        return NoContent();
    }

    [HttpPost("send-to-team")]
    public async Task<IActionResult> SendNotificationToTeam([FromBody] SendNotificationToTeamRequest request)
    {
        await _service.SendNotificationToTeamAsync(
            request.TeamId,
            request.Title,
            request.Body,
            request.Data
        );
        return NoContent();
    }
}

public class SendNotificationRequest
{
    public string Token { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string Body { get; set; } = string.Empty;
    public Dictionary<string, string>? Data { get; set; }
}

public class SendNotificationToTeamRequest
{
    public string TeamId { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string Body { get; set; } = string.Empty;
    public Dictionary<string, string>? Data { get; set; }
}

