import requests 
from bs4 import BeautifulSoup
import os

#Checking the response from the website and scraping or fetching the data
def get_url():
    url = "https://dcsa.puchd.ac.in/show-noticeboard.php?nbid=1"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,features="html.parser")
        with open("main.html","w",encoding="utf-8") as file:
            file.write(str(soup.prettify()))
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

get_url()

#Creating a folder to store the downloaded files
folder_name = 'pdf'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

#Creating a HTML file to store the source code of the website
with open("main.html","r",encoding="utf-8") as file:
    data = file.read()

soup = BeautifulSoup(data,"html.parser")


#Iterating through all the Links present in the html
for i in soup.find_all("a"):
    if(i.parent.name=="td"):
        pdf_name = i.get("href")[-5::] #Storing the ID/name of the file
        try:
            response = requests.get("https://dcsa.puchd.ac.in/"+ i.get("href"))
            if response.status_code == 200:
                url_soup = BeautifulSoup(response.text,features="html.parser")

                for j in url_soup.find_all("a",href=True):
                    if (".pdf" in j.get("href")):
                        print(j.get("href"))

                        #Downloading the file
                        try:
                            data=requests.get("https://dcsa.puchd.ac.in/"+j.get("href"))
                            break
                        except Exception as e:
                            print("Could not download the file")
                with open("pdf/"+pdf_name+".pdf","wb") as file:
                    file.write(data.content)
            else:
                print(f"Failed to retrieve the page. Status code: {response.status_code}")
        except Exception as e:
            print(e)
    