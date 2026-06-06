using AndroidTests.Config;
using AndroidTests.Models.Appium;
using Microsoft.Extensions.Configuration;
using OpenQA.Selenium.Appium;
using OpenQA.Selenium.Appium.Android;
using Serilog;

namespace AndroidTests.Drivers;

public static class DriverFactory
{
    public static AndroidDriver CreateDriver()
    {
        var options = new AppiumOptions();
        var settings = ConfigManager.Configuration
            .GetSection(nameof(AppiumSettings))
            .Get<AppiumSettings>();
        
        options.PlatformName = settings.PlatformName;
        options.AutomationName = settings.AutomationName;
        options.DeviceName = settings.DeviceName;
        
        options.AddAdditionalAppiumOption("appPackage", settings.AppPackage);
        options.AddAdditionalAppiumOption("appActivity", settings.AppActivity);
        options.AddAdditionalAppiumOption("newCommandTimeout", 60);
        options.AddAdditionalAppiumOption("noReset", true);

        return new AndroidDriver(
            new Uri(settings.ServerUrl),
            options,
            TimeSpan.FromSeconds(180));
    }
}