using AndroidTests.Base;
using AndroidTests.Config;
using AndroidTests.Models.Login;
using Microsoft.Extensions.Configuration;
using OpenQA.Selenium;
using OpenQA.Selenium.Appium.Android;
using Serilog;

namespace AndroidTests.Pages;

public class LoginPage : BasePage
{
    private readonly AndroidDriver _driver;
    
    public LoginPage(AndroidDriver driver) : base(driver)
    {
        _driver = driver;
    }

    public bool WaitForPageToLoad()
    {
        Log.Information("Waiting for login page to load");
        
        return IsDisplayed(By.XPath("//android.widget.EditText[@resource-id=\"phone\"]"));
    }
    
    public void EnterPhoneNumber(string phoneNumber)
    {
        Log.Information("Entering phone number");
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"phone\"]"), phoneNumber);
        
        Log.Information("Entering phone is successfully");
    }

    public void EnterPassword(string password)
    {
        Log.Information("Entering password");
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"password\"]"), password);
        
        Log.Information("Entering password is successfully");
    }

    public void ClickLoginButton()
    {
        Log.Information("Clicking login button");
        
        Click(By.XPath("//android.widget.Button[@text=\"Войти\"]"));
        
        Log.Information("Click is successfully");
    }

    public void Login(string phone, string password)
    {
        WaitForPageToLoad();
        EnterPhoneNumber(phone);
        EnterPassword(password);
        ClickLoginButton();
    }
}