from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import random

def obtenir_golejadors_premier_league(any_inici, any_final, posicio, num_futbolistes):
    # Configuració del navegador en Selenium
    opcions = Options()
    opcions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, com Gecko) Chrome/115.0.0.0 Safari/537.36")
    
    # Inicialitzar el driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opcions)
    
    # Navegar a la pàgina d'estadístiques de la Premier League amb els paràmetres de temporada i posició
    url = f'https://www.transfermarkt.com/premier-league/ewigetorschuetzen/wettbewerb/GB1/plus//galerie/0?saisonIdVon={any_inici}&saisonIdBis={any_final}&tabellenart=alle&filterPosition={posicio}'
    driver.get(url)
    sleep(10)  # Espera perquè la pàgina carregui completament

    # Acceptar galetes
    try:
        boto_galetes = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), "Accept & continue")]'))
        )
        driver.execute_script("arguments[0].click();", boto_galetes)
        sleep(2)  # Espera per assegurar-se que les galetes s'han acceptat
    except Exception as e:
        print("No s'ha trobat el botó de galetes:", e)

    # Llistes per emmagatzemar estadístiques
    noms, gols, clubs, nacionalitats, minuts, aparicions, minuts_per_gol = [], [], [], [], [], [], []

    # Funció per extreure les dades d'una pàgina
    def extreure_dades(driver):
        noms, gols, clubs, nacionalitats, minuts, aparicions, minuts_per_gol = [], [], [], [], [], [], []
        try:
            jugadors = driver.find_elements(By.XPATH, '//table[contains(@class, "items")]/tbody/tr')
            for jugador in jugadors:
                try:
                    nom = jugador.find_element(By.XPATH, './/td[2]//a').text
                    gols_marcats = jugador.find_element(By.XPATH, './/td[8]').text
                    club = jugador.find_element(By.XPATH, './/td[4]//a').text
                    if not club:
                        club = " 1 Club"
                    nacionalitat = jugador.find_element(By.XPATH, './/td[3]//img').get_attribute('title')
                    minuts_jugats = jugador.find_element(By.XPATH, './/td[6]').text
                    aparicions_jugador = jugador.find_element(By.XPATH, './/td[5]').text
                    minuts_per_gol_jugador = jugador.find_element(By.XPATH, './/td[7]').text

                    noms.append(nom)
                    gols.append(gols_marcats)
                    clubs.append(club)
                    nacionalitats.append(nacionalitat)
                    minuts.append(minuts_jugats)
                    aparicions.append(aparicions_jugador)
                    minuts_per_gol.append(minuts_per_gol_jugador)
                except Exception as e:
                    print("Error al extreure informació d'un jugador:", e)
        except Exception as e:
            print("Error al trobar la taula de jugadors:", e)
        return noms, gols, clubs, nacionalitats, minuts, aparicions, minuts_per_gol
    
    # Extreure dades fins a arribar al nombre desitjat de jugadors
    while len(noms) < num_futbolistes:
        nous_noms, nous_gols, nous_clubs, noves_nacionalitats, nous_minuts, noves_aparicions, nous_minuts_per_gol = extreure_dades(driver)
        noms.extend(nous_noms)
        gols.extend(nous_gols)
        clubs.extend(nous_clubs)
        nacionalitats.extend(noves_nacionalitats)
        minuts.extend(nous_minuts)
        aparicions.extend(noves_aparicions)
        minuts_per_gol.extend(nous_minuts_per_gol)

        if len(noms) >= num_futbolistes:
            break

        # Navegar a la pàgina següent
        try:
            boto_seguent = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//li[@class="tm-pagination__list-item tm-pagination__list-item--icon-next-page"]/a'))
            )
            boto_seguent.click()
            sleep(random.uniform(3, 7))  # Espera aleatòria
        except Exception as e:
            print("No s'ha trobat el botó de pàgina següent o s'ha arribat al final:", e)
            break

    # Guardar els resultats en un fitxer CSV amb el nom que inclou els paràmetres
    nom_fitxer = f'golejadors_premier_league_{any_inici}_{any_final}_{posicio}_{num_futbolistes}.csv'
    with open(nom_fitxer, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Jugador', 'Gols', 'Club', 'Nacionalitat', 'Minuts jugats', 'Aparicions', 'Minuts per gol'])
        for i in range(len(noms[:num_futbolistes])):
            writer.writerow([noms[i], gols[i], clubs[i], nacionalitats[i], minuts[i], aparicions[i], minuts_per_gol[i]])
    
    print(f"Dades dels {num_futbolistes} primers jugadors guardades en '{nom_fitxer}'.")

    # Tancar el driver
    driver.quit()


