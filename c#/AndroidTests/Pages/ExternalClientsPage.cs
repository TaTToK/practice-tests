using AndroidTests.Base;
using OpenQA.Selenium;
using OpenQA.Selenium.Appium.Android;
using Serilog;

namespace AndroidTests.Pages;

public class ExternalClientsPage : BasePage
{
    private readonly AndroidDriver _driver;

    public ExternalClientsPage(AndroidDriver driver) : base(driver)
    {
        _driver = driver;
    }
    
    public void ClickToCreateExternalClient()
    {
        Log.Information("Clicking button to create external client");
        
        Click(By.XPath("//android.view.View[@resource-id=\"app\"]/android.view.View/android.widget.Button[2]"));
        
        Log.Information("Click is successfully");
    }

    public void TypeNameCompany()
    {
        Log.Information("Typing name of company");
        
        Type(By.XPath("//android.view.View[@resource-id=\"app\"]/android.view.View/android.widget.Button[2]"), "Test company");
        
        Log.Information("Typing is successfully");
    }

    public void ClickToDetails()
    {
        Log.Information("Clicking button to details");
        
        Click(By.XPath("//android.view.View[@text=\"Реквизиты\"]"));
        
        Log.Information("Click is successfully");
    }
    
    public void TypeINN()
    {
        Log.Information("Typing INN");
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"inn\"]"), "7707083893");
        
        Log.Information("Typing is successfully");
    }
    
    public void TypeOGRN()
    {
        Log.Information("Typing OGRN");

        ScrollForFindInDialogElement(By.XPath("//android.widget.EditText[@resource-id='ogrn']"));
        
        Type(By.XPath("//android.widget.EditText[@resource-id='ogrn']"), "1027700132195");
        
        Log.Information("Typing is successfully");
    }

    public void TypeKPP()
    {
        Log.Information("Typing KPP");
        
        ScrollForFindInDialogElement(By.XPath("//android.widget.EditText[@resource-id=\"kpp\"]"));
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"kpp\"]"), "770701001");
        
        Log.Information("Typing is successfully");
    }

    public void TypeLegalAddress()
    {
        Log.Information("Typing legal address");

        ScrollForFindInDialogElement(By.XPath("//android.widget.EditText[@resource-id=\"legalAddress\"]"));
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"legalAddress\"]"), "101000, г. Москва, ул. Тестовая, д. 1, офис 1");
        
        Log.Information("Typing is successfully");
    }

    public void TypeName()
    {
        Log.Information("Typing name");

        ScrollForFindInDialogElement(By.XPath("//android.view.View[@text=\"Имя*\"]"));
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"contactName\"]"), "Тест");
        
        Log.Information("Typing is successfully");
    }

    public void TypePhoneNumber()
    {
        Log.Information("Typing phone number");

        ScrollForFindInDialogElement(By.XPath("//android.view.View[@text=\"Телефон*\"]"));

        Type(By.XPath("//android.widget.EditText[@resource-id=\"contactPhone\"]"), "79262266015");
        
        Log.Information("Typing is successfully");
    }
    
    public void TypeEmail()
    {
        Log.Information("Typing email");

        ScrollForFindInDialogElement(By.XPath("//android.view.View[@text=\"Email\"]"));

        Type(By.XPath("//android.widget.EditText[@resource-id=\"contactEmail\"]"), "test@example.com");
        
        Log.Information("Typing is successfully");
    }

    public void ClickToBankDetails()
    {
        Log.Information("Clicking button to bank details");

        ScrollForFindInDialogElement(By.XPath("//android.view.View[@text=\"Банковские реквизиты\"]"));
        
        Click(By.XPath("//android.view.View[@text=\"Банковские реквизиты\"]"));
        
        Log.Information("Click is successfully");
    }

    public void TypeBIK()
    {
        Log.Information("Typing BIK");

        ScrollForFindInDialogElement(By.XPath("//android.view.View[@text=\"БИК\"]"));
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"bik\"]"), "044525225");
        
        Log.Information("Typing is successfully");
    }

    public void TypeNameBank()
    {
        Log.Information("Typing type bank");

        ScrollForFindInDialogElement(By.XPath("//android.view.View[@text=\"Название банка\"]"));

        Type(By.XPath("//android.widget.EditText[@resource-id=\"bankName\"]"), "ПАО Сбербанк");
        
        Log.Information("Typing is successfully");
    }

    public void TypeCurrentAccount()
    {
        Log.Information("Typing current account");

        ScrollForFindInDialogElement(By.XPath("//android.view.View[@text=\"Расчётный счёт\"]"));

        Type(By.XPath("//android.widget.EditText[@resource-id=\"settlementAccount\"]"), "407 ");
        
        Log.Information("Typing is successfully");
    }

    public void TypeCorrespondentAccount()
    {
        Log.Information("Typing correspondent account");

        ScrollForFindInDialogElement(By.XPath("//android.view.View[@text=\"Корреспондентский счёт\"]"));
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"correspondentAccount\"]"), "3010392089350489230");
        
        Log.Information("Typing is successfully");
    }

    public void TypeDescription()
    {
        Log.Information("Typing description");

        ScrollForFindInDialogElement(By.XPath("//android.view.View[@text=\"Описание\"]"));
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"description\"]"), "Test successful");
        
        Log.Information("Typing is successfully");
    }

    public void TypeEquipment()
    {
        Log.Information("Typing equipment");

        ScrollForFindInDialogElement(By.XPath("//android.view.View[@text=\"Тип оборудования\"]"));
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"equipmentType\"]"), "Test equipment");
        
        Log.Information("Typing is successfully");
    }

    public void ClickToSave()
    {
        Log.Information("Clicking button to save");

        ScrollForFindInDialogElement(By.XPath("//android.widget.Button[@text=\"Сохранить\"]"));

        Click(By.XPath("//android.widget.Button[@text=\"Сохранить\"]"));
        
        Log.Information("Click is successfully");
    }
}