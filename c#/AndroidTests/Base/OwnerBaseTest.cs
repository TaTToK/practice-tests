using AndroidTests.Config;
using AndroidTests.Models.Emulator;
using AndroidTests.Models.Login;
using AndroidTests.Pages;
using Microsoft.Extensions.Configuration;

namespace AndroidTests.Base;

public class OwnerBaseTest : BaseTest
{
    [OneTimeSetUp]
    public void Setup()
    {
        GlobalSetup();
    
        var owner = ConfigManager.Configuration
            .GetSection(nameof(OwnerEquipment))
            .Get<OwnerEquipment>();
    
        new LoginPage(Driver!).Login(owner!.PhoneNumber, owner.Password);
    }
    
    protected void FillBaseRequestForm(EquipmentPage equipmentPage, MainPage mainPage)
    {
        var photoPath = ConfigManager.Configuration
            .GetSection(nameof(EmulatorSettings))
            .Get<EmulatorSettings>()!.TestPhotoPath;

        mainPage.ClickToAllowNotifications();
        mainPage.WaitForPageToLoad();
        mainPage.ClickToCreateRequest();
        equipmentPage.WaitForPageToLoad();
        equipmentPage.ClickToCommercialEquipment();
        equipmentPage.ClickToCreateRequest();
        equipmentPage.AddPhoto(photoPath);
        equipmentPage.ClickToEditType();
        equipmentPage.SelectionFault();
        equipmentPage.ClickToPriority();
        equipmentPage.SelectionPlanned();
        equipmentPage.TypeDescription();
    }
}