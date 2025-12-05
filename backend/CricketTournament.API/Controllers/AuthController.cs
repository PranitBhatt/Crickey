using CricketTournament.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace CricketTournament.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly IAuthService _service;

    public AuthController(IAuthService service)
    {
        _service = service;
    }

    [HttpPost("validateToken")]
    public async Task<ActionResult<object>> ValidateToken([FromBody] ValidateTokenRequest request)
    {
        var isValid = await _service.ValidateTokenAsync(request.Token);
        return Ok(new { valid = isValid });
    }
}

public class ValidateTokenRequest
{
    public string Token { get; set; } = string.Empty;
}

