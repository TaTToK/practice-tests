import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Полностью динамический словарь локаторов (устойчив к смене порядка элементов)
LOCATORS = {
    "three_dots": '//android.view.View[@resource-id="app"]/android.view.View/android.view.View[1]/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.widget.Button',
    "change_assignee": '//android.widget.Button[@text="Сменить исполнителя"]',
    "continue": '//android.widget.Button[@text="Продолжить"]',
    "cancel_checkbox": '//android.widget.CheckBox[@resource-id="shouldCancel"]',
    
    # Поле "Новый исполнитель"
    "new_assignee": '//android.view.View[starts-with(@resource-id, "v-")]/android.view.View/android.view.View[2]/android.view.View',
    "partners_tab": '//android.view.View[contains(@resource-id, "trigger-vendor")]',
    
    # --- УМНЫЙ ПОИСК КОМПАНИЙ ПО ТЕКСТУ ---
    # Ищем внутри диалога элемент View, у которого внутри (в тексте или в дочерних элементах) есть слово "Мастерская"
    "partner_masterskaya": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]//android.view.View[contains(@text, "Мастерская") or .//*[contains(@text, "Мастерская")]]',
    
    # Ищем внутри диалога элемент View, у которого внутри есть слово "Больница"
    "partner_hospital": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]//android.view.View[contains(@text, "Больница") or .//*[contains(@text, "Больница")]]',
    
    "confirm_change": '//android.widget.Button[@text="Сменить исполнителя"]'
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
    
    # Ищем вкладку "Заявки" с правильными скобками для индекса
    button_application = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH, '(//android.view.View[@content-desc="Заявки"])[2]'
        ))
    )
    print("Вкладка 'Заявки' найдена, кликаем...")
    button_application.click()
    time.sleep(3)

    # !!! ВНИМАНИЕ !!! 
    # Если ты попал на список заявок, здесь нужен клик по конкретной заявке, например:
    # wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "ТВОЙ_ЛОКАТОР_ЗАЯВКИ"))).click()
    
    # 1. Нажимаем на три точки
    print("--- ШАГ 1: Открытие меню заявки ---")
    print("Нажимаем на три точки...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["three_dots"]))).click()

    # 2. Выбираем "Сменить исполнителя"
    print("--- ШАГ 2: Клик по 'Сменить исполнителя' ---")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["change_assignee"]))).click()

    # 3. ПРОВЕРКА ГАЛОЧКИ АННУЛИРОВАНИЯ (Должна быть ВЫКЛЮЧЕНА)
    print("--- ШАГ 3: Проверка чекбокса аннулирования ---")
    cancel_chk = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["cancel_checkbox"])))
    is_already_cancelled = cancel_chk.get_attribute("checked") == "true"
    print(f"Текущий статус галочки на экране: {is_already_cancelled}")

    if is_already_cancelled:
        print("Галочка СТОИТ, а нам не нужно. Кликаем, чтобы снять!")
        cancel_chk.click()
    else:
        print("Галочка не стоит, всё ок. Пропускаем клик.")

    # 4. Нажимаем "Продолжить"
    print("--- ШАГ 4: Нажатие кнопки 'Продолжить' ---")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["continue"]))).click()

    # 5. Выбираем нового исполнителя
    print("--- ШАГ 5: Выбор нового исполнителя ---")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["new_assignee"]))).click()

    # 6. Переходим на вкладку "Партнеры"
    print("--- ШАГ 6: Переход на вкладку 'Партнеры' ---")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["partners_tab"]))).click()

    # 7. ПРОВЕРКА ВЫБРАННОГО ПАРТНЕРА
    print("--- ШАГ 7: Умный выбор партнера ---")
    masterskaya = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["partner_masterskaya"])))
    is_masterskaya_selected = (masterskaya.get_attribute("checked") == "true" or 
                               masterskaya.get_attribute("selected") == "true")

    if is_masterskaya_selected:
        print("ООО 'Мастерская' уже выбрана! Переключаемся на ГБУЗ 'Больница'...")
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["partner_hospital"]))).click()
    else:
        print("ООО 'Мастерская' свободна. Выбираем её!")
        masterskaya.click()

    # 8. Финальное подтверждение
    print("--- ШАГ 8: Подтверждение изменений ---")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["confirm_change"]))).click()

    print("Тест 'Смена исполнителя без аннулирования' успешно выполнен!")
    time.sleep(5)

except Exception as e:
    print(f"\n[ОШИБКА ТЕСТА]: {e}")
finally:
    print("Закрываем сессию драйвера...")
    driver.quit()