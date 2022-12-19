# -*- coding: utf-8 -*-
"""
    :description: A Python Script To Fetch The Government Securities Interest Rates From RBI Website.
    :license: MIT.
    :author: Dr June Moone
    :created: On Monday November 28, 2022 11:17:53 GMT+05:30
"""
__author__ = "Dr June Moone"
__webpage__ = "https://github.com/MooneDrJune"
__license__ = "MIT"

try:
    import json
    import requests
    import pandas as pd
    from selectolax.parser import HTMLParser
except (ImportError, ModuleNotFoundError):
    __import__("os").system(
        f"{__import__('sys').executable} -m pip install -U requests selectolax pandas json"
    )
    import json
    import requests
    from selectolax.parser import HTMLParser
    from typing import Tuple, List, Dict, Union

user_agent = requests.get(
    "https://techfanetechnologies.github.io/latest-user-agent/user_agents.json"
).json()[-2]

headers = {
    "user-agent": user_agent,
}
    
def riskFreeInetrestRate(
    url: str = "https://www.rbi.org.in/",
) -> None:
    response = HTMLParser(requests.get(url,headers=headers).content)
    selector = "#wrapper > div:nth-child(10) > table"
    data = [node.html for node in rbi.css(selector)]
    df = (pd.read_html(data[0])[0][4:13])
    df.columns = ["GovernmentSecurityName", "Percent"]
    df.reset_index(inplace=True,drop=True)
    df["GovernmentSecurityName"] = df["GovernmentSecurityName"].str.rstrip(' ').str.lstrip(' ')
    df["Percent"] = df["Percent"].str.rstrip('% #').str.rstrip('%*').str.lstrip(':  ')
    df = df.astype({'GovernmentSecurityName': 'str', 'Percent': 'float32'}, copy=False)
    with open("RiskFreeInetrestRate.json", "w") as jsonFile:
        jsonFile.write(df.to_json(orient='records'))

if __name__ == "__main__":
    riskFreeInetrestRate()
    
