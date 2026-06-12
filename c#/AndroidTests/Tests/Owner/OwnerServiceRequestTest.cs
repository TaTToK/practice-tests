using AndroidTests.Base;
using AndroidTests.Config;
using AndroidTests.Models.Emulator;
using AndroidTests.Pages;
using Microsoft.Extensions.Configuration;

namespace AndroidTests.Tests.Owner;

[TestFixture, Order(2)]
public class OwnerServiceRequestTest : OwnerBaseTest
{
    private EquipmentPage _equipmentPage = null!;
    private MainPage _mainPage = null!;

    [SetUp]
    public void TestSetUp()
    {
        _equipmentPage = new EquipmentPage(Driver!);
        _mainPage = new MainPage(Driver!);
    }

    [Test]
    public void CreateRequestToOwnerServiceTest()
    {
        _mainPage.ClickToAllowNotifications();
        _mainPage.WaitForPageToLoad();
        _mainPage.ClickToCreateRequest();
        _equipmentPage.WaitForPageToLoad();
        _equipmentPage.ClickToCommercialEquipment();
        _equipmentPage.ClickToCreateRequest();
        _equipmentPage.AddPhoto(ConfigManager.Configuration.GetSection(nameof(EmulatorSettings)).Get<EmulatorSettings>()!.TestPhotoPath);
        _equipmentPage.ClickToEditType();
        _equipmentPage.SelectionFault();
        _equipmentPage.ClickToPriority();
        _equipmentPage.SelectionPlanned();
        _equipmentPage.TypeDescription();
        _equipmentPage.ClickToPerformer();
        _equipmentPage.SelectionPerformer();
        _equipmentPage.SendRequest();
    }
}