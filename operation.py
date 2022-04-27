import requests

class operation:
    def __init__(self):
        self.files = [
        ]
        self.headers = {
            'x-api-key': 'ca8eb275449c03fd1f5f',
            'userId': '1111',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'PostmanRuntime/7.29.0'
        }

    def get_runs(self, type, teamId, count):
        str1 = "https://www.notexponential.com/aip2pgaming/api/rl/score.php?type="
        str2 = "&teamId="
        str3 = "&count="
        total = str1, type, str2, teamId, str3, count

        url = ''.join(total)

        payload = {
        }

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        return response

    def get_location(self, type, teamId):
        str1 = "https://www.notexponential.com/aip2pgaming/api/rl/gw.php?type="
        str2 = "&teamId="
        total = str1, type, str2, teamId

        url = ''.join(total)

        payload = {
        }

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        return response

    def enter_a_world(self, teamId, type, worldId):
        url = "https://www.notexponential.com/aip2pgaming/api/rl/gw.php"

        payload = {'teamId': teamId,
                   'type': type,
                   'worldId': worldId}

        response = requests.request("POST", url, headers=self.headers, data=payload, files=self.files)
        return response

    def make_a_move(self, teamId, type, worldId, move):
        url = "https://www.notexponential.com/aip2pgaming/api/rl/gw.php"

        payload = {'move': move,
                   'teamId': teamId,
                   'type': type,
                   'worldId': worldId}

        response = requests.request("POST", url, headers=self.headers, data=payload, files=self.files)
        return response

    def get_score(self, type, teamId):
        str1 = "https://www.notexponential.com/aip2pgaming/api/rl/score.php?type="
        str2 = "&teamId="
        total = str1, type, str2, teamId

        url = ''.join(total)

        payload = {
        }

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        return response
