import random


class UserAgentManager:
    def __init__(self):

        self.user_agents = [

            (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/149 Safari/537.36"
            ),


            (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/120 Safari/537.36"
            ),


            (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/605.1.15 "
                "Safari/605.1.15"
            ),


            (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "Firefox/121.0"
            )

        ]


    def get_user_agent(self):
        return random.choice(self.user_agents)