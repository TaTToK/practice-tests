import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Словарь СТАБИЛЬНЫХ локаторов (устойчивы к перезапускам приложения)
LOCATORS = {
    # 1. Три точки (тут статический путь, оставляем)
    "three_dots": '//android.view.View[@resource-id="app"]/android.view.View/android.view.View[1]/android.view.View[3]/android.view.View[1]/android.view.View[2]/android.widget.Button',
    
    # 2. Кнопки с текстом (самые надежные, они не изменятся)
    "change_assignee": '//android.widget.Button[@text="Сменить исполнителя"]',
    "continue": '//android.widget.Button[@text="Продолжить"]',
    "cancel_checkbox": '//android.widget.CheckBox[@resource-id="shouldCancel"]',
    
    # 3. Поле "Новый исполнитель" (заменили точный "v-79" на поиск любого ID, начинающегося с "v-")
    "new_assignee": '//android.view.View[starts-with(@resource-id, "v-")]/android.view.View/android.view.View[2]/android.view.View',
    
    # 4. Вкладка "Партнеры" (целевое свойство "trigger-vendor" остается всегда, вырезали меняющийся v-97/v-88)
    "partners_tab": '//android.view.View[contains(@resource-id, "trigger-vendor")]',
    
    # 5. Варианты партнеров (привязались к неизменяемому "reka-dialog-content" вместо динамических ID диалога)
    "partner_masterskaya": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]/android.view.View/android.view.View[3]/android.view.View[1]/android.view.View',
    "partner_hospital": '//android.app.Dialog[contains(@resource-id, "reka-dialog-content")]/android.view.View/android.view.View[3]/android.view.View[2]/android.view.View',
    
    # 6. Финальное подтверждение
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

    # Исправленный XPath: добавinternalлена открывающая скобка в начале строки
    button_application = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH, '(//android.view.View[@content-desc="Заявки"])[2]'
        ))
    )
    
    print("Кликаем по вкладке 'Заявки'...")
    button_application.click()
    time.sleep(3)
    
    # 1. Нажимаем на три точки
    print("Нажимаем на три точки...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["three_dots"]))).click()

    # 2. Выбираем "Сменить исполнителя"
    print("Выбираем 'Сменить исполнителя'...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["change_assignee"]))).click()

    # 3. ПРОВЕРКА ГАЛОЧКИ АННУЛИРОВАНИЯ (Должна быть включена)
    print("Проверяем состояние чекбокса аннулирования...")
    cancel_chk = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, LOCATORS["cancel_checkbox"])))
    is_already_cancelled = cancel_chk.get_attribute("checked") == "true"
    print(f"Текущий статус галочки: {is_already_cancelled}")

    if not is_already_cancelled:
        print("Галочка НЕ стоит, активируем аннулирование...")
        cancel_chk.click()
    else:
        print("Галочка уже стоит. Пропускаем клик.")

    # 4. Нажимаем "Продолжить"
    print("Нажимаем кнопку 'Продолжить'...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["continue"]))).click()

    # 5. Выбираем нового исполнителя
    print("Открываем поле 'Новый исполнитель'...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["new_assignee"]))).click()

    # 6. Переходим на вкладку "Партнеры"
    print("Переходим на вкладку 'Партнеры'...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["partners_tab"]))).click()

    # 7. ПРОВЕРКА ВЫБРАННОГО ПАРТНЕРА
    print("Проверяем текущего выбранного партнера...")
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
    print("Подтверждаем смену исполнителя...")
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, LOCATORS["confirm_change"]))).click()

    print("Тест 'Смена исполнителя с аннулированием' успешно выполнен!")
    time.sleep(5)

except Exception as e:
    print(f"Произошла ошибка во время выполнения теста: {e}")
finally:
    print("Закрываем сессию драйвера...")
    driver.quit()