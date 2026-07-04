using AndroidTests.Base;
using AndroidTests.Pages;

namespace AndroidTests.Tests.Owner;

[TestFixture, Order(1)]
public class CreateRequestExternalClientTest : ServiceBaseTest
{
    private ExternalClientsPage _externalClientsPage = null!;
    private ServiceCompanyMainPage _mainPage = null!;

    [SetUp]
    public void TestSetUp()
    {
        _externalClientsPage = new ExternalClientsPage(Driver!);
        _mainPage = new ServiceCompanyMainPage(Driver!);
    }

    [Test]
    public void CreateRequestToExternalClientTest()
    {
        _externalClientsPage.ClickToSave();
    }
}