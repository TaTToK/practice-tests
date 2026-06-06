using AndroidTests.Drivers;
using AndroidTests.Utils;
using OpenQA.Selenium.Appium.Android;
using Serilog;

namespace AndroidTests.Base;

public class BaseTest
{
    protected AndroidDriver? Driver;

    [OneTimeSetUp]
    public void GlobalSetup()
    {
        LoggerManager.Configure();
        Log.Information("Starting test run");
        EmulatorManager.Start();
        EmulatorManager.ClearAppData();
        Driver = DriverFactory.CreateDriver();
    }

    [OneTimeTearDown]
    public void OneTimeTearDown()
    {
        Log.Information("Test run finished");
        Driver?.Quit();
        Driver?.Dispose();
    }
}