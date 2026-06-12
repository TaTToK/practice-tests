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
    
    # Теперь ищем СТРОГО сам текст внутри нужного диалога, без родительских контейнеров
    "partner_masterskaya": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]//*[contains(@text, "Мастерская")]',
    "partner_hospital": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]//*[contains(@text, "Больница")]',
    "partner_tszh": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]//*[contains(@text, "Красный 234")]',
    
    "confirm_change": '//android.widget.Button[@text="Сменить исполнителя"]',
    
    "tab_assignee": '//android.view.View[contains(@resource-id, "trigger-assignee")]',
    "current_assignee_text": '//android.widget.TextView[contains(@resource-id, "reka-popover-trigger")]'
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
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["new_assignee"])))
    time.sleep(1) # Небольшая пауза для стабильности анимации развертывания
    driver.find_element(AppiumBy.XPATH, LOCATORS["new_assignee"]).click()

    print("Переходим на вкладку 'Партнеры'...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["partners_tab"]))).click()
    time.sleep(1)

    # --- НАДЕЖНЫЙ ВЫБОР ПАРТНЕРА ---
    print("Проверяем доступность партнеров...")
    
    masterskaya = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["partner_masterskaya"])))
    
    # Умная проверка: если элемент checked, selected ИЛИ disabled (enabled == false), значит он нам не подходит
    is_masterskaya_busy = (masterskaya.get_attribute("checked") == "true" or 
                           masterskaya.get_attribute("selected") == "true" or 
                           masterskaya.get_attribute("enabled") == "false")

    target_element = None
    expected_partner_text = ""

    if is_masterskaya_busy:
        print("ООО 'Мастерская' недоступна или уже занята. Проверяем ГБУЗ 'Больница'...")
        hospital = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["partner_hospital"])))
        is_hospital_busy = (hospital.get_attribute("checked") == "true" or 
                             hospital.get_attribute("selected") == "true" or 
                             hospital.get_attribute("enabled") == "false")
        
        if is_hospital_busy:
            print("ГБУЗ 'Больница' тоже занята! Выбираем ТСЖ 'Красный 234'...")
            target_element = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["partner_tszh"])))
            expected_partner_text = "Красный 234"
        else:
            print("ГБУЗ 'Больница' свободна. Выбираем её!")
            target_element = hospital
            expected_partner_text = "Больница"
    else:
        print("ООО 'Мастерская' свободна. Выбираем её!")
        target_element = masterskaya
        expected_partner_text = "Мастерская"

    # Кликаем ТОЧНО по элементу текста выбранного партнера
    target_element.click()
    print(f"Выбран партнер, ожидаем в конце подстроку: '{expected_partner_text}'")
    time.sleep(1.5) # Даем шторке выбора закрыться после клика

    print("Подтверждаем смену исполнителя...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["confirm_change"]))).click()
    time.sleep(3)

    # --- ПРОВЕРКА РЕЗУЛЬТАТА ---
    print("\n--- НАЧАЛО ПРОВЕРКИ РЕЗУЛЬТАТА ---")
    print("Переходим на вкладку 'Исполнитель' в карточке заявки...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["tab_assignee"]))).click()
    time.sleep(1.5)

    actual_assignee_element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["current_assignee_text"])))
    actual_assignee_text = actual_assignee_element.text
    print(f"Фактически на экране отображается исполнитель: '{actual_assignee_text}'")

    if expected_partner_text in actual_assignee_text:
        print(f"УСПЕХ! Данные обновились корректно. Исполнитель содержит: '{expected_partner_text}'")
    else:
        print(f"ВНИМАНИЕ! Проверка не прошла. Ожидали увидеть '{expected_partner_text}', но на экране: '{actual_assignee_text}'")
        raise AssertionError("Фактический исполнитель на экране не совпадает с выбранным партнером!")

    print("\nТест 'Смена исполнителя с аннулированием' успешно выполнен!")
    time.sleep(2)

except Exception as e:
    print(f"Произошла ошибка во время выполнения теста: {e}")
finally:
    print("Закрываем сессию драйвера...")
    driver.quit()
