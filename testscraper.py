import tkinter
import requests

#UI
top = tkinter.Tk()





def scrape(url: str) -> None:
    page = requests.get(url)
    print(page.text)

async def main():
    print("test")
    
    
    
if __name__ == "__main__":
    asyncio.run(main())