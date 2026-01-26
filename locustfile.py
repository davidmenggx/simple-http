from locust import FastHttpUser, task

class GetUser(FastHttpUser):
    @task
    def make_get_request(self):
        url = '/'

        self.client.get(url)