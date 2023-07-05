# reddit-app-v2-no-praw
The difference between version 1 (https://github.com/relixia/reddit-app) and this one is that it is forbidden to use the reddit praw library. Instead, async playwright is used via async version of flask named Quart to complete the web scraping process in a challenging way.

TR Hedef: Reddit içerisindeki subredditler’de paylaşılan postların anlık olarak takip edilmesini sağlayan bir Python servisi geliştirmek. İsterlerimiz şunlar: Login olunabilmesi. Crawl edilen postların database’de tutulması. Postların anlık takip edilmesi. Postların API tarafından servis edilmesi. Yazılan tüm kodun test edilmesi. Dockerize edilmesi

ENG Aim: Developing a Python service that provides instant tracking of posts on subreddits in Reddit. Requirements: login service, saving the crawled posts in an appropriate database. Instant tracking of the newly posted contents. Serving the posts via API calls. Testing. Dockerizing.

The user enters his Reddit credentials of username and password so that the login process can be completed. Then, the user can write the name of the subreddits that will be tracked. There is no lower or upper limit for the number of subreddits, and all of them will be tracked simultaneously. To see if the service is working properly without waiting for a new post in a subreddit, the last 10 posts of the subreddit also will be saved in the database. Then, the service checks in every 60 seconds to see if there is a new post or not. As the database, sqlite3 is used.

While the program is working, everything can be seen from the database easily. Here is an example run:
<img width="1470" alt="Ekran Resmi 2023-07-05 04 12 39" src="https://github.com/relixia/reddit-app-v2-no-praw/assets/77904399/657be891-1167-4403-9ebb-4fc982308859">

Here is the screenshot of http://127.0.0.1:5000/posts 
<img width="1470" alt="Ekran Resmi 2023-07-05 03 19 11" src="https://github.com/relixia/reddit-app-v2-no-praw/assets/77904399/9d6e4e7c-ab17-4a2d-a3e2-4c54187b2705">

