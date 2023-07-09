import asyncio
import threading
from quart import Quart, render_template_string
from quart.wrappers import Response
from playwright.async_api import async_playwright
from getpass import getpass
from models import Base, Post
from database import engine, Session

app = Quart(__name__)
Base.metadata.create_all(bind=engine)


@app.route('/posts')
async def index():
    try:
        session = Session()
        posts = session.query(Post).all()
        session.close()

        template = """
        <html>
        <head>
            <title>Reddit Posts</title>
        </head>
        <body>
            <h1>Reddit Posts</h1>
            <ul>
            {% for post in posts %}
                <li>
                    <a href="{{ post.url }}" target="_blank">{{ post.title }}</a>
                    <span>by {{ post.author }}</span>
                </li>
            {% endfor %}
            </ul>
        </body>
        </html>
        """

        rendered_template = await render_template_string(template, posts=posts)
        response = Response(rendered_template, mimetype='text/html')

        return response

    except Exception as e:
        return f"An error occurred: {str(e)}"


async def login_to_reddit(page, username, password):
    while True:
        await page.goto('https://www.reddit.com/login')

        # Fill in the login form
        await page.fill('input[name="username"]', username)
        await page.fill('input[name="password"]', password)

        await page.click('button[type="submit"]')

        print("Logging in...")

        try:
            # Wait for the login success element
            success_element = await page.wait_for_selector('#USER_DROPDOWN_ID', timeout=50000)
            if success_element:
                print("Successfully logged in to Reddit!")
                break
            else:
                print("Login failed. Please try again.")
                username = input("Enter your Reddit username: ")
                password = getpass("Enter your Reddit password: ")

        except Exception as e:
            print("Login failed. Please try again.")
            username = input("Enter your Reddit username: ")
            password = getpass("Enter your Reddit password: ")


async def get_subreddit_post_text(page):
    # Retrieve post titles
    post_title_elements = await page.query_selector_all('div.Post div > h3')
    titles = [await post_title_element.inner_text() for post_title_element in post_title_elements]

    # Retrieve usernames
    username_elements = await page.query_selector_all('a[data-testid="post_author_link"]')
    usernames = [await username_element.inner_text() for username_element in username_elements]

    # Retrieve post URLs
    url_elements = await page.query_selector_all('a[data-click-id="body"]')
    urls = [f"https://www.reddit.com{await url_element.get_attribute('href')}" for url_element in url_elements]

    # Create a session
    session = Session()

    # Store each post in the database
    for title, author, url in zip(titles, usernames, urls):
        # Check if the post already exists in the database
        post = session.query(Post).filter_by(url=url).first()
        if not post:
            post = Post(title=title, author=author, url=url)
            session.add(post)
            print(f"Post stored: {title} by {author}, URL: {url}")
        else:
            print(f"Post already exists: {title} by {author}")

    # Commit the session to persist the changes in the database
    session.commit()

    # Close the session
    session.close()


async def retrieve_data_for_subreddits(subreddits):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()

        username = input("Enter your Reddit username: ")
        password = getpass("Enter your Reddit password: ")

        page = await context.new_page()

        # Login to Reddit
        await login_to_reddit(page, username, password)

        while True:
            for subreddit in subreddits:
                url = f"https://www.reddit.com/r/{subreddit}/new"
                await page.goto(url, timeout=200000000)

                await get_subreddit_post_text(page)
                print(f"Data retrieved for subreddit: {subreddit}\n")

                # Delay for 5 seconds before going to the next subreddit
                await asyncio.sleep(5)

            # Delay for 1 minute before checking for new posts
            await asyncio.sleep(60)

        await page.close()
        await context.close()
        await browser.close()


def run_quart_app():
    # Run the Quart application
    app.run()


if __name__ == '__main__':
    # Ask the user for the subreddits
    subreddits = input("Enter the subreddits you want to retrieve data for (comma-separated): ").split(",")
    subreddits = [subreddit.strip() for subreddit in subreddits]

    # Start the data retrieval process in a separate thread
    retrieval_thread = threading.Thread(target=asyncio.run, args=(retrieve_data_for_subreddits(subreddits),))
    retrieval_thread.start()

    # Start the Quart application in the main thread
    run_quart_app()
