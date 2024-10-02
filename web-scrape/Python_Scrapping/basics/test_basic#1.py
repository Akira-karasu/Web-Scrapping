from bs4 import BeautifulSoup
import requests

def url_checker(url_req):
        if url_req.status_code >= 100 and url_req.status_code <= 199:
            return f"Informational Response: {url_req.status_code}"
        elif url_req.status_code >= 200 and url_req.status_code <= 299:
            return f"Successful Response: {url_req.status_code}"
        elif url_req.status_code >= 300 and url_req.status_code <= 399:
            return f"Client Error Responses: {url_req.status_code}"
        elif url_req.status_code >= 400 and url_req.status_code <= 499:
            return f"Server Error Responses: {url_req.status_code}"
        else:
            return "Invalid!"


def scrapping(url_req):
     
    soup = BeautifulSoup(url_req.text, "lxml")

    library = soup.find("div", class_="lib latest no-select")

    books = library.find_all("a")

    result = []

    for book in books:
         details = {}
         details["Author"] = book["authors"]
         details["Title"] = book["title"]
         result.append(details)
    

    # for r in result:
    #      print()
    #      for key in r:
    #           print(f"{key}: {r[key]}")

    return result
              
    


if __name__ == "__main__":

    url = "https://www.gutenberg.org"

    url_request = requests.get(url)

    print(url_checker(url_request))

    results = scrapping(url_request)

    val = 0

    print(f"Title: {results[val]['Title']}")
    print(f"Author: {results[val]['Author']}")

    
