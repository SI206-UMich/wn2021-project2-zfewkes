from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, filename)
    f = open(full_path)
    soup = BeautifulSoup(f, 'html.parser')
    anchor = soup.find_all('span', itemprop='name')
    anchor2 = []
    for i in range(len(anchor)):
        if (anchor[i].attrs.get('aria-level', 0) == '4'):
            anchor2.append((anchor[i].text.strip(), anchor[i + 1].text.strip()))

    f.close()
    return anchor2
    


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = 'https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    anchor = soup.find_all('a', class_='bookTitle')
    ret_list = []

    for i in range(10):
        ret_list.append('https://www.goodreads.com' + anchor[i].get('href', None).strip())
    
    return ret_list


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    #print(soup.find('h1', id = 'bookTitle').text)
    #print(soup.find('span', itemprop = 'author').text)
    #print(soup.find('span', itemprop = 'numberOfPages').text)
    
    ret_tuple = (soup.find('h1', id = 'bookTitle').text.strip(),
     soup.find('span', itemprop = 'name').text.strip().strip(' (Goodreads Author)'), 
     int(soup.find('span', itemprop = 'numberOfPages').text.strip().strip(' pages')))

    return ret_tuple
   





    


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """

    source_dir = os.path.dirname(__file__) #<-- directory name
    full_path = os.path.join(source_dir, filepath)
    f = open(full_path, encoding= 'utf8')
    soup = BeautifulSoup(f, 'html.parser')
    cat_list = soup.find_all('div', class_='category clearFix')
    
    ret_tup_list = []
    for item in cat_list:
        ret_tup_list.append((item.find('h4', class_= 'category__copy' ).text.strip(), 
        item.find('img').get('alt', None).strip(), 
        item.find('a').get('href', None).strip()))
    f.close()
    return ret_tup_list




    


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, filename), 'w', newline="")
    csv_writer = csv.writer(outFile, delimiter = ',', quotechar= '"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Book Title', 'Author Name'])
    for item in data:
        csv_writer.writerow([item[0].strip(), item[1].strip()])
    outFile.close()


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """

    #more test cases required
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()


    def test_get_titles_from_search_results(self):
        
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        title_tup_list = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(20, len(title_tup_list))
        # check that the variable you saved after calling the function is a list
        li = []
        self.assertEqual(type(title_tup_list), type(li))
        # check that each item in the list is a tuple
        tuple = ()
        for item in title_tup_list:
            self.assertEqual(type(tuple), type(item))
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'),
        title_tup_list[0])
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'),
        title_tup_list[19])
        


    def test_get_search_links(self):
        
        #links_list = get_search_links()
        # check that TestCases.search_urls is a list
        li = []
        self.assertEqual(type(TestCases.search_urls), type(li))
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(10, len(TestCases.search_urls))

        # check that each URL in the TestCases.search_urls is a string
        str = ''
        for item in TestCases.search_urls:
            self.assertEqual(type(item), type(str))

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for item in TestCases.search_urls:
            self.assertEqual(item[:36], 'https://www.goodreads.com/book/show/') 
        


    def test_get_book_summary(self):
        
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for item in TestCases.search_urls:
            summaries.append(get_book_summary(item))
            # check that each item in the list is a tuple
        tuple = ()
        for item in summaries:
            self.assertEqual(type(tuple), type(item))
            # check that each tuple has 3 elements
            self.assertEqual(3, len(item))
            # check that the first two elements in the tuple are string
            self.assertEqual(type(''), type(item[0]))
            self.assertEqual(type(''), type(item[1]))
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(int, type(item[2]))
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)
        
        

    def test_summarize_best_books(self):
        
        # call summarize_best_books and save it to a variable
        sum_best_books = summarize_best_books('best_books_2020.htm')
        # check that we have the right number of best books (20)
        self.assertEqual(20, len(sum_best_books))
        for item in sum_best_books:
            # assert each item in the list of best books is a tuple
            self.assertEqual(tuple, type(item))
            # check that each tuple has a length of 3
            self.assertEqual(3, len(item))
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(sum_best_books[0][0], 'Fiction')
        self.assertEqual(sum_best_books[0][1], 'The Midnight Library')
        self.assertEqual(sum_best_books[0][2], 'https://www.goodreads.com/choiceawards/best-fiction-books-2020')
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(sum_best_books[19][0], 'Picture Books')
        self.assertEqual(sum_best_books[19][1], 'Antiracist Baby')
        self.assertEqual(sum_best_books[19][2], 'https://www.goodreads.com/choiceawards/best-picture-books-2020')
        


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        title_list = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(title_list, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        dir = os.path.dirname(__file__)
        csv_cols = []
        with open(os.path.join(dir, 'test.csv')) as csv_file:
            csv_reader = csv.reader(csv_file)

            for col in csv_reader:
                csv_cols.append(col)
        
        # check that there are 21 lines in the csv
        self.assertEqual(21, len(csv_cols))

        # check that the header row is correct
        self.assertEqual(csv_cols[0][0], 'Book Title')
        self.assertEqual(csv_cols[0][1], 'Author Name')

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_cols[1][0], 'Harry Potter and the Deathly Hallows (Harry Potter, #7)')
        self.assertEqual(csv_cols[1][1], 'J.K. Rowling')

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_cols[20][0], 'Harry Potter: The Prequel (Harry Potter, #0.5)')
        self.assertEqual(csv_cols[20][1], 'J.K. Rowling')


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



