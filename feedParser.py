import feedparser
import time

d = feedparser.parse('http://25livepub.collegenet.com/calendars/featured-events-calendar-1.rss')

print('Done');

count = 1
blockcount = 1
for post in d['entries']:
    if count % 5 == 1:
        print("\n" + time.strftime("%a, %b %d %I:%M %p") + ' ((( YU Cal - ' + str(blockcount) + ' )))')
        print("------------------------------------------------------\n")
        blockcount += 1
    print(post.title + "\n")
    print(post.summary + "\n")
    count += 1

