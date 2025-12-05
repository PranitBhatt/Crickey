using CricketTournament.Application.DTOs;
using CricketTournament.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace CricketTournament.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TeamsController : ControllerBase
{
    private readonly ITeamService _service;

    public TeamsController(ITeamService service)
    {
        _service = service;
    }

    [HttpPost]
    public async Task<ActionResult<object>> CreateTeam([FromBody] TeamDTO team)
    {
        var id = await _service.CreateTeamAsync(team);
        return Ok(new { id });
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<TeamDTO>> GetTeam(string id)
    {
        var team = await _service.GetTeamAsync(id);
        if (team == null) return NotFound();
        return Ok(team);
    }

    [HttpGet("tournament/{tournamentId}")]
    public async Task<ActionResult<List<TeamDTO>>> GetTeamsByTournament(string tournamentId)
    {
        var teams = await _service.GetTeamsByTournamentAsync(tournamentId);
        return Ok(teams);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateTeam(string id, [FromBody] TeamDTO team)
    {
        await _service.UpdateTeamAsync(id, team);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteTeam(string id)
    {
        await _service.DeleteTeamAsync(id);
        return NoContent();
    }
}

