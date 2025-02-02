from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Parsing:
    def __init__(self, driver_path: str):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-extensions")
        # Uncomment the next line to run in headless mode
        self.options.add_argument("--headless")

        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def load_main(self, url: str, wait_time: int = 15)-> dict:
              
        try:
            self.driver.get(url)
            self.list_anime = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#wrap > div:nth-child(5) > div > div > div.col-12.col-md-12.col-lg-6.col-xl-4.mb-3.mb-md-0.content-block')))

            self.click_container()
            self.d_anime = self.anime_id_name_data_href_photo()
            
            time.sleep(3)
            print(f"Page loaded successfully: {url}")
        except Exception as ex:
            print(f"An error occurred: {ex}")
        finally:
            self.close_driver()
            return self.d_anime

    def click_container(self) -> None:
        try:
            for cl in self.list_anime.find_elements(By.CLASS_NAME, "bb-dashed-1"):
                if cl.get_attribute('aria-expanded') == "false":
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(cl)).click()
                    time.sleep(1)
        except Exception as ex:
            print(f"An error in click_container occurred: {ex}")


    def anime_id_name_data_href_photo(self, wait_time : int = 15) -> dict:
        d = {}
        days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]  
        for  index, day_anime in enumerate(self.list_anime.find_elements(By.CLASS_NAME, 'last-update-container.scroll.collapse.show')):
            try:
                lst_pr = []
                
                name = day_anime.find_elements(By.TAG_NAME, 'span')
                data = day_anime.find_elements(By.CLASS_NAME, 'ml-3.text-right')
                href = day_anime.find_elements(By.CLASS_NAME, 'card-link.list-group-item-action.bg-transparent')
                photo = day_anime.find_elements(By.CLASS_NAME, 'img-square.lazy.br-50')
             
                    
                for ind, an in enumerate(name):
                    #### photo address processing
                    thd = photo[ind].get_attribute("data-original")
                    f = thd.find('120')
                    result = thd[:f] + "500x700" + thd[f+7:]
                    ##### data address processing
                    episod, dt = data[ind].text.split('\n')
                
                    lst_pr.append([ind+1, an.text, episod, dt, href[ind].get_attribute('href'), result])
                d[days_of_week[index]] = lst_pr
            except Exception as ex:
                print(f"An error in anime_name_data_href occurred: {ex}")
    
        return d

    def close_driver(self):
        if self.driver:
            self.driver.quit()  # No need to call .close()

# Usage example
if __name__ == "__main__":
    driver_path = r"C:\working\Python\parcing\AnimeGo\app\database\chromedriver.exe"
    parser = Parsing(driver_path)
    week = parser.load_main("https://animego.me/")
    for day in week:
        for anime in (week[day]):
            #print(anime)
            
            id = anime[0]
            name = anime[1]
            episod = anime[2]
            data = anime[3]
            href = anime[4]
            photo_path = anime[5]
            print(id,name, episod, data, href, photo_path, day)
