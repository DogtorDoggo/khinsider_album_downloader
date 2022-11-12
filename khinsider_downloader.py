import requests
from bs4 import BeautifulSoup
import os
import time
import urllib.parse

khinsider_base_url = "https://downloads.khinsider.com"

# modify these params, self-explanatory
chooseFlac = True
save_path = "E:\\b\\"
khinsider_album_url = "https://downloads.khinsider.com/game-soundtracks/album/bayonetta-2-original-soundtrack"

# for testing purposes only
test_song_url = "https://downloads.khinsider.com/game-soundtracks/album/bayonetta/1-01.%2520Opening%2520Demo.mp3"
test_download_url = "https://vgmsite.com/soundtracks/bayonetta/luxigxzobe/1-01.%20Opening%20Demo.flac"


def save_file(download_url, save_path):
    # create path if non-existent
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    last_slash_index = download_url.rfind("/")
    filename = urllib.parse.unquote(download_url[last_slash_index + 1:])
    print(f"Saving song: {filename} as {save_path + filename}:")
    with open(save_path + filename, 'wb') as out_file:
        content = requests.get(download_url, stream=True).content
        out_file.write(content)
    print(f"{filename} saved to {save_path + filename}.")


def download_song(song_url, chooseFlac):
    response_text = requests.get(song_url).text
    soup = BeautifulSoup(response_text, 'html.parser')
    download_url = ""
    for link in soup.find_all('a'):
        rel_url = link.get('href')
        if chooseFlac:
            if str(rel_url).endswith(".flac"):
                download_url = rel_url
        else:
            if str(rel_url).endswith(".mp3"):
                download_url = rel_url
    save_file(download_url, save_path)
    time.sleep(5)


def save_khinsider_album(album_url, chooseFlac):
    response_text = requests.get(khinsider_album_url).text
    download_urls = []
    soup = BeautifulSoup(response_text, 'html.parser')
    for link in soup.find_all('a'):
        rel_url = link.get('href')
        if str(rel_url).endswith(".mp3"):
            download_urls.append(khinsider_base_url + rel_url)

    # remove dupe
    download_urls = [*set(download_urls)]
    for url in download_urls:
        # print(url)
        download_song(url, chooseFlac)


if __name__ == "__main__":
    # print(khinsider_album_url)
    save_khinsider_album(khinsider_album_url, True)
    # download_song(test_song_url, True)
    # save_file(test_download_url, save_path)