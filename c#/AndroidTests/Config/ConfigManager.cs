using AndroidTests.Models;
using Microsoft.Extensions.Configuration;
using OpenQA.Selenium.Appium;

namespace AndroidTests.Config;

public static class ConfigManager
{
    public static IConfiguration Configuration { get; } = new ConfigurationBuilder()
        .SetBasePath(AppContext.BaseDirectory)
        .AddJsonFile("appsettings.json", optional: false)
        .AddJsonFile("appsettings.local.json", optional: true)
        .AddEnvironmentVariables()
        .Build();
}