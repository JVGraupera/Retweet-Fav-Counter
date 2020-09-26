#------------------------------------
# Program Name: Rt and Fav counter bot
# Author: James Graupera
# Use: A twitter bot that programmatically counts the number of retweets and favorites
# a twitter has received on their tweets and returns those numbers in a status.
#------------------------------------
import tweepy
import time

consumer_key = 'XXXX'
consumer_secret = 'XXXX'
access_token = 'XXXX'
access_token_secret = 'XXXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
key_phrase = "how many rts and favs have i received"

#Gets the id of the last tweet seen
def get_last_id():
    f_read = open("last_id.txt", 'r')
    last_id = int(f_read.read().strip())
    f_read.close()
    return last_id;

#Stores the id of the last tweet seen
def set_last_id(last_id):
    f_write = open("last_id.txt", 'w')
    f_write.write(str(last_id))
    f_write.close()
    return;

#Reads mentions and searches for the key phrase
def read_mentions():
    last_id = get_last_id()
    for status in reversed(api.mentions_timeline(last_id)):
        text = status.text.lower()
        id = status.id
        name = "@" + status.user.screen_name
        print("%d- %s"%(id, text))
        if key_phrase in text:
            count = get_fav_rt_count(name)
            api.update_status("%s Your authored tweets have recieved %d rts and %d fav"%(name, count[1], count[0]), id)
        last_id = id
    set_last_id(last_id)
    time.sleep(30)
    read_mentions()

#Scrolls through the users tweet page counting the number of likes and retweets on their tweets
def get_fav_rt_count(user_name):
    fav_count = 0
    rt_count = 0
    for status in tweepy.Cursor(api.user_timeline, include_rts = False, screen_name = user_name).items():
        fav_count += status._json["favorite_count"]
        rt_count += status._json["retweet_count"]
    return [fav_count, rt_count];

#The entry point for the program
def main():
    read_mentions()

if __name__ == "__main__":
    main()
