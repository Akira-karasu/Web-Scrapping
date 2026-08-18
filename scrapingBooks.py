import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

url = "http://books.toscrape.com/"

def html_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Success:", response.status_code)
        print("link:", response.url, "\n")
        soup = BeautifulSoup(response.text, "lxml")
        return soup
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")           
    except requests.exceptions.Timeout:
        print("Request timed out!")
    except requests.exceptions.ConnectionError:
        print("No internet / site unreachable")
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong: {e}")


def scrape_side_category_links(html_body):
    books_categories = {}

    div = html_body.find("div", class_="side_categories")

    a = div.find_all("a")

    for categories in a:
        category = categories.get_text(strip=True)
        link = categories.get("href") 
        books_categories[category] = url + link
    
    return books_categories


def scrape_category_books(html_body):

    del html_body["Books"]

    link_books = {}

    for categories, links in html_body.items():
        book_links = []

        category_page = html_request(links)

        article = category_page.find_all("article", class_="product_pod")

        for articles in article:
            book_list_link = articles.find_all("h3")

            for a in book_list_link:
                books = a.find("a")
                book_link = books.get("href").replace("../../..", "")
                book_links.append(url + 'catalogue' + book_link)
        
            link_books[categories] = book_links

    return link_books

def book_details(book_links):

    scrape_books_data = {}

    for category, links in book_links.items():

        list_books = []

        for link in links:
            book_details = {}
            product = html_request(link)
            
            product_gallery = product.find("div", id="product_gallery")

            book_img = product_gallery.find("img")
            img_src = url + book_img.get("src").replace('../../', '')

            product_title = product.find("div", class_="product_main")
            book_title = product_title.h1.text

            product_availability = product.find("p", class_="instock").text.strip()

            product_rating = product.find("p", class_="star-rating")
            rating = product_rating.get("class")[1]

            sub_header = product.find("div", class_="sub-header")

            if sub_header:
                description_tag = sub_header.find_next_sibling("p")
                product_description = description_tag.get_text(strip=True) if description_tag else "No description."
            else:
                product_description = "No description."

            table_product_info = product.find("table", class_="table")

            table_row = table_product_info.find_all("tr")

            upc_value = ""
            price_excl_value = ""
            price_incl_value = ""
            tax_value = ""
            num_review_value = ""

            for row in table_row:
                table_header = row.find("th").text
                table_data = row.find("td").text

                if table_header == "UPC":
                    upc_value = table_data
                elif table_header == "Price (excl. tax)":
                    price_excl_value = table_data
                elif table_header == "Price (incl. tax)":
                    price_incl_value = table_data
                elif table_header == "Tax":
                    tax_value = table_data
                elif table_header == "Number of reviews":
                    num_review_value = table_data

            book_details["book_title"] = book_title
            book_details["UPC"] = upc_value
            book_details["book_image"] = img_src
            book_details["price_excl"] = price_excl_value
            book_details["price_incl"] = price_incl_value
            book_details["tax"] = tax_value
            book_details["reviews"] = num_review_value
            book_details["instock"] = product_availability
            book_details["ratings"] = rating
            book_details["description"] = product_description


            print(f'Book_category: {category}')
            print(f'Book_title: {book_title}')
            print(f'UPC: {upc_value}')
            print(f'Book_image: {img_src}')
            print(f'Price_excl: {price_excl_value}')
            print(f'Price_incl: {price_incl_value}')
            print(f'Tax: {tax_value}')
            print(f'In-stock: {product_availability}')
            print(f'Reviews: {num_review_value}')
            print(f'Ratings: {rating}\n')
            print(f'Description: {product_description}')
            print(f'\n')

            list_books.append(book_details)
        
        scrape_books_data[category] = list_books
    
    for category, books in scrape_books_data.items():
        print(category, "->" , books, '\n')

    return scrape_books_data

def save_excel(data):
    wb = Workbook()
    default_sheet = wb.active 
    wb.remove(default_sheet)

    for category, list_books in data.items():
        ws_datasheet = wb.create_sheet(category)

        headers = [
            "Book Title",
            "UPC",
            "Book Image Url",
            "Price_excl",
            "Price_incl",
            "Tax",
            "In-stock",
            "Reviews",
            "Ratings",
            "Description"
        ]

        ws_datasheet.append(headers)

        for cell in ws_datasheet[1]: 
            cell.font = Font(bold=True)

        for books_data in list_books:
            ws_datasheet.append(
                [
                    books_data["book_title"],
                    books_data["UPC"],
                    books_data["book_image"],
                    books_data["price_excl"],
                    books_data["price_incl"],
                    books_data["tax"],
                    books_data["reviews"],
                    books_data["instock"],
                    books_data["ratings"],
                    books_data["description"]
                ]
            )
        

    ws_datasheet.freeze_panes = "A2"

    wb.save(r"C:\Users\LORD RAVEN ENRIQUE\OneDrive\Documents\Automation&Scripting\Web Scrapping Practice\scraped_books.xlsx")

    print("Excel file created successfully.")




request = html_request(url)

request_links = scrape_side_category_links(request)

category_book_links = scrape_category_books(request_links)

scraped_books = book_details(category_book_links)

save_excel(scraped_books)


