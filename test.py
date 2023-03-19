from xAPIConnector import *

userId = 14473639
password = "xoh96725"

file = open("test.csv", "w")
# create & connect to RR socket
client = APIClient()

# connect to RR socket, login
loginResponse = client.execute(loginCommand(userId=userId, password=password))
logger.info(str(loginResponse))

# check if user logged in correctly
if not loginResponse['status']:
    print('Login failed. Error code: {0}'.format(loginResponse['errorCode']))
    exit(1)
else:
    print("zalogowane elo")

# get ssId from login response
ssid = loginResponse['streamSessionId']

now = int(time.time() * 1000)
year_ago = now - 365 * 24 * 60 * 60 * 1000 # 365 days ago
thirty = now - 30 * 24 * 60 * 60 * 1000 # 20 days ago
one_day = now - 24 * 60 * 60 * 1000 # 1 day in minutes

history = {
    "command": "getChartLastRequest",
    "arguments": {
        "info": {
            "period": 1, # 6 hours in minutes
            "start": thirty,
            "symbol": "ETHEREUM"
        }
    }
}
resp = client.execute(history)
for label in resp["returnData"]["rateInfos"][1]:
    if label != "ctmString":
        file.write(label)
        file.write(", ")

digits = resp["returnData"]["digits"]

file.write("\n")
print(len(resp["returnData"]["rateInfos"]))
for record in range(len(resp["returnData"]["rateInfos"])):
    for label in resp["returnData"]["rateInfos"][record]:
        if label != "ctmString":
            if label == "ctm" or label == "vol":
                file.write(str(resp["returnData"]["rateInfos"][record][label]))
            else:
                file.write(str(resp["returnData"]["rateInfos"][record][label] / (10 ** digits)))
            file.write(", ")
    file.write("\n")


#print(json.dumps(resp, indent=4))
client.disconnect()
file.close()