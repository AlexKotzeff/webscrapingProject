# This is a practice program that uses a webscraping sandbox called "books.toscrape.com". This program is to both
# refresh my coding skills in python and to learn about webscraping. While I could check the robots.txt for an actual
# website, I do not want to risk taking down their site. This also avoids any ethical or legal issues that I do not
# have the knowledge to navigate yet.

# This code uses the requests library to access the web and then the BeautifulSoup package to read the information.

# Author: Alexander Kotzeff
# Date: Aug 12, 2023

import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup


# This function moves through the catalogue of books to gather all the book titles and the link to access more
# information about them
def run_catalogue_scrape():
    start_url = "http://books.toscrape.com/catalogue/page-1.html"

    # Create a csv file to save all the books to.
    file = "Books.csv"
    f = open(file, "w")
    headers = "Book title,Link\n"
    f.write(headers)

    # Since there are multiple pages containing the books, we will need to use a pointer named "this_page" to extract
    # all the information from the given page and add that info to the csv.
    this_page = start_url
    next_page = True
    while next_page:
        req = requests.get(this_page)
        soup = BeautifulSoup(req.content, "html.parser")
        allbooks = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

        for book in allbooks:
            # Using the html of the site, we can get the href so that each book can be inspected individually if needed.
            book_title = book.h3.a["title"]
            book_link = book.h3.a["href"]
            f.write("\"" + book_title + "\"" + ", http://books.toscrape.com/catalogue/" + book_link + "\n")

        # Check if there is a next button in the page meaning that we need to continue scraping.
        next_button = soup.find("li", {"class": "next"})
        if next_button is not None:
            this_page = "http://books.toscrape.com/catalogue/" + next_button.a["href"]
            next_page = True
        else:
            next_page = False
    f.close()


def run_book_scrape(book, word):
    url = book["Link"].values[0]
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")

    description = soup.find_all('p')[3].get_text().strip()
    return description.count(word)



# This function moves through the csv of books to try and find what the user is looking for. It uses the pandas library
# for speed and simplicity.
def find_in_csv(book_to_find):
    df = pd.read_csv("Books.csv")
    found = df[df["Book title"].str.contains(book_to_find, case=False)]

    return found


def user_book_input():
    book_name = input("\nPlease enter the name of the book you would like to search for: ")

    found = find_in_csv(book_name)
    count = found.shape[0]

    if count == 0:
        print("\nNo books with that name were found in the catalogue. Please try again")
        user_book_input()
    elif count > 1:
        print("\nSeveral books matching that name were found.")
        for title in found["Book title"]:
            print(title)
        user_book_input()
    else:
        print("\nThe book was found in the catalogue!\n")

    return found


if __name__ == '__main__':
    # Check if the user wants to refresh the scrape since last time.
    run_again = input("Would you like to run the scrape again? (Yes/No): ")
    if run_again.casefold() == "yes":
        run_catalogue_scrape()

    # Get the book from the user and check if it is in the catalogue
    book_info = user_book_input()

    keyword = input("Please enter the word you would like to search for in the description of the book: ")

    word_count = run_book_scrape(book_info, keyword)

    print(f"\nThe word \"{keyword}\" was found {word_count} times in the product description.")
