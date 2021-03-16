import requests
from bs4 import BeautifulSoup
import json
import sys

# this class is responsible for fetching top movies info from given base url

class MovieScrapper():
    def __init__(self, base_url, item_count):
        self.base_url = base_url
        self.item_count = item_count
        self.top_movies_slug = []

    def fetch_top_movies_link(self):
        page = requests.get(self.base_url)
        beautiful_soup = BeautifulSoup(page.content, features='lxml')
        movie_table = beautiful_soup.find('tbody', class_ = 'lister-list')
        movies = movie_table.find_all('tr')

        for index, movie in enumerate(movies):
            if(index < int(self.item_count)):
                title_col = movie.find('td', class_ = 'titleColumn')
                movie_link = title_col.find('a', href = True)['href']

                #storing movie links in array as all info not present on listing page
                self.top_movies_slug.append(movie_link)

    def fetch_top_movies_info(self):
        result = []
        for slug in self.top_movies_slug:
            page = requests.get('https://www.imdb.com/' + slug)
            beautiful_soup = BeautifulSoup(page.content, features='lxml')

            # extracting title related info from title_wrappr
            title_wrapper = beautiful_soup.find("div", class_="title_wrapper")
            title_text = title_wrapper.find("h1").text.strip()
            movie_title = title_text.split('(')[0].strip()
            release_year = title_text.split('(')[1][:-1]


            # extracting genre, duration info from sub_text
            genre = ''
            sub_text = title_wrapper.find("div", class_="subtext")
            duration = sub_text.find("time").text.strip()
            genre_tags = sub_text.find_all("a", text=True)
            for genre_tag in genre_tags[:-1]:
                genre += genre_tag.text.strip() + ' '
            genre = genre.rstrip()
            genre = genre.replace(" ", ", ")


            imdb_rating = beautiful_soup.find("span", itemprop="ratingValue").text.strip()
            summary = beautiful_soup.find("div", class_="summary_text").text.strip()

            result.append({
                'title': movie_title,
                'movie_release_year': release_year,
                'imdb_rating': imdb_rating,
                'summary': summary,
                'duration': duration,
                'genre': genre
            })

        return json.dumps(result)



if __name__ == "__main__":
    base_url = sys.argv[1]
    item_count = sys.argv[2]
    movie_scrapper = MovieScrapper(base_url, item_count)

    try:
        movie_scrapper.fetch_top_movies_link()
    except:
        print("Unable to get fetch movie link")

    try:
        print(movie_scrapper.fetch_top_movies_info())
    except:
        print("Unable to fetch movies information")


