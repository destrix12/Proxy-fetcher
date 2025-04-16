import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import re
import random
from typing import Set, Tuple, List, Optional
import time

proxy_sources = [
    "https://geonode.com/free-proxy-list",
    "https://proxyscrape.com/free-proxy-list",
    "https://free-proxy-list.net/",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://www.proxynova.com/proxy-server-list/",
    "https://proxyelite.info/free-proxy-list/",
    "https://spys.one/en/",
    "https://proxifly.dev/",
    "https://www.webshare.io/features/proxy-list",
    "https://hide.me/en/proxy-list/",
    "https://gimmeproxy.com/",
    "https://oxylabs.io/products/free-proxies",
    "https://www.proxy-list.download/",
    "https://free-proxy-list.net/web-proxy.html",
    "https://proxyscrape.com/free-proxy-list/united-states",
    "https://github.com/TheSpeedX/PROXY-List",
    "https://github.com/proxifly/free-proxy-list",
    "https://github.com/Flareonz44/free-proxy-list.net_API",
    "https://proxylist.geonode.com/api/proxy-list",
    "https://www.freeproxylists.net/",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
    "https://www.sslproxies.org/",
    "https://www.us-proxy.org/",
    "https://free-proxy-list.net/uk-proxy.html",
    "https://free-proxy-list.net/anonymous-proxy.html",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://openproxy.space/list",
    "https://hidemy.name/en/proxy-list/",
    "https://vpnoverview.com/privacy/anonymous-browsing/free-proxy-servers/",
    "https://openproxylist.xyz/",
    "https://proxyhub.me/",
    "https://proxydatabase.net/",
    "https://proxy-list.org/english/index.php",
    "https://premproxy.com/proxy-list/",
    "https://www.proxydocker.com/en/proxylist/",
    "https://www.proxyrotator.com/free-proxy-list/",
    "https://spys.me/proxy.txt",
    "https://proxies.evozi.com/proxies.txt",
    "https://vpnturner.com/proxylist/",
]#all free proxy sources I could find

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
]

def detect_proxy_type(url: str) -> str:
    if "socks5" in url.lower():
        return "socks5"
    elif "socks4" in url.lower():
        return "socks4"
    elif "https" in url.lower():
        return "https"
    else:
        return "http"

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    try:
        async with session.get(url, headers=headers, timeout=15) as resp:
            if resp.status == 200:
                return await resp.text()
            else:
                return ""
    except Exception:
        return ""

async def fetch_proxies_from_url(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, url: str) -> Set[Tuple[str, str, str]]:
    async with semaphore:
        proxy_type = detect_proxy_type(url)
        proxies = set()
        
        text = await fetch(session, url)
        if not text:
            return proxies

        #github raw content or plain text files
        if "raw.githubusercontent.com" in url or url.endswith(".txt"):
            for line in text.splitlines():
                line = line.strip()
                if re.match(r"^\d+\.\d+\.\d+\.\d+:\d+$", line):
                    ip, port = line.split(":")
                    proxies.add((ip, port, proxy_type))
        
        #geonode
        elif "proxylist.geonode.com/api" in url:
            try:
                data = json.loads(text)
                if "data" in data:
                    for proxy in data["data"]:
                        ip = proxy.get("ip")
                        port = str(proxy.get("port"))
                        if ip and port:
                            proxies.add((ip, port, proxy_type))
            except json.JSONDecodeError:
                pass
        
        #freeproxylist net and similar
        elif any(domain in url for domain in ["free-proxy-list.net", "sslproxies.org", "us-proxy.org"]):
            soup = BeautifulSoup(text, "html.parser")
            table = soup.find("table", {"id": "proxylisttable"})
            if table:
                rows = table.find("tbody").find_all("tr") if table.find("tbody") else []
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        ip = cols[0].text.strip()
                        port = cols[1].text.strip()
                        proxies.add((ip, port, proxy_type))
        
        #any text file
        if not proxies:
            pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[^\d]?:(\d{2,5})'
            matches = re.findall(pattern, text)
            for ip, port in matches:
                if 0 <= int(port) <= 65535:
                    proxies.add((ip, port, proxy_type))

        if proxies:
            print(f"Found {len(proxies)} proxies from {url}")
        return proxies

async def check_proxy_access(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, 
                            proxy_data: Tuple[str, str, str], target_url: str, 
                            result_list: List, counter: List) -> None:
    ip, port, proxy_type = proxy_data
    proxy_url = f"{proxy_type}://{ip}:{port}"
    
    async with semaphore:
        try:
            async with session.get(target_url, proxy=proxy_url, timeout=8) as resp:
                if resp.status == 200:
                    print(f"{ip}:{port} ({proxy_type})")
                    result_list.append(proxy_data)
        except:
            pass
        finally:
            counter[0] += 1
            if counter[0] % 100 == 0:
                print(f"Progress: {counter[0]}/{counter[1]} proxies checked. Found {len(result_list)} working.")

async def main():
    print("~~~~~destrix's proxy scraper~~~~~")
    
    target_url = input("Enter target URL (for example google.com) or leave blank for all proxies: ").strip()
    if target_url is None or target_url == "":
        target_url = ""
    elif not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    
    connector = aiohttp.TCPConnector(limit=None, ssl=False)
    timeout = aiohttp.ClientTimeout(total=60)
    
    start_time = time.time()
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        print(f"Fetching proxies from {len(proxy_sources)} sources...")
        
        fetch_semaphore = asyncio.Semaphore(25)
        
        fetch_tasks = [
            fetch_proxies_from_url(session, fetch_semaphore, url) 
            for url in proxy_sources
        ]
        results = await asyncio.gather(*fetch_tasks)
        
        all_proxies = set()
        for proxy_set in results:
            all_proxies.update(proxy_set)
        
        fetch_time = time.time() - start_time
        
        if not all_proxies:
            print("No proxies found. Exiting.")
            return
            
        print(f"Got {len(all_proxies)} unique proxies in {fetch_time:.2f} seconds")
        
        if target_url is None or target_url == "":
            working_proxies = list(all_proxies)
            working_proxies.sort(key=lambda x: x[2])
            
            #json format
            with open("working_proxies.json", "w") as f:
                json.dump(
                    [{
                        "ip": ip, 
                        "port": port, 
                        "type": ptype, 
                        "url": f"{ptype}://{ip}:{port}"
                    } for ip, port, ptype in working_proxies],
                    f,
                    indent=4
                )
            
            #also save as txt
            with open("working_proxies.txt", "w") as f:
                for ip, port, ptype in working_proxies:
                    f.write(f"{ptype}://{ip}:{port}\n")
            total_time = time.time() - start_time
            print(f"Saved results to working_proxies.json and working_proxies.txt")
            print(f"Total time: {total_time:.2f} seconds")
            return

        print(f"Checking which proxies can reach: {target_url}")
        
        check_semaphore = asyncio.Semaphore(1000) #1000 max at one time (its enough imo)
        
        working_proxies = []
        counter = [0, len(all_proxies)]
        
        check_tasks = [
            check_proxy_access(session, check_semaphore, proxy_data, target_url, working_proxies, counter)
            for proxy_data in all_proxies
        ]
        await asyncio.gather(*check_tasks)
        total_time = time.time() - start_time
        
        if working_proxies:
            working_proxies.sort(key=lambda x: x[2])
            
            #json format
            with open("working_proxies.json", "w") as f:
                json.dump(
                    [{
                        "ip": ip, 
                        "port": port, 
                        "type": ptype, 
                        "url": f"{ptype}://{ip}:{port}"
                    } for ip, port, ptype in working_proxies],
                    f,
                    indent=4
                )
            
            #also save as txt
            with open("working_proxies.txt", "w") as f:
                for ip, port, ptype in working_proxies:
                    f.write(f"{ptype}://{ip}:{port}\n")
            
            print(f"\nFound {len(working_proxies)} working proxies out of {len(all_proxies)} total")
            print(f"Saved results to working_proxies.json and working_proxies.txt")
            print(f"Total time: {total_time:.2f} seconds")
        else:
            print(f"\nNo working proxies found that can access {target_url} after checking {len(all_proxies)} proxies.")
            print(f"Total time: {total_time:.2f} seconds")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")