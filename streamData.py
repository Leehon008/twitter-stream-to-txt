#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
#credentials.py
consumer_key = 'UyoJGgBlRy8VcNdzJ0s16OyOl'
consumer_secret = '23odkMbHhpoOdjstS56LmVn1XnPRt3kZa5ay6ihQmyAoaDSXk7'
access_token = '4133498632-TziR44yO8UvXpvZUNnsIWq0KkuSHh238hWj0vPj'
access_token_secret = 'wT0U4valS7ljBk3lpAPVcuaP3oKsukhBQ6Flc2Q0rdHh4'

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['ZimWildlife', 'ZimParks', 'ZimbabweWildlife','Zim Tourism'])