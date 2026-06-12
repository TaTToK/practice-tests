namespace AndroidTests.Models.Appium;

public class AppiumSettings
{
    public required string ServerUrl { get; set; }
    public required string DeviceName { get; set; }
    public required string PlatformName { get; set; }
    public required string AutomationName { get; set; }
    public required string AppPackage { get; set; }
    public required string AppActivity { get; set; }
}