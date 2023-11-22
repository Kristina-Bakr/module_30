import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()

def test_show_pets(driver):
    # явные ожидания элементов страницы
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'email')))
    driver.find_element(By.ID, 'email').send_keys('tes@yandex.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Ищем на странице все фотографии, имена, породу (вид) и возраст питомцев:
    images = pytest.webdriver.find_elements_by_xpath('//img[@class="card-img-top"]')
    names = pytest.webdriver.find_elements_by_xpath('//h5[@class="card-title"]')
    descriptions = pytest.webdriver.find_elements_by_xpath('//p[@class="card-text"]')

    for i in range(len(names)):
        image_source = images[i].get_attribute('src')
        name_text = names[i].text
        print(f"Image source: {image_source}")
        print(f"Name text: {name_text}")

    # Проверяем, что на странице есть фото питомцев, имена, порода и возраст питомцев не пустые строки:
    for i in range(len(names)):
        image_source = images[i].get_attribute('src')
        name_text = names[i].text
        assert image_source != ''  # ( image_source не должен быть пустым.)
        assert names[i].text != ''  # ( name_text не должен быть пустым.)
        assert descriptions[i].text != ''  # (descriptions[i] не должен быть пустым.)
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(
            parts[0]) > 0  # (первая часть текста descriptions[i], разделенная запятой) должна иметь длину больше 0.
        assert len(
            parts[1]) > 0  # (вторая часть текста descriptions[i], разделенная запятой) должна иметь длину больше 0



def test_show_my_pets(pytest):
    # Вводим email, пароль, открываем главную страницу сайта
    pytest.webdriver.find_element(By.ID, 'email').send_keys('test@yandex.ru')
    pytest.webdriver.find_element(By.ID, 'pass').send_keys('12345')
    pytest.webdriver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.webdriver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Настраиваем переменную явного ожидания:
    wait = WebDriverWait(pytest.driver, 5)

    # Открываем /my_pets.
    pytest.webdriver.find_element_by_css_selector('a[href="/my_pets"]').click()

    # Ожидаем в течение 5с, что на странице есть тег h2 с текстом "All" - именем пользователя
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), "All"))

    pets_number = pytest.webdriver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    pets_count = pytest.webdriver.find_element(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    wait = WebDriverWait(pytest.driver, 5)
    assert int(pets_number) == len(pets_count)

    # в таблице все строки с полными данными питомцев
    css_locator = 'tbody>tr'
    data_my_pets = pytest.webdriver.find_elements_by_css_selector(css_locator)
    for i in range(len(data_my_pets)):
        assert wait.until(EC.visibility_of(data_my_pets[i]))

    # Ищем все фото питомцев
    image_my_pets = pytest.webdriver.find_elements_by_css_selector('img[style="max-width: 100px; max-height: 100px;"]')
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            assert wait.until(EC.visibility_of(image_my_pets[i]))

    # Ищем все имена питомцев
    name_my_pets = pytest.webdriver.find_elements_by_xpath('//tbody/tr/td[1]')
    for i in range(len(name_my_pets)):
        assert wait.until(EC.visibility_of(name_my_pets[i]))

    # Ищем все породы питомцев
    type_my_pets = pytest.webdriver.find_elements_by_xpath('//tbody/tr/td[2]')
    for i in range(len(type_my_pets)):
        assert wait.until(EC.visibility_of(type_my_pets[i]))

    # Ищем все данные возраста питомцев
    age_my_pets = pytest.webdriver.find_elements_by_xpath('//tbody/tr/td[3]')
    for i in range(len(age_my_pets)):
        assert wait.until(EC.visibility_of(age_my_pets[i]))

    # Ищем на странице my_pets статистику пользователя,
    # и из полученных данных получаем кол-во питомцев:
    all_statistics = pytest.webdriver.find_element_by_xpath('//div[@class=".col-sm-4 left"]').text.split("\n")
    statistics_pets = all_statistics[1].split(" ")
    all_my_pets = int(statistics_pets[-1])
    # количество строк в таблице с моими питомцами равно общему количеству питомцев,
    # в статистике:
    assert len(data_my_pets) == all_my_pets

    # Проверка - у половины питомцев есть фото:
    count = 0
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            count += 1
    assert count >= all_my_pets / 2

    # Проверка - всех питомцев есть имя:
    for i in range(len(name_my_pets)):
        assert name_my_pets[i].text != ''

    # Проверка - у всех питомцев есть порода:
    for i in range(len(type_my_pets)):
        assert type_my_pets[i].text != ''

    # Проверка - у всех питомцев есть возраст:
    for i in range(len(age_my_pets)):
        assert age_my_pets[i].text != ''

    # Проверка - у всех питомцев разные имена:
    list_name_my_pets = []
    for i in range(len(name_my_pets)):
        list_name_my_pets.append(name_my_pets[i].text)
    set_name_my_pets = set(list_name_my_pets)
    #  список в множество
    assert len(list_name_my_pets) == len(set_name_my_pets)

    # Проверяем, что в списке нет повторяющихся питомцев:
    list_data_my_pets = []
    for i in range(len(data_my_pets)):
        list_data = data_my_pets[i].text.split("\n")  # отделяем от данных питомца "х" удаления питомца
        list_data_my_pets.append(list_data[0])  # выбираем элемент с данными питомца и добавляем в список
    set_data_my_pets = set(list_data_my_pets)  # список в множество
    assert len(list_data_my_pets) == len(set_data_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть


