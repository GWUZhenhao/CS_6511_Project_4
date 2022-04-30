import requests
import json

class operation:
    def __init__(self, teamId):
        self.files = [
        ]
        self.headers = {
            'x-api-key': 'ca8eb275449c03fd1f5f',
            'userId': '1111',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'PostmanRuntime/7.29.0'
        }
        self.teamId = teamId

    def get_my_team(self):
        url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=myTeams'
        payload = {}

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response

    def reset_my_team(self):
        url = 'https://www.notexponential.com/aip2pgaming/api/rl/reset.php?teamId={}&otp=5712768807'.format(self.teamId)
        payload = {}

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response


    def get_runs(self, count):
        url = 'https://www.notexponential.com/aip2pgaming/api/rl/score.php?type=runs&teamId={}&count={}'.format(self.teamId, count)
        payload = {}

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response

    def get_location(self):
        url = 'https://www.notexponential.com/aip2pgaming/api/rl/gw.php?type=location&teamId={}'.format(self.teamId)
        payload = {}

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response

    def enter_a_world(self, worldId):
        url = "https://www.notexponential.com/aip2pgaming/api/rl/gw.php"

        payload = {'teamId': self.teamId,
                   'type': 'enter',
                   'worldId': worldId}

        response = requests.request("POST", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response

    def make_a_move(self, worldId, move):
        url = "https://www.notexponential.com/aip2pgaming/api/rl/gw.php"

        payload = {'move': move,
                   'teamId': self.teamId,
                   'type': 'move',
                   'worldId': worldId}

        response = requests.request("POST", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response

    def get_score(self, type, teamId):
        str1 = "https://www.notexponential.com/aip2pgaming/api/rl/score.php?type="
        str2 = "&teamId="
        total = str1, type, str2, teamId

        url = ''.join(total)

        payload = {
        }

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        return response
