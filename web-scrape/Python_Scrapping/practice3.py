from bs4 import BeautifulSoup
import requests 
import re


def Category_Books():

    Books_to_Scrape = requests.get('https://books.toscrape.com/').text

    soup = BeautifulSoup(Books_to_Scrape, 'lxml')

    side_categories = soup.find("div", class_="side_categories")

    title_book = side_categories.ul.li.a

    print("\n---------------- | SIDE CONTENT | ----------------\n")

    print(f'Books: {title_book['href']}')

    Book_Category = side_categories.ul.li.ul.find_all("a")

    print("\n------------------ | CATEGORIES | ------------------")

    print("\n")

    for books in Book_Category:
        print(f"Category: {books.text.strip()}")
        link = books["href"]
        numbers = re.findall(r'\d+', link)
        print(f"Number of Category: {numbers[0]}")
        print(f"links: {link}\n")
        

    print("\n-----------------------------------------------------")
    try:
        category = input("Insert category: ").lower().replace(" ", "-")
        num_category = input("Insert Number of Category: ")


        print("\n")

        category_page = requests.get(f'https://books.toscrape.com/catalogue/category/books/{category}_{num_category}/index.html').text
        soup = BeautifulSoup(category_page, 'lxml')

        page = soup.find("div", class_="page")
        if not page:
            raise ValueError("Page div with class 'page' not found.")

        section = page.find("section")
        if not section:
            raise ValueError("Section within the page div not found.")
        
        articles = section.find_all("article")
        for article in articles:
            title = article.h3.a["title"]

            price_content = article.find("div", class_="product_price")

            price = price_content.find("p", class_="price_color").text

            stock = price_content.find("p", class_="instock availability").text

            ratings = article.find("p", class_="star-rating").get("class")

            book_link = article.find("div", class_="image_container")

            link = book_link.a['href']

            after = link.partition("_")

            number = re.findall(r'\d+', after[2])

            print("Title: ", title)
            print("Book No. : ", number[0])
            print("Link: ", link)
            print("Price: ", price)
            print("Stock: ", stock.strip())
            print("Star-Ratings: ", ratings[1], "\n")
            
    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred with the network request: {e}")
    except ValueError as e:
        print(f"\nAn error occurred while parsing the HTML: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


    print("\n")

# Category_Books()


def Available_Books(page):
    try:
        Books_to_Scrape = requests.get(f'https://books.toscrape.com/catalogue/page-{page}.html').text

        soup = BeautifulSoup(Books_to_Scrape, 'lxml')

        side_categories = soup.find("ol", class_="row")

        cards = side_categories.find_all("article", class_="product_pod")
        if not cards:
            raise ValueError("aarticle div with class 'product_pod' not found.")

        for card in cards:
            title = card.h3.a["title"]

            price_content = card.find("div", class_="product_price")

            price = price_content.find("p", class_="price_color").text

            stock = price_content.find("p", class_="instock availability").text

            ratings = card.find("p", class_="star-rating").get("class")

            book_link = card.find("div", class_="image_container")

            link = book_link.a['href']

            after = link.partition("_")

            number = re.findall(r'\d+', after[2])

            print("Title: ", title)
            print("BookNo. : ", number[0])
            print("Link : ", link)
            print("Price: ", price)
            print("Stock: ", stock.strip())
            print("Star-Ratings: ", ratings[1], "\n")
    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred with the network request: {e}")
    except ValueError as e:
        print(f"\nAn error occurred while parsing the HTML: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    print("\n")

# Available_Books(2)

def book(Bk_name, Bk_no):

    print("\n")

    try:
        Books_to_Scrape = requests.get(f'https://books.toscrape.com/catalogue/{Bk_name}_{Bk_no}/index.html').text

        soup = BeautifulSoup(Books_to_Scrape, 'lxml')

        article = soup.find("article", class_="product_page")

        product_main = article.find("div", class_="product_main")

        Book_title = product_main.find("h1").text

        price = product_main.find("p", class_="price_color").text

        stock = product_main.find("p", class_="instock availability").text

        star_rating = product_main.find("p", class_="star-rating").get("class")

        print(f"Book Title: {Book_title}")
        print(f"Price: {price}")
        print(f"Stock: {stock.strip()}")
        print(f"star_rating: {star_rating[1]}\n")

        product_description = article.h2.text

        paragraph = article.find("p")

        description = paragraph.find_next("p").find_next("p").find_next("p").text

        print(product_description)
        print(f"-{description}\n")

        product_description = article.find_next("h2").find_next("h2").text

        table = article.find("table", class_="table table-striped")

        table_row = table.find_all("tr")

        
        print(product_description)

        for rows in table_row:
            th = rows.find("th").text
            td = rows.find("td").text

            print(f"{th}: {td}")
    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred with the network request: {e}")
    except ValueError as e:
        print(f"\nAn error occurred while parsing the HTML: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    
    print("\n")

# book(Bk_name = "a-light-in-the-attic", Bk_no = 1000)

def book_scraper():

    while True:
        print("\nHello there, Welcome to Books to scrape, we love being scrape <3")
        print("Choose what you want to be scrapped\n")
        print("Book Categories           [BC]")
        print("Book Available            [BA]")
        print("Book Description          [BD]\n")
        print("Exit                      [EX]\n")

        prompt  = input("> ").upper()

        if  prompt ==  "BC":
            Category_Books()
        elif prompt == "BA":
            print("\nChoose page 1-50 only")
            prompt  = int(input("> "))
            if prompt >= 50:
                print("Your input is  invalid, please input again")
            else:
                Available_Books(prompt)
        elif prompt == "BD":
            print("what book do you want to search?")
            bk_name = input("BookName: ").lower().replace(" ","-").replace(",", "").replace("(", "").replace(")", "").replace("!", "").replace("@", "").replace("#", "").replace(".", "").replace(":", "").replace("+", "").replace("", "")
            bk_no = input("BookNumber: ")
            book(bk_name, bk_no)
        elif prompt ==  "EX":
            break
        else:
            print("Invalid Input, please try again")

book_scraper()






