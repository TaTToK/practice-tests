using AndroidTests.Base;
using AndroidTests.Config;
using AndroidTests.Models.Login;
using AndroidTests.Pages;
using Microsoft.Extensions.Configuration;
using OpenQA.Selenium;
using OpenQA.Selenium.Appium;
using Serilog;

namespace AndroidTests.Tests;

public class AuthorizationTest : BaseTest
{
    private LoginPage _loginPage = null!;

    [SetUp]
    public void TestSetUp()
    {
        _loginPage = new LoginPage(Driver!);
    }

    [Test, Order(1)]
    [TestCase("Owner")]
    [TestCase("Service")]
    public void LoginTest(string role)
    {
        var (phone, password) = role switch
        {
            "Owner" => (
                ConfigManager.Configuration.GetSection(nameof(OwnerEquipment)).Get<OwnerEquipment>()!.PhoneNumber,
                ConfigManager.Configuration.GetSection(nameof(OwnerEquipment)).Get<OwnerEquipment>()!.Password
            ),
            "Service" => (
                ConfigManager.Configuration.GetSection(nameof(ServiceCompanies)).Get<ServiceCompanies>()!.PhoneNumber,
                ConfigManager.Configuration.GetSection(nameof(ServiceCompanies)).Get<ServiceCompanies>()!.Password
            ),
            _ => throw new ArgumentException($"Unknown role: {role}")
        };
        
        _loginPage.WaitForPageToLoad();
        _loginPage.EnterPhoneNumber(phone);
        _loginPage.EnterPassword(password);
        _loginPage.ClickLoginButton();
    }
}
