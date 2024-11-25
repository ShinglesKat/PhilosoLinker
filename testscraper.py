import asyncio
import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import *
import requests
import re


wikipedia_link_format = r"/wiki/[A-Za-z0.9_]+"
def scrape(url: str) -> None:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    #Find all links in website
    website_links = soup.find_all('a')
    wikipedia_links = []
    for link in website_links:
        href = link.get('href')
        if href and re.search(wikipedia_link_format, href):
            wikipedia_links.append(href)
        

    for link_to_check in wikipedia_links:
        print(link_to_check)

def paste_link(input_txt):
    input_txt.insert("1.0", "https://en.wikipedia.org/wiki/Old_School_RuneScape")
    
def take_input(input_txt):
    INPUT = input_txt.get("1.0", "end-1c")
    scrape(INPUT)
    print(INPUT)
    
def showUI():
    root = tk.Tk()
    root.geometry("800x200")
    root.title("PhilosoLinker")
    input_txt = Text(root, height = 1, width = 60)
    button = Button(root, height = 2, width = 20, text="Crawl", command = lambda:take_input(input_txt))
    paste_osrs_link = Button(root, height = 1, width = 10, text="Link", command = lambda:paste_link(input_txt))

    input_txt.pack()
    button.pack()
    paste_osrs_link.pack()
    
    root.mainloop()
    
async def main():
    showUI()
    
    
if __name__ == "__main__":
    asyncio.run(main())