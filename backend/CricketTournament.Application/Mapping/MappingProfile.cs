using AutoMapper;
using CricketTournament.Application.DTOs;
using CricketTournament.Domain.Entities;

namespace CricketTournament.Application.Mapping;

public class MappingProfile : Profile
{
    public MappingProfile()
    {
        CreateMap<Tournament, TournamentDTO>().ReverseMap();
        CreateMap<Team, TeamDTO>().ReverseMap();
        CreateMap<Player, PlayerDTO>().ReverseMap();
        CreateMap<Match, MatchDTO>().ReverseMap();
        CreateMap<MatchScore, MatchScoreDTO>().ReverseMap();
        CreateMap<BallByBall, BallByBallDTO>().ReverseMap();
    }
}

