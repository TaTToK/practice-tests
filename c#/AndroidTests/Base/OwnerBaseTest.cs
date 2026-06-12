using AndroidTests.Config;
using AndroidTests.Models.Login;
using AndroidTests.Pages;
using Microsoft.Extensions.Configuration;

namespace AndroidTests.Base;

public class OwnerBaseTest : BaseTest
{
    [OneTimeSetUp]
    public void LoginAsOwner()
    {
        var owner = ConfigManager.Configuration
            .GetSection(nameof(OwnerEquipment))
            .Get<OwnerEquipment>();
        
        new LoginPage(Driver!).Login(owner.PhoneNumber, owner.Password);
    }
}