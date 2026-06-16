using AndroidTests.Base;
using AndroidTests.Config;
using AndroidTests.Models.Emulator;
using AndroidTests.Pages;
using Microsoft.Extensions.Configuration;

namespace AndroidTests.Tests.Owner;

/*[TestFixture, Order(1)]
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
        FillBaseRequestForm(_equipmentPage, _mainPage);
        _equipmentPage.ClickToPerformer();
        _equipmentPage.SelectionPerformer();
        _equipmentPage.SendRequest();
    }
}*/