using CricketTournament.Application.DTOs;
using CricketTournament.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace CricketTournament.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TournamentsController : ControllerBase
{
    private readonly ITournamentService _service;

    public TournamentsController(ITournamentService service)
    {
        _service = service;
    }

    [HttpPost]
    public async Task<ActionResult<object>> CreateTournament([FromBody] TournamentDTO tournament)
    {
        var id = await _service.CreateTournamentAsync(tournament);
        return Ok(new { id });
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<TournamentDTO>> GetTournament(string id)
    {
        var tournament = await _service.GetTournamentAsync(id);
        if (tournament == null) return NotFound();
        return Ok(tournament);
    }

    [HttpGet]
    public async Task<ActionResult<List<TournamentDTO>>> GetAllTournaments()
    {
        var tournaments = await _service.GetAllTournamentsAsync();
        return Ok(tournaments);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateTournament(string id, [FromBody] TournamentDTO tournament)
    {
        await _service.UpdateTournamentAsync(id, tournament);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteTournament(string id)
    {
        await _service.DeleteTournamentAsync(id);
        return NoContent();
    }
}

