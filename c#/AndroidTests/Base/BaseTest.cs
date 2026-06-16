using AndroidTests.Drivers;
using AndroidTests.Utils;
using OpenQA.Selenium.Appium.Android;
using Serilog;

namespace AndroidTests.Base;

public class BaseTest
{
    #pragma warning disable NUnit1032
    protected AndroidDriver? Driver;
    #pragma warning restore NUnit1032

    public void GlobalSetup()
    {
        LoggerManager.Configure();
        Log.Information("Starting test run");
        EmulatorManager.Start();
        EmulatorManager.ClearAppData();
        Driver = DriverFactory.CreateDriver();
    }

    [TearDown]
    public void TearDown()
    {
    }

    [OneTimeTearDown]
    public void OneTimeTearDown()
    {
        Log.Information("Test run finished");
        Driver?.Quit();
        Driver?.Dispose();
        Driver = null;
    }
}