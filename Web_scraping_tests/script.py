from bs4 import BeautifulSoup
import requests

url = requests.get("https://www.thesubath.com/bars/score/")
data = url.text
soup = BeautifulSoup(data, features='html.parser')

for i in soup.find_all():
    print (i)