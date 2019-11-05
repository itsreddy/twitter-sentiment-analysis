import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from dateutil import parser
import sys


#consumer key, consumer secret, access token, access secret.
ckey="dq8xpP2rogJOGWgq7dvFsUl0e"
csecret="5F7Cl7F1EVmJTNyc42elidOpbjWczGt9xsPszGO2AyobORvrrk"
atoken="2578033484-9aQGb7Z5BwTLwiYclI0qOTGABHGVrumu1dN6Ahe"
asecret="OiCSDGDyX3MXjSTTFVWa2zcxpiiO8T3q64m7lAAriLkny"

class listener(StreamListener):

    def on_data(self, data):
        #print(data)
        datajson = json.loads(data)
        text = datajson['text']
        username = datajson["user"]["screen_name"]
        tweet_id = datajson['id']
        created_at = parser.parse(datajson['created_at'])
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        #print(text.translate(non_bmp_map))
        with open('twitDB.json', 'a') as fp:
            json.dump(datajson, fp)
        #print (datajson)
        return(True)

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["MODI"])
