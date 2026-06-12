using AndroidTests.Config;
using AndroidTests.Models.Login;
using AndroidTests.Pages;
using Microsoft.Extensions.Configuration;

namespace AndroidTests.Base;

public class ServiceBaseTest : BaseTest
{
    [OneTimeSetUp]
    public void LoginAsService()
    {
        var service = ConfigManager.Configuration
            .GetSection(nameof(ServiceCompanies))
            .Get<ServiceCompanies>();

        new LoginPage(Driver!).Login(service.PhoneNumber, service.Password);
    }
}