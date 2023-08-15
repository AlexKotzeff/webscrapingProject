# This is a practice program that uses a webscraping sandbox called "books.toscrape.com". This program is to both
# refresh my coding skills in python and to learn about webscraping. While I could check the robots.txt for an actual
# website, I do not want to risk taking down their site. This also avoids any ethical or legal issues that I do not
# have to knowledge to navigate yet.

# This code uses the requests library to access the web and then the BeautifulSoup package to read the information.

# Author: Alexander Kotzeff
# Date: Aug 12, 2023

import requests
from bs4 import BeautifulSoup


def run_scrape():
    start_url = "http://books.toscrape.com/catalogue/page-1.html"

    # Create a csv file to save all the books to.
    file = "Books.csv"
    f = open(file, "w")
    headers = "Book title, Link\n"
    f.write(headers)

    # Since there are multiple pages containing the books, we will need to use a pointer named "this_page" to extract
    # all the information from the given page and add that info to the csv.
    this_page = start_url
    next_page = True
    while next_page:
        req = requests.get(this_page)
        soup = BeautifulSoup(req.content, "html.parser")
        booklinks = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

        for links in booklinks:
            # Using the html of the site, we can get the href so that each book can be inspected individually if needed.
            book_title = links.h3.a["title"]
            book_link = links.h3.a["href"]
            f.write("\"" + book_title + "\"" + ", http://books.toscrape.com/catalogue/" + book_link + "\n")

        # Check if there is a next button in the page meaning that we need to continue scraping.
        next_button = soup.find("li", {"class": "next"})
        if next_button is not None:
            this_page = "http://books.toscrape.com/catalogue/" + next_button.a["href"]
            print(this_page)
            next_page = True
        else:
            next_page = False

    f.close()



if __name__ == '__main__':
    run_again = input("Would you like to run the scrape again? (Yes/No): ")

    if run_again is "Yes":
        run_scrape()


