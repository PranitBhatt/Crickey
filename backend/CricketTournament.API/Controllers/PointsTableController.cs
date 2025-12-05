using CricketTournament.Application.DTOs;
using CricketTournament.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace CricketTournament.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PointsTableController : ControllerBase
{
    private readonly IPointsTableService _service;

    public PointsTableController(IPointsTableService service)
    {
        _service = service;
    }

    [HttpPost("update")]
    public async Task<IActionResult> UpdatePointsTable([FromBody] UpdatePointsTableRequest request)
    {
        await _service.UpdatePointsTableAsync(request.TournamentId);
        return NoContent();
    }

    [HttpGet("{tournamentId}/{group}")]
    public async Task<ActionResult<PointsTableDTO>> GetPointsTable(string tournamentId, string group)
    {
        var pointsTable = await _service.GetPointsTableAsync(tournamentId, group);
        if (pointsTable == null) return NotFound();
        return Ok(pointsTable);
    }

    [HttpGet("{tournamentId}")]
    public async Task<ActionResult<List<PointsTableDTO>>> GetAllPointsTables(string tournamentId)
    {
        var pointsTables = await _service.GetAllPointsTablesAsync(tournamentId);
        return Ok(pointsTables);
    }
}

public class UpdatePointsTableRequest
{
    public string TournamentId { get; set; } = string.Empty;
}

