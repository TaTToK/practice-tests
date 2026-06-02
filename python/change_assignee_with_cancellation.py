import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOCATORS = {
    "three_dots": '//android.view.View[@resource-id="app"]/android.view.View/android.view.View[1]/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.widget.Button',
    "change_assignee": '//android.widget.Button[@text="Сменить исполнителя"]',
    "continue": '//android.widget.Button[@text="Продолжить"]',
    "cancel_checkbox": '//android.widget.CheckBox[@resource-id="shouldCancel"]',
    "new_assignee": '//android.view.View[starts-with(@resource-id, "v-")]/android.view.View/android.view.View[2]/android.view.View',
    "partners_tab": '//android.view.View[contains(@resource-id, "trigger-vendor")]',
    "partner_masterskaya": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View',
    "partner_hospital": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View',
    "confirm_change": '//android.widget.Button[@text="Сменить исполнителя"]'
}

options = AppiumOptions()
options.set_capability('platformName', 'Android')
options.set_capability('automationName', 'UiAutomator2')
options.set_capability('deviceName', 'emulator-5554')
options.set_capability('appPackage', 'udp.reeng.app')
options.set_capability('appActivity', 'udp.reeng.app.MainActivity')
options.set_capability('noReset', True)

print("Запуск сценария: Смена исполнителя С АННУЛИРОВАНИЕМ")
driver = webdriver.Remote('http://localhost:4723', options=options)
wait = WebDriverWait(driver, 15)

try:
    print("Начало симуляции")

    button_application = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH, '(//android.view.View[@content-desc="Заявки"])[2]'
        ))
    )

    print("Кликаем по вкладке 'Заявки'...")
    button_application.click()
    time.sleep(3)

    print("Нажимаем на три точки...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["three_dots"]))).click()

    print("Выбираем 'Сменить исполнителя'...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["change_assignee"]))).click()

    print("Проверяем состояние чекбокса аннулирования...")
    cancel_chk = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["cancel_checkbox"])))
    is_already_cancelled = cancel_chk.get_attribute("checked") == "true"
    print(f"Текущий статус галочки: {is_already_cancelled}")

    if not is_already_cancelled:
        print("Галочка НЕ стоит, активируем аннулирование...")
        cancel_chk.click()
    else:
        print("Галочка уже стоит. Пропускаем клик.")

    print("Нажимаем кнопку 'Продолжить'...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["continue"]))).click()

    print("Открываем поле 'Новый исполнитель'...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["new_assignee"]))).click()

    print("Переходим на вкладку 'Партнеры'...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["partners_tab"]))).click()

    print("Проверяем текущего выбранного партнера...")
    masterskaya = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["partner_masterskaya"])))
    is_masterskaya_selected = (
        masterskaya.get_attribute("checked") == "true" or
        masterskaya.get_attribute("selected") == "true"
    )

    if is_masterskaya_selected:
        print("ООО 'Мастерская' уже выбрана! Переключаемся на ГБУЗ 'Больница'...")
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["partner_hospital"]))).click()
    else:
        print("ООО 'Мастерская' свободна. Выбираем её!")
        masterskaya.click()

    print("Подтверждаем смену исполнителя...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["confirm_change"]))).click()

    print("Тест 'Смена исполнителя с аннулированием' успешно выполнен!")
    time.sleep(5)

except Exception as e:
    print(f"Произошла ошибка во время выполнения теста: {e}")
finally:
    print("Закрываем сессию драйвера...")
    driver.quit()
