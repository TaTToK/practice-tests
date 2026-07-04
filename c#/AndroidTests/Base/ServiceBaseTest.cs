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
        GlobalSetup();
        
        var service = ConfigManager.Configuration
            .GetSection(nameof(ServiceCompanies))
            .Get<ServiceCompanies>();

        new LoginPage(Driver!).Login(service.PhoneNumber, service.Password);
    }

    protected void ServiceFillBaseRequestForm(ExternalClientsPage externalClientsPage, ServiceCompanyMainPage service)
    {
        service.WaitForPageToLoad();
        service.ClickToAllowNotifications();
        service.ClickToExternalClient();
        
        externalClientsPage.ClickToCreateExternalClient();
        externalClientsPage.TypeNameCompany();
        externalClientsPage.ClickToDetails();
        externalClientsPage.TypeINN();
        externalClientsPage.TypeOGRN();
        externalClientsPage.TypeKPP();
        externalClientsPage.TypeLegalAddress();
        externalClientsPage.TypeName();
        externalClientsPage.TypePhoneNumber();
        externalClientsPage.TypeEmail();
        externalClientsPage.ClickToBankDetails();
        externalClientsPage.TypeBIK();
        externalClientsPage.TypeNameBank();
        externalClientsPage.TypeCurrentAccount();
        externalClientsPage.TypeCorrespondentAccount();
        externalClientsPage.TypeDescription();
        externalClientsPage.TypeEquipment();
    }
}