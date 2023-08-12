# This is a practice program that should scrape a github profile page to retrieve information about the user.

# Author: Alexander Kotzeff
# Date: Aug 12, 2023

import requests
from bs4 import BeautifulSoup


# This function takes in the username that the user has passed to get basic information.
def access_page(username):
    req = requests.get("https://github.com/" + username)

    code = req.status_code

    if code >= 400:
        print("You may be trying to access a page that does not exist. Please try again.")
    elif code != 200:
        print("There was an issue accessing this webpage. Please try again later.")
    else:
        print("The webpage was able to be accessed at: %s" % req.url)
        retrieve_info(req)


# This function should be able to parse the contents of the webpage using BeautifulSoup
def retrieve_info(req):
    soup = BeautifulSoup(req.content, 'html.parser')
    pages = soup.select('h1')
    print(pages)


if __name__ == '__main__':
    # uname = input("Please input the username of the GitHub account you would like to access: ")
    access_page('AlexKotzeff')
