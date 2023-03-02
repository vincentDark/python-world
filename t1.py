import requests

url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

payload = "q=日出&target=en&source=zh-TW"
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"Accept-Encoding": "application/gzip",
	"X-RapidAPI-Key": "e894e35180msh01cb6a8a5abd710p117d81jsn3de236ec5bb7",
	"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)