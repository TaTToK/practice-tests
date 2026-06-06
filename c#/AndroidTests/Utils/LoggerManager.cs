using OpenQA.Selenium.Appium.Android;
using Serilog;

namespace AndroidTests.Utils;

public class LoggerManager
{
    public static void Configure()
    {
        Log.Logger = new LoggerConfiguration()
            .WriteTo.Console()
            .WriteTo.File(
                "logs/tests.txt",
                rollingInterval: RollingInterval.Day)
            .CreateLogger();
    }
}