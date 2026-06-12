using OpenQA.Selenium;
using OpenQA.Selenium.Appium;
using OpenQA.Selenium.Appium.Android;
using OpenQA.Selenium.Interactions;
using OpenQA.Selenium.Support.UI;
using Serilog;

namespace AndroidTests.Base;

public abstract class BasePage
{
    protected readonly AndroidDriver Driver;

    protected BasePage(AndroidDriver driver)
    {
        Driver = driver;
    }

    protected IWebElement WaitForElement(By by, int timeoutSeconds = 10)
    {
        var wait = new WebDriverWait(
            Driver,
            TimeSpan.FromSeconds(timeoutSeconds));

        return wait.Until(d => d.FindElement(by));
    }

    protected void Click(By by)
    {
        var locator = by;
        
        try
        {
            Log.Information(
                "Trying to click element {Locator}",
                locator);
            
            WaitForElement(locator).Click();
        }
        catch (Exception e)
        {
            Log.Error(
                e,
                "Failed to click element {Locator}",
                locator);
            
            throw;
        }
    }

    protected void Type(By by, string text)
    {
        var element = WaitForElement(by);
        
        element.Clear();
        element.SendKeys(text);
    }
    
    protected bool IsDisplayed(By by)
    {
        var element = WaitForElement(by);

        return element.Displayed;
    }

    protected void ScrollDown()
    {
        Driver.ExecuteScript(
            "mobile: scrollGesture",
            new Dictionary<string, object>
            {
                { "left", 100 },
                { "top", 100 },
                { "width", 800 },
                { "height", 1600 },
                { "direction", "down" },
                { "percent", 0.8 }
            });
    }

    protected IWebElement ScrollForFind(string text)
    {
        var element = Driver.FindElement(
            MobileBy.AndroidUIAutomator(
                "new UiScrollable(new UiSelector().scrollable(true))" +
                $".scrollIntoView(new UiSelector().text(\"{text}\"))"));
        
        return element;
    }
    
    protected IWebElement ScrollForFindInDialog(string text)
    {
        try
        {
            return Driver.FindElement(By.XPath($"//*[@text='{text}']"));
        }
        catch (NoSuchElementException) { }

        for (int i = 0; i < 5; i++)
        {
            var finger = new PointerInputDevice(PointerKind.Touch, "finger");
            var sequence = new ActionSequence(finger);
            sequence.AddAction(finger.CreatePointerMove(CoordinateOrigin.Viewport, 540, 1200, TimeSpan.Zero));
            sequence.AddAction(finger.CreatePointerDown(MouseButton.Left));
            sequence.AddAction(finger.CreatePointerMove(CoordinateOrigin.Viewport, 540, 600, TimeSpan.FromMilliseconds(500)));
            sequence.AddAction(finger.CreatePointerUp(MouseButton.Left));
            Driver.PerformActions(new List<ActionSequence> { sequence });
            Thread.Sleep(500);

            try
            {
                return Driver.FindElement(By.XPath($"//*[@text='{text}']"));
            }
            catch (NoSuchElementException) { }
        }

        throw new NoSuchElementException($"Element '{text}' not found after scrolling");
    }

    public void ClickUi(string mobile)
    {
        var element = MobileBy.AndroidUIAutomator(mobile);
        Click(element);
    }
}