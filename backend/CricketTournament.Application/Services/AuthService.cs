using CricketTournament.Application.Interfaces;
using FirebaseAdmin;
using FirebaseAdmin.Auth;

namespace CricketTournament.Application.Services;

public class AuthService : IAuthService
{
    public async Task<bool> ValidateTokenAsync(string token)
    {
        try
        {
            var decodedToken = await FirebaseAuth.DefaultInstance.VerifyIdTokenAsync(token);
            return decodedToken != null;
        }
        catch
        {
            return false;
        }
    }
}

