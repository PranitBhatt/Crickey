using CricketTournament.Application.DTOs;
using CricketTournament.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace CricketTournament.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class MatchesController : ControllerBase
{
    private readonly IMatchService _service;

    public MatchesController(IMatchService service)
    {
        _service = service;
    }

    [HttpPost]
    public async Task<ActionResult<object>> CreateMatch([FromBody] MatchDTO match)
    {
        var id = await _service.CreateMatchAsync(match);
        return Ok(new { id });
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<MatchDTO>> GetMatch(string id)
    {
        var match = await _service.GetMatchAsync(id);
        if (match == null) return NotFound();
        return Ok(match);
    }

    [HttpGet("tournament/{tournamentId}")]
    public async Task<ActionResult<List<MatchDTO>>> GetMatchesByTournament(string tournamentId)
    {
        var matches = await _service.GetMatchesByTournamentAsync(tournamentId);
        return Ok(matches);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateMatch(string id, [FromBody] MatchDTO match)
    {
        await _service.UpdateMatchAsync(id, match);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteMatch(string id)
    {
        await _service.DeleteMatchAsync(id);
        return NoContent();
    }

    [HttpPost("{id}/score")]
    public async Task<IActionResult> UpdateScore(string id, [FromBody] ScoreUpdateDTO score)
    {
        await _service.UpdateMatchScoreAsync(id, score);
        return NoContent();
    }

    [HttpPost("{id}/ball")]
    public async Task<IActionResult> AddBallByBall(string id, [FromBody] BallByBallDTO ball)
    {
        await _service.AddBallByBallAsync(id, ball);
        return NoContent();
    }
}

