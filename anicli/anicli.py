# coding:utf-8
import click
import os
import json
import re
os.environ["PATH"] = os.path.dirname(__file__) + os.pathsep + os.environ["PATH"]
import mpv
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

base_url = 'http://mavanimes.cc'
headers = {"x-requested-with": "XMLHttpRequest"}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKYELLOW = '\033[93m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    FAIT = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'


def openAnime(anime_url):
    # Settings options
    options = ChromeOptions()
    options.add_argument('log-level=3')  # show fatal log
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])  # disable devtool warn
    options.headless = True

    driver = Chrome(options=options)
    driver.get(base_url + anime_url)

    print(f'{bcolors.OKGREEN}[+] Searching the url...{bcolors.END}')

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, 'btn-robot'))).click()

    iframes = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe')))
    for iframe in iframes:
        url = re.search('^https?:\/\/.*fembed.*\/v\/(.*)$',
                        iframe.get_attribute('src'))
        if url:
            id = url.group(1)
            break
    print(f"{bcolors.OKGREEN}[+] URL fetched{bcolors.END}")

    if id:
        driver.quit()
        # print('[!] Send request (%s)' % id[:50])

        with requests.post('https://fembed-hd.com/api/source/'+id, headers=headers) as r:
            response = json.loads(r.text)

        print(
            f"{bcolors.OKGREEN}[+] Server response successfully, opening media plyer...{bcolors.END}")

        # TODO : VLC
        # Instance = vlc.Instance()
        # player = Instance.media_player_new()
        # Media = Instance.media_new(response['data'][-1]['file'])
        # Media.get_mrl()
        # player.set_media(Media)
        # player.play()

        player = mpv.MPV(
            loglevel='no',
            script_opts='title="TEST - TITLE",force-media-title="TEST - TITLE"',
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True)
        player.play(response['data'][-1]['file'])
        os.system('cls' if os.name == 'nt' else 'clear')
        player.wait_for_playback()


def reqAnimeList(anime):
    r = requests.get(base_url + '/tous-les-animes-en-vostfr')

    animeList = re.findall(
        f"^<a href=\"(.*)\">({''.join([f'(?:{i}).*' for i in anime.split(' ')])})</a>$", r.text, flags=re.I+re.M)

    if r.status_code != 200 or animeList == []:
        return False
    else:
        return animeList


def episode_exist(id, episodes):
    if id == 'l' or id == 'list':
        print(
            f"{bcolors.OKBLUE}Episode {[x['id'] for x in episodes]}{bcolors.END}")
        return False
    elif id.replace('.', '', 1).isdigit():
        id = int(id) if id.isdigit() else float(id)
        for episode in episodes:
            if episode['id'] == id:
                return episode['url']
    return False


def episode_list(anime):
    r = requests.get(base_url + anime)
    soup = BeautifulSoup(r.text, 'html.parser')
    tempEpisodes = list(map(lambda x: x.a.get('href'),
                        soup.find_all('article', 'episode')))

    episodes = []
    count = {'i': 0, 'f': 0}
    for episode in tempEpisodes:
        regex = re.search(
            r'(-([0-9.]+-[0-9])-)vostfr|(-([0-9.]+)-)vostfr', episode)
        if regex.group(2) is not None:
            episodes.append(
                {'id': float(regex.group(2).replace('-', '.')), 'url': episode})
            count['f'] += 1
        else:
            id = int(regex.group(4))
            episodes.append({'id': id, 'url': episode})
            if id > count['i']: count['i'] = id

    episodes.sort(key=lambda x: x['id'], reverse=True)

    print(
        f"{bcolors.HEADER + bcolors.BOLD}Veuillez choisir l'épisode (1-{count['i']} / {count['f']} filler)\nlist/l pour les afficher{bcolors.END}")
    url = episode_exist(input(f'{bcolors.OKCYAN}>>> {bcolors.END}'), episodes)
    while url is False:
        url = episode_exist(
            input(f'{bcolors.OKCYAN}>>> {bcolors.END}'), episodes)

    return url


def anime_list(animes):
    print(f"{bcolors.HEADER + bcolors.BOLD}Veuillez choisir l'anime (>> 0){bcolors.END}")
    for i, anime in enumerate(animes):
        print(
            f"{bcolors.ITALIC}{bcolors.OKGREEN if i % 2 == 0 else bcolors.OKYELLOW} {i} - {anime[1]}{bcolors.END}")

    id = int(input(f'{bcolors.OKCYAN}>> {bcolors.END}'))
    while id < 0 or id > len(animes):
        id = int(input(f'{bcolors.OKCYAN}>> {bcolors.END}'))

    return (f'/{animes[id][0]}')


def menu():
    print(f"{bcolors.HEADER + bcolors.BOLD}Veuillez rentrer le titre{bcolors.END}")
    animes = reqAnimeList(input(f'{bcolors.OKCYAN}> {bcolors.END}'))
    while animes is False:
        print(
            f"{bcolors.HEADER}Anime introuvable, veuillez ressayer avec un autre titre.")
        animes = reqAnimeList(input(f'{bcolors.OKCYAN}> {bcolors.END}'))

    return animes

@click.command()
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    animes = menu()
    os.system('cls' if os.name == 'nt' else 'clear')
    animeUrl = anime_list(animes)
    os.system('cls' if os.name == 'nt' else 'clear')
    episodeUrl = episode_list(animeUrl)
    os.system('cls' if os.name == 'nt' else 'clear')
    openAnime(episodeUrl)


if __name__ == '__main__':
    main()
