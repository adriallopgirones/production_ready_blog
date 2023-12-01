from locust import HttpUser, between, task


class LoadTestUser(HttpUser):
    """
    Class for load testing with locust, it sets two tasks:
        On start it gets the token for a test user
        - get_posts_list: GET request to /blog_posts/ endpoint
        - get_posts_detail: GET request to /blog_posts/2 endpoint
    """

    # Random wait time between requests
    wait_time = between(1, 5)

    def on_start(self):
        body = {
            "username": "adria",
            "password": "adria",
        }
        token = self.client.post(
            "http://localhost:8000/api/v1/api-token-auth/",
            body,
        )

        self.headers = {"Authorization": f"Token {token.json()['token']}"}

    @task
    def get_posts_list(self):
        self.client.get("/blog_posts/", headers=self.headers)

    @task
    def get_posts_detail(self):
        self.client.get("/blog_posts/2", headers=self.headers)
