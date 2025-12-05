using AutoMapper;
using CricketTournament.Application.DTOs;
using CricketTournament.Application.Interfaces;
using CricketTournament.Domain.Interfaces;

namespace CricketTournament.Application.Services;

public class TournamentService : ITournamentService
{
    private readonly ITournamentRepository _repository;
    private readonly IMapper _mapper;

    public TournamentService(ITournamentRepository repository, IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<string> CreateTournamentAsync(TournamentDTO tournament)
    {
        var entity = _mapper.Map<Domain.Entities.Tournament>(tournament);
        return await _repository.CreateAsync(entity);
    }

    public async Task<TournamentDTO?> GetTournamentAsync(string id)
    {
        var entity = await _repository.GetByIdAsync(id);
        return entity == null ? null : _mapper.Map<TournamentDTO>(entity);
    }

    public async Task<List<TournamentDTO>> GetAllTournamentsAsync()
    {
        var entities = await _repository.GetAllAsync();
        return _mapper.Map<List<TournamentDTO>>(entities);
    }

    public async Task UpdateTournamentAsync(string id, TournamentDTO tournament)
    {
        var entity = _mapper.Map<Domain.Entities.Tournament>(tournament);
        entity.Id = id;
        await _repository.UpdateAsync(entity);
    }

    public async Task DeleteTournamentAsync(string id)
    {
        await _repository.DeleteAsync(id);
    }
}

