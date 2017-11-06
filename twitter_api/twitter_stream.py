from Queue import Queue
from threading import Thread

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import settings
from s3_utils import s3_save


q = Queue()

# writer thread
def s3_writer():
    buff = []
    try:
        while True:
            item = q.get()
            buff.append(item.replace("\n"," "))
            q.task_done()
            if len(buff) > settings.s3_file_records:
                print("Write Stream to S3")
                s3_save("{prefix}_stream_{ts}.json".format(prefix= settings.s3_stream_path_prefix
                                                           , ts=time.time()),"[" + ",\n".join(buff) + "]" )
                buff = []
    except Exception:
        if len(buff) > 0:
            print("Exception, write Stream to S3")
            s3_save("{prefix}_stream_{ts}.json".format(prefix=settings.s3_stream_path_prefix,
                                                       ts=time.time()), "\n".join(buff))


def start_writers(number=1):
    threads = []
    for i in range(number):
        t = Thread(target=s3_writer)
        t.daemon = True
        t.start()
        threads.append(t)

    return threads

class QueueListener(StreamListener):
    def on_data(self, data):
        q.put(data)
        return True

    def on_error(self, status):
        print("Error: {}".format(status))

if __name__ == '__main__':
    l = QueueListener()
    auth = OAuthHandler(settings.consumer_key, settings.consumer_secret)
    auth.set_access_token(settings.access_token, settings.access_token_secret)
    stream = Stream(auth, l)
    print("Start loading data from stream...")
    writers = start_writers()
    stream.filter(track=settings.twitter_keywords, async=True)