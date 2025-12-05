using AutoMapper;
using CricketTournament.Application.DTOs;
using CricketTournament.Application.Interfaces;
using CricketTournament.Domain.Interfaces;

namespace CricketTournament.Application.Services;

public class MatchService : IMatchService
{
    private readonly IMatchRepository _repository;
    private readonly IMapper _mapper;

    public MatchService(IMatchRepository repository, IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<string> CreateMatchAsync(MatchDTO match)
    {
        var entity = _mapper.Map<Domain.Entities.Match>(match);
        return await _repository.CreateAsync(entity);
    }

    public async Task<MatchDTO?> GetMatchAsync(string id)
    {
        var entity = await _repository.GetByIdAsync(id);
        return entity == null ? null : _mapper.Map<MatchDTO>(entity);
    }

    public async Task<List<MatchDTO>> GetMatchesByTournamentAsync(string tournamentId)
    {
        var entities = await _repository.GetByTournamentIdAsync(tournamentId);
        return _mapper.Map<List<MatchDTO>>(entities);
    }

    public async Task UpdateMatchAsync(string id, MatchDTO match)
    {
        var entity = _mapper.Map<Domain.Entities.Match>(match);
        entity.Id = id;
        await _repository.UpdateAsync(entity);
    }

    public async Task DeleteMatchAsync(string id)
    {
        await _repository.DeleteAsync(id);
    }

    public async Task UpdateMatchScoreAsync(string matchId, ScoreUpdateDTO score)
    {
        await _repository.UpdateScoreAsync(matchId, score.TeamId, score.Runs, score.Wickets, score.Overs);
    }

    public async Task AddBallByBallAsync(string matchId, BallByBallDTO ball)
    {
        var entity = _mapper.Map<Domain.Entities.BallByBall>(ball);
        await _repository.AddBallByBallAsync(matchId, entity);
    }
}

