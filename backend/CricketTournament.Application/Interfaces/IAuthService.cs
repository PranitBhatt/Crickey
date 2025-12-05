namespace CricketTournament.Application.Interfaces;

public interface IAuthService
{
    Task<bool> ValidateTokenAsync(string token);
}

