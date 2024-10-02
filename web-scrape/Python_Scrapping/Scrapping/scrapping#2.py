import csv
from bs4 import BeautifulSoup
import requests
import os

def scrape(url):
    """Fetch the HTML content of the webpage."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve page. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error during requests to {url} : {str(e)}")
        return None

def csv_extractor(data, folder_path):
    """Extracts data from the webpage and stores or updates it in a CSV file inside a specified folder."""
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Path for the CSV file
    file_path = os.path.join(folder_path, "Hockey_teams_data.csv")

    # Check if the file exists
    file_exists = os.path.isfile(file_path)
    
    existing_data = []
    if file_exists:
        # Read existing data to avoid duplication
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_data.append(row)
    
    # Filter out any duplicate entries
    new_entries = [entry for entry in data if entry not in existing_data]

    # Write new data (append if file exists)
    with open(file_path, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames = data[0].keys() if data else [])
        
        # Write header only if the file is being created
        if not file_exists:
            writer.writeheader()
        
        # Write only new entries
        for entry in new_entries:
            writer.writerow(entry)
    
    print(f"Data saved to {file_path}")

def parser(html_page):
    """Parse the HTML content using BeautifulSoup and extract relevant data."""
    all_data_countries_of_the_world = []
    all_data_Hockey_Teams = []

    def content_pages(con_page):
        data = []
        soup = BeautifulSoup(con_page, 'html.parser')
        div = soup.find_all("div", class_="page")

        for x in div:
            link = "https://www.scrapethissite.com" + x.a["href"]
            data.append(link)
        
        return data

    content = content_pages(html_page)

    def countries_of_the_world(con_page1):
        result = []
        res = scrape(con_page1)
        soup = BeautifulSoup(res, 'html.parser')
        country = soup.find_all("div", class_="country")
        for x in country:
            details = {}
            country_name = x.h3.text.strip()
            country_info = x.find("div", class_="country-info")
            country_capital = country_info.find("span", class_="country-capital")
            country_population = country_info.find("span", class_="country-population")
            country_area = country_info.find("span", class_="country-area")
            strong_elem = country_info.find_all("strong")
            
            # Prepare the dictionary with scraped details
            details["country_name"] = country_name.upper()
            details[strong_elem[0].text.replace(":", "")] = country_capital.text.upper()
            details[strong_elem[1].text.replace(":", "")] = country_population.text
            details[strong_elem[2].text.replace(":", "")] = country_area.text
            
            result.append(details)
        return result

    # Scrape and parse the countries from the first link
    countries_data = countries_of_the_world(content[0])

    # Save data to CSV
    csv_extractor(countries_data, "scrape_data_csv")

    all_data_countries_of_the_world.append(countries_data)

    def Hockey_Teams(con_page2):
        per_page = {}
        pagination_link = []

        res = scrape(con_page2)
        soup = BeautifulSoup(res, 'html.parser')

        selector = soup.find("select", class_="form-control")

        option = selector.find_all("option")

        for x in option:
            per_page[x.text] = f"https://www.scrapethissite.com/pages/forms/?per_page={x.text}"
        
        user_input = input("Enter how many per page do want, you only have (25, 50, 100): ")

        page = scrape(per_page[user_input])
        soup = BeautifulSoup(page, 'html.parser')

        pagination = soup.find("ul", class_="pagination")

        li = pagination.find_all("li")
        
        for x in li:
            pagination_link.append("https://www.scrapethissite.com"+ x.find("a").get("href"))
        
        def parsing_pagination(pagi_parse_link):
            result = []

            for x in pagi_parse_link:
                pagi_page = scrape(x)
                soup = BeautifulSoup(pagi_page, 'html.parser')

                table = soup.find("table")


                table_row = table.find_all("tr", class_="team")

                for tbl_row in table_row:

                    data = {}

                    tbl_data_name = tbl_row.find("td", class_="name").text
                    tbl_data_year = tbl_row.find("td", class_="year").text
                    tbl_data_win = tbl_row.find("td", class_="wins").text
                    tbl_data_losses = tbl_row.find("td", class_="losses").text
                    tbl_data_otlosses = tbl_row.find("td", class_="ot-losses").text
                    tbl_data_pct = tbl_row.find("td", class_="pct").text
                    tbl_data_gf = tbl_row.find("td", class_="gf").text
                    tbl_data_ga = tbl_row.find("td", class_="ga").text
                    tbl_data_diff = tbl_row.find("td", class_="diff").text

                    table_header = table.find_all("th")

                    data[table_header[0].text.strip()] = tbl_data_name.strip().replace("\n", "")
                    data[table_header[1].text.strip()] = tbl_data_year.strip().replace("\n", "")
                    data[table_header[2].text.strip()] = tbl_data_win.strip().replace("\n", "")
                    data[table_header[3].text.strip()] = tbl_data_losses.strip().replace("\n", "")
                    data[table_header[4].text.strip()] = tbl_data_otlosses.strip().replace("\n", "")
                    data[table_header[5].text.strip()] = tbl_data_pct.strip().replace("\n", "")
                    data[table_header[6].text.strip()] = tbl_data_gf.strip().replace("\n", "")
                    data[table_header[7].text.strip()] = tbl_data_ga.strip().replace("\n", "")
                    data[table_header[8].text.strip()] = tbl_data_diff.strip().replace("\n", "")

                    result.append(data)

            return result

        
        hockey_team_records = parsing_pagination(pagination_link)

        return hockey_team_records
        
        
    Hockey_Teams_data = Hockey_Teams(content[1])

    csv_extractor(Hockey_Teams_data, "scrape_data_csv")

    all_data_Hockey_Teams.append(Hockey_Teams_data)

    return all_data_Hockey_Teams





def output(result):
    """Output the parsed data in a readable format."""
    def extract(data):
        # Extract headers
        headers = data[0].keys()

        # Dynamically calculate column widths based on the longest entry in each column
        column_widths = {}
        for key in headers:
            # Find the maximum length between the header and the longest data entry for that column
            max_data_length = max(len(str(row[key])) for row in data)
            column_widths[key] = max(len(key), max_data_length) + 2  # Adding 2 for padding

        # Print the table headers with proper alignment
        header_row = " | ".join(key.ljust(column_widths[key]) for key in headers)
        print(header_row)
        print("-" * len(header_row))

        # Print each row with proper alignment
        for row in data:
            print(" | ".join(str(row[key]).ljust(column_widths[key]) for key in headers))
            print("-" * len(header_row))

    extract(result[0])


def main():
    url = "https://www.scrapethissite.com/pages/"
    html_page = scrape(url)
    if html_page:
        result = parser(html_page)
        output(result)

if __name__ == "__main__":
    main()
