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
    
    # Ищем СТРОГО сам текст внутри нужного диалога, чтобы кликать точно в цель
    "partner_masterskaya": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]//*[contains(@text, "Мастерская")]',
    "partner_hospital": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]//*[contains(@text, "Больница")]',
    "partner_tszh": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]//*[contains(@text, "Красный 234")]',
    
    "confirm_change": '//android.widget.Button[@text="Сменить исполнителя"]',
    
    # Локаторы для финального Ассерта (Защищены от динамических v-ID)
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

print("Запуск сценария: Смена исполнителя БЕЗ АННУЛИРОВАНИЯ")
driver = webdriver.Remote('http://localhost:4723', options=options)
wait = WebDriverWait(driver, 15)

try:
    print("--- ШАГ 0: Проверка экрана и переход в Заявки ---")
    
    button_application = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH, '(//android.view.View[@content-desc="Заявки"])[2]'
        ))
    )
    print("Вкладка 'Заявки' найдена, кликаем...")
    button_application.click()
    time.sleep(3)
    
    print("--- ШАГ 1: Открытие меню заявки ---")
    print("Нажимаем на три точки...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["three_dots"]))).click()

    print("--- ШАГ 2: Клик по 'Сменить исполнителя' ---")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["change_assignee"]))).click()

    print("--- ШАГ 3: Проверка чекбокса аннулирования ---")
    cancel_chk = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["cancel_checkbox"])))
    is_already_cancelled = cancel_chk.get_attribute("checked") == "true"
    print(f"Текущий статус галочки на экране: {is_already_cancelled}")

    if is_already_cancelled:
        print("Галочка СТОИТ, а нам не нужно. Кликаем, чтобы снять!")
        cancel_chk.click()
    else:
        print("Галочка не стоит, всё ок. Пропускаем клик.")

    print("--- ШАГ 4: Нажатие кнопки 'Продолжить' ---")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["continue"]))).click()

    print("--- ШАГ 5: Выбор нового исполнителя ---")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["new_assignee"])))
    time.sleep(1) # Короткая пауза для стабильности анимации развертывания
    driver.find_element(AppiumBy.XPATH, LOCATORS["new_assignee"]).click()

    print("--- ШАГ 6: Переход на вкладку 'Партнеры' ---")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["partners_tab"]))).click()
    time.sleep(1)

    print("--- ШАГ 7: Умный выбор партнера ---")
    print("Проверяем доступность партнеров в списке...")
    
    masterskaya = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["partner_masterskaya"])))
    
    # Тройная проверка доступности: checked, selected или заблокирован (enabled == false)
    is_masterskaya_busy = (masterskaya.get_attribute("checked") == "true" or 
                           masterskaya.get_attribute("selected") == "true" or 
                           masterskaya.get_attribute("enabled") == "false")

    target_element = None
    expected_partner_text = ""

    if is_masterskaya_busy:
        print("ООО 'Мастерская' недоступна (выбрана или серая). Проверяем ГБУЗ 'Больница'...")
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

    # Кликаем строго по тексту выбранной организации
    target_element.click()
    print(f"Выбран партнер, запоминаем для финальной проверки: '{expected_partner_text}'")
    time.sleep(1.5) # Даем шторке выбора корректно скрыться

    print("--- ШАГ 8: Подтверждение изменений ---")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["confirm_change"]))).click()
    time.sleep(3) # Ждем, пока диалог сохранится и закроется

    print("--- ШАГ 9: Проверка результата на экране заявки ---")
    print("Переходим на вкладку 'Исполнитель' в карточке заявки...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["tab_assignee"]))).click()
    time.sleep(1.5)

    # Забираем актуальное текстовое значение исполнителя
    actual_assignee_element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["current_assignee_text"])))
    actual_assignee_text = actual_assignee_element.text
    print(f"Фактически на экране отображается исполнитель: '{actual_assignee_text}'")

    # Сверяем, содержит ли итоговая строка имя выбранной нами компании
    if expected_partner_text in actual_assignee_text:
        print(f"[УСПЕХ]: Данные в карточке обновились! Исполнитель содержит: '{expected_partner_text}'")
    else:
        print(f"[ВНИМАНИЕ]: Ошибка валидации! Ждали '{expected_partner_text}', а на экране красуется: '{actual_assignee_text}'")
        raise AssertionError("Фактический исполнитель на экране не совпадает с выбранным партнером!")

    print("\nТест 'Смена исполнителя без аннулирования' успешно выполнен!")
    time.sleep(2)

except Exception as e:
    print(f"\n[ОШИБКА ТЕСТА]: {e}")
finally:
    print("Закрываем сессию драйвера...")
    driver.quit()
