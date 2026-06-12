using AndroidTests.Base;
using AndroidTests.Utils;
using OpenQA.Selenium;
using OpenQA.Selenium.Appium.Android;
using Serilog;

namespace AndroidTests.Pages;

public class EquipmentPage : BasePage
{
    private readonly AndroidDriver _driver;

    public EquipmentPage(AndroidDriver driver) : base(driver)
    {
        _driver = driver;
    }

    public bool WaitForPageToLoad()
    {
        Log.Information("Waiting for equipment page to load");
        
        return IsDisplayed(By.XPath("//android.view.View[@text=\"Автомобильные мойки\"]"));
    }

    public void ClickToCommercialEquipment()
    {
        Log.Information("Clicking commercial equipment page to load");

        ScrollForFind("Торговое нехолодильное оборудование");
        
        Click(By.XPath("//android.view.View[@text=\"Торговое нехолодильное оборудование\"]"));
        
        Log.Information("Click was successful");
    }

    public void AddPhoto(string localPhotoPath)
    {
        EmulatorManager.PushPhoto(localPhotoPath);
        
        Click(By.XPath("//android.view.View[@resource-id=\"reka-popover-trigger-v-52\"]"));
        
        Click(By.XPath("//android.view.View[@text=\"Выбрать фото\"]"));
        
        Click(By.XPath("//android.widget.TextView[@resource-id=\"com.google.android.apps.photos:id/title\" and @text=\"Pictures\"]"));
        
        Click(By.XPath("//android.widget.ImageView[@content-desc=\"Photo taken on Jun 6, 2026 5:02 AM\"]"));
        
        Click(By.XPath("//android.widget.Button[@content-desc=\"Done\"]"));
    }
    
    public void ClickToCreateRequest()
    {
        Log.Information("Clicking request page to load");
        
        Click(By.XPath("//android.widget.Button[@text=\"Создать заявку\"]"));
        
        Log.Information("Click was successful");
    }
    
    public void ClickToEditType()
    {
        Log.Information("Clicking on edit type to request");
        
        ClickUi("new UiSelector().text(\"Выберите тип заявки\")");
        
        Log.Information("Click was successful");
    }

    public void SelectionFault()
    {
        Log.Information("Selecting fault");
        
        Click(By.XPath("//android.widget.TextView[@text=\"Неисправность\"]"));
        
        Log.Information("Fault selected");
    }
    
    public void ClickToPriority()
    {
        Log.Information("Clicking on edit priority to request");
        
        ClickUi("new UiSelector().text(\"Выберите приоритет\")");
        
        Log.Information("Click was successful");
    }

    public void SelectionPlanned()
    {
        Log.Information("Selecting planned");
        
        Click(By.XPath("//android.widget.TextView[@text=\"Плановая\"]"));
        
        Log.Information("Click was successful");
    }
    
    public void TypeDescription()
    {
        Log.Information("Selecting type description");
        
        Type(By.XPath("//android.widget.EditText[@resource-id=\"description\"]"), "test successful");
        
        Log.Information("Type successful");
    }

    public void ClickToPerformer()
    {
        Log.Information("Clicking to performer");

        var performer = ScrollForFindInDialog("Исполнитель*");
        
        ClickUi("new UiSelector().className(\"android.widget.Button\").instance(5)");
        
        Log.Information("Click was successful");
    }

    public void ClickToPartners()
    {
        Log.Information("Clicking to partners");
        
        ClickUi("new UiSelector().resourceId(\"reka-tabs-v-62-trigger-vendor\")");
        
        Log.Information("Click was successful");
    }

    public void SelectionService()
    {
        Log.Information("Selecting service");
        
        ClickUi("new UiSelector().className(\"android.view.View\").instance(75)");
    }
    
    public void SelectionPerformer()
    {
        Log.Information("Selecting performer");
        
        Click(By.XPath("new UiSelector().className(\"android.view.View\").instance(75)"));
        
        Log.Information("Selecting successful");
    }
    
    public void SendRequest()
    {
        Log.Information("Sending request");
        
        Click(By.XPath("//android.widget.Button[@text=\"Отправить\"]"));
        
        Log.Information("Sending was successful");
    }
}