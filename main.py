import re
import sys
import time
import pyautogui as pyauto
from tkinter import Tk
from difflib import SequenceMatcher
import pyperclip


tk = Tk()

def search_song(song):
    """
    Recherche une chanson, filtre selon le format et dll le resultat si trouvé
    :param song:
    :return:
    """
    # focus l'input search et envoi la recherche
    pyperclip.copy(song)
    pyauto.click((53, 146))
    pyauto.hotkey("ctrl", "v")
    pyauto.press('enter')
    # focus l'input filter et envoi flac
    pyauto.click((933, 673))
    time.sleep(5)
    pyauto.typewrite("flac")
    time.sleep(2)
    # verifie si la recherche a retourné quelque chose
    dll = download_song(song)
    if not dll:
        # si pas de flac ou fichier non correspondant
        pyauto.click((933, 673), clicks=2)
        pyperclip.copy("mbr:320")
        pyauto.hotkey("ctrl", "v")
        time.sleep(4)
        download_song(song)

def download_song(song):
    """
    Clique sur le premier resultat, fait un ctrl+c et verifie si resultat match la recherche
    :param song:
    :return:
    """
    pyauto.click((395, 252))
    pyauto.hotkey("ctrl", "c")
    data = tk.clipboard_get()
    ratio = similar(data, song)
    print(ratio)
    if ratio >= 0.5:
        pyauto.click(button="right")
        pyauto.click((427, 271))
        return True

def similar(a, b):
    """
    Retourne le ratio de ressemble entre deux strings
    :param a:
    :param b:
    :return:
    """
    return SequenceMatcher(None, a, b).ratio()

if __name__ == "__main__":
    print('start')
    try:
        with open(sys.argv[1], "r") as f:
            text = f.read()
        pattern = "[\d]+:[\d]+\s:"
        # retire les timestamps
        splitted = re.split(pattern, text)
        # retire les tirets
        splitted = [x.replace("-", "") for x in splitted if len(x) > 1]
        # retire le texte entre parentheses
        splitted = [re.sub(r'\([^()]*\)', '', s) for s in splitted]
        pyauto.click((241, 77))
        for x in splitted:
            search_song(x)
    except FileNotFoundError:
        print("Fichier non trouvé")
        time.sleep(5)
