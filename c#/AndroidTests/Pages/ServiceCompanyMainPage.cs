using AndroidTests.Base;
using OpenQA.Selenium;
using OpenQA.Selenium.Appium.Android;
using Serilog;

namespace AndroidTests.Pages;

public class ServiceCompanyMainPage : BasePage
{
    private readonly AndroidDriver _driver;

    public ServiceCompanyMainPage(AndroidDriver driver) : base(driver)
    {
        _driver = driver;
    }

    public bool WaitForPageToLoad()
    {
        Log.Information("Waiting for main page to load");

        return IsDisplayed(By.XPath("//android.view.View[@content-desc=\"Внешние клиенты\"]"));
    }
    
    public void ClickToAllowNotifications()
    {
        Log.Information("Clicking button to allow notifications");
        
        Click(By.XPath("//android.widget.Button[@resource-id=\"com.android.permissioncontroller:id/permission_allow_button\"]"));
        
        Log.Information("Click is successfully");
    }
    
    public void ClickToExternalClient()
    {
        Log.Information("Clicking button to allow external client");
        
        Click(By.XPath("//android.view.View[@content-desc=\"Внешние клиенты\"]"));
        
        Log.Information("Click is successfully");
    }
}