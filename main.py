from bs4 import BeautifulSoup
import requests
import smtplib

my_email = "james.standlee.testing@gmail.com"
my_password = "dgnyflwwvmtiaard"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

sheet = requests.get("https://api.sheety.co/f8724e1153f9bdc8a257690deeb690bc/untitledSpreadsheet/price").json()
price_sheet = sheet["price"]

for entries in price_sheet:
    try:
        response = requests.get(url=entries["url"], headers=headers)
    except:
        pass
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        price = soup.find(name="span", class_="a-price-whole").text
        item_name = soup.find(name="span", id="productTitle").text
        num_price = int(price.replace(".", ""))
        minimum_price = int(entries["price"])
        if minimum_price >= num_price:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs=entries["email"],
                                    msg=f"Subject: Amazon Price Alert! \n\n{item_name} is now ${num_price}\n"
                                        f"{entries['url']}")
                connection.close()