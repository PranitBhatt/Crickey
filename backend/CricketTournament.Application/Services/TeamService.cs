using AutoMapper;
using CricketTournament.Application.DTOs;
using CricketTournament.Application.Interfaces;
using CricketTournament.Domain.Interfaces;

namespace CricketTournament.Application.Services;

public class TeamService : ITeamService
{
    private readonly ITeamRepository _repository;
    private readonly IMapper _mapper;

    public TeamService(ITeamRepository repository, IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<string> CreateTeamAsync(TeamDTO team)
    {
        var entity = _mapper.Map<Domain.Entities.Team>(team);
        return await _repository.CreateAsync(entity);
    }

    public async Task<TeamDTO?> GetTeamAsync(string id)
    {
        var entity = await _repository.GetByIdAsync(id);
        return entity == null ? null : _mapper.Map<TeamDTO>(entity);
    }

    public async Task<List<TeamDTO>> GetTeamsByTournamentAsync(string tournamentId)
    {
        var entities = await _repository.GetByTournamentIdAsync(tournamentId);
        return _mapper.Map<List<TeamDTO>>(entities);
    }

    public async Task UpdateTeamAsync(string id, TeamDTO team)
    {
        var entity = _mapper.Map<Domain.Entities.Team>(team);
        entity.Id = id;
        await _repository.UpdateAsync(entity);
    }

    public async Task DeleteTeamAsync(string id)
    {
        await _repository.DeleteAsync(id);
    }
}

