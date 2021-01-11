from locust import HttpUser, task


class BookstoreLoadTest(HttpUser):
    host = "http://167.99.31.178:3000"
    min_wait = 5000
    max_wait = 9000

    # @task
    # def token_test(self):
    #     self.client.post("/token", dict(username="test", password="test"))

    @task
    def test_post_user(self):
        user_dict = {
            "name": "personel1",
            "password": "pass1",
            "role": "admin",
            "mail": "a@b.com"
        }
        auth_header = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyZGIiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE2MTA4MTQwNjN9.OC9yT7CzsU5ks05yTMjh_R_QOcMJcSJLCd0CY0iU6a4"}
        self.client.post("/v1/user", json=user_dict, headers=auth_header)