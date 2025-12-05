using CricketTournament.Domain.Interfaces;
using CricketTournament.Infrastructure.Repositories;
using CricketTournament.Infrastructure.Services;
using FirebaseAdmin;
using Google.Apis.Auth.OAuth2;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace CricketTournament.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
    {
        // Initialize Firebase Admin
        var projectId = configuration["Firebase:ProjectId"];
        var credentialsPath = configuration["Firebase:CredentialsPath"];

        if (!string.IsNullOrEmpty(credentialsPath) && File.Exists(credentialsPath))
        {
            var credential = GoogleCredential.FromFile(credentialsPath);
            FirebaseApp.Create(new AppOptions
            {
                Credential = credential,
                ProjectId = projectId
            });
        }
        else if (!string.IsNullOrEmpty(projectId))
        {
            // Use default credentials (for cloud deployment)
            FirebaseApp.Create(new AppOptions
            {
                ProjectId = projectId
            });
        }

        // Register repositories
        services.AddScoped<IFirestoreRepository, FirestoreRepository>();
        services.AddScoped<ITournamentRepository, TournamentRepository>();
        services.AddScoped<ITeamRepository, TeamRepository>();
        services.AddScoped<IMatchRepository, MatchRepository>();
        services.AddScoped<IPointsTableRepository, PointsTableRepository>();

        return services;
    }
}

