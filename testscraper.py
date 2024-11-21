import asyncio
import tkinter as tk
from tkinter import *
import requests

def scrape(url: str) -> None:
    page = requests.get(url)
    print(page.text)

def Take_input(inputtxt):
    INPUT = inputtxt.get("1.0", "end-1c")
    print(INPUT)
    
def showUI():
    root = tk.Tk()
    root.geometry("800x200")
    root.title("PhilosoLinker")
    inputtxt = Text(root, height = 1, width = 60)
    button = Button(root, height = 2, width = 20, text="Crawl", command = lambda:Take_input(inputtxt))

    inputtxt.pack()
    button.pack()
    
    root.mainloop()
    
async def main():
    showUI()
    
    
if __name__ == "__main__":
    asyncio.run(main())