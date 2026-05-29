import time
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
# Импортируем модули для умного ожидания элементов:
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = AppiumOptions()
options.set_capability('platformName', 'Android')
options.set_capability('automationName', 'UiAutomator2')
options.set_capability('deviceName', 'emulator-5554')
options.set_capability('appPackage', 'udp.reeng.app')
options.set_capability('appActivity', 'udp.reeng.app.MainActivity')
options.set_capability('noReset', False) 

print("Подключаемся к Appium серверу и запускаем приложение...")
driver = webdriver.Remote('http://localhost:4723', options=options)

# Настраиваем объект ожидания: максимум ждем 15 секунд появления элемента
wait = WebDriverWait(driver, 15)

try:
    print("Ожидаем появления поля ввода телефона на экране...")
    # Ищем поле телефона по твоему полному XPath
    phone_field = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH, '//android.widget.EditText[@resource-id="phone"]'
        ))
    )
    
    print("Поле телефона найдено! Вводим номер...")
    phone_field.click()
    phone_field.clear()
    phone_field.send_keys("+79160000071")

    # Ищем поле пароля
    print("Ожидаем появления поля пароля...")
    password_field = wait.until(
        EC.presence_of_element_located((
            AppiumBy.XPATH, '//android.widget.EditText[@resource-id="password"]'
        ))
    )
    
    print("Поле пароля найдено! Вводим пароль...")
    password_field.click()
    password_field.clear()
    password_field.send_keys("Qwerty100")

    # Скрываем клавиатуру
    if driver.is_keyboard_shown():
        print("Скрываем клавиатуру...")
        driver.hide_keyboard()

    # НАЖАТИЕ НА КНОПКУ "ВОЙТИ"
    print("Ожидаем появления кнопки 'Войти'...")
    login_button = wait.until(
        EC.element_to_be_clickable((
            AppiumBy.XPATH, '//android.widget.Button[@text="Войти"]'
        ))
    )
    
    print("Кнопка найдена! Нажимаем 'Войти'...")
    login_button.click()
    
    # Даем приложению загрузить главный экран после входа
    print("Ожидаем переход на главный экран...")
    time.sleep(7)
    print("Тест авторизации успешно завершен!")

except Exception as e:
    print(f"\nПроизошла ошибка во время выполнения теста:\n{e}")
