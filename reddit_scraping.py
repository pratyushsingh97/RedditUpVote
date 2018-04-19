from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import sys, traceback

class Reddit:
    def __init__(self):

        self.subreddits = []
        self.count = 0
        self.pageNumber = 1
        self.total = 1000

    def get_top_hundred_subs(self, url):
        '''
        This method gets the top 1000 subreddits by suscriber count. It stores
        the rank, name, and the number of suscribers for each subreddit. It calls
        http://redditlist.com/all?page=1 recursively until 1000 subreddits are scraped.
        Once the 1000 subreddits are scraped, it is stored in a CSV.
        '''
        try:
            URL = url
            r = requests.get(URL)
            popular_subreddits_html = r.text

            soup = BeautifulSoup(popular_subreddits_html, "lxml")
            popular_subreddits_suscribers = soup.find_all("div", {"class": "span4 listing"})[1]

            suscriber_divs = popular_subreddits_suscribers.find_all("div", {"class": "listing-item"})

            for div in suscriber_divs:
                rank_value = div.find("span", {"class": "rank-value"}).text

                subreddit_span = div.find("span", {"class": "subreddit-url"})
                subreddit_name = subreddit_span.find("a").text

                num_suscribers = div.find("span", {"class": "listing-stat"}).text
                num_suscribers = num_suscribers.replace(",", "")

                self.subreddits.append([rank_value, subreddit_name, num_suscribers])
                self.count = self.count + 1

            #go to next page
            if self.count < self.total:
                self.pageNumber = self.pageNumber + 1
                url = 'http://redditlist.com/all?page=' + str(self.pageNumber)
                self.get_top_hundred_subs(url)

            else:
                self.subreddits = np.asarray(self.subreddits)

                self.subreddits_df = pd.DataFrame(self.subreddits) #convert DataFrame
                self.subreddits_df = self.subreddits_df.rename(columns={0: "ranking", 1: "sub_name", 2: "suscriber_count"})
                self.subreddits_df.to_csv('reddit_data.csv', index=False)

                print(self.subreddits_df.head())



        except:
            print("Exception has occurred while parsing the website")
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)



def main():
    r = Reddit()
    r.get_top_hundred_subs('http://redditlist.com/all?page=1')

if __name__ == '__main__':
    main()
