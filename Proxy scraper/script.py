import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import re
import random
from typing import Set, Tuple, List, Optional
import time

proxy_sources = [
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=2&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=3&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=4&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=5&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=6&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=7&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=8&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=9&sort_by=lastChecked&sort_type=desc",
    "https://geonode.com/free-proxy-list",
    "https://geonode.com/free-proxy-list?page=1",
    "https://geonode.com/free-proxy-list?page=2",
    "https://geonode.com/free-proxy-list?page=3",
    "https://proxylist.geonode.com/api/proxy-list?limit=1000",
    "https://proxylist.geonode.com/api/proxy-list?limit=1000&page=1",
    "https://proxylist.geonode.com/api/proxy-list?limit=1000&page=2",
    "https://proxyscrape.com/free-proxy-list",
    "https://proxyscrape.com/free-proxy-list/anonymous-proxy-list",
    "https://proxyscrape.com/free-proxy-list/elite-proxy-list",
    "https://proxyscrape.com/free-proxy-list/united-states",
    "https://proxyscrape.com/free-proxy-list/united-kingdom",
    "https://free-proxy-list.net/",
    "https://free-proxy-list.net/web-proxy.html",
    "https://free-proxy-list.net/uk-proxy.html",
    "https://free-proxy-list.net/anonymous-proxy.html",
    "https://www.sslproxies.org/",
    "https://www.us-proxy.org/",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://www.proxy-list.download/HTTP",
    "https://www.proxy-list.download/HTTPS",
    "https://www.proxy-list.download/SOCKS4",
    "https://www.proxy-list.download/SOCKS5",
    "https://www.proxynova.com/proxy-server-list/",
    "https://www.proxynova.com/proxy-server-list/country-us/",
    "https://www.proxynova.com/proxy-server-list/country-de/",
    "https://www.proxynova.com/proxy-server-list/country-fr/",
    "https://www.proxynova.com/proxy-server-list/country-ru/",
    "https://www.proxynova.com/proxy-server-list/country-in/",
    "https://www.proxynova.com/proxy-server-list/country-cn/",
    "https://www.proxynova.com/proxy-server-list/country-br/",
    "https://www.proxynova.com/proxy-server-list/elite-proxies/",
    "https://www.proxynova.com/proxy-server-list/anonymous-proxies/",
    "https://proxyelite.info/free-proxy-list/",
    "https://proxyelite.info/free-proxy-list-socks4/",
    "https://proxyelite.info/free-proxy-list-socks5/",
    "https://proxyelite.info/free-proxy-list-transparent/",
    "https://proxyelite.info/free-proxy-list-anonymous/",
    "https://proxyelite.info/free-proxy-list-elite/",
    "https://spys.one/en/",
    "https://spys.one/en/http-proxy-list/",
    "https://spys.one/en/https-ssl-proxy/",
    "https://spys.one/en/socks-proxy-list/",
    "https://spys.one/en/anonymous-proxy-list/",
    "https://proxifly.dev/",
    "https://proxifly.dev/proxies",
    "https://www.webshare.io/features/proxy-list",
    "https://hide.me/en/proxy-list/",
    "https://hide.me/en/proxy-list/?ac=1&start=0",
    "https://hide.me/en/proxy-list/?ac=1&start=50",
    "https://hide.me/en/proxy-list/?ac=1&start=100",
    "https://gimmeproxy.com/",
    "https://gimmeproxy.com/api/getProxy?protocol=http",
    "https://gimmeproxy.com/api/getProxy?protocol=https",
    "https://gimmeproxy.com/api/getProxy?protocol=socks5",
    "https://oxylabs.io/products/free-proxies",
    "https://www.freeproxylists.net/",
    "https://www.freeproxylists.net/?c=&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=0",
    "https://www.freeproxylists.net/?c=&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=50",
    "https://www.freeproxylists.net/?c=&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=100",
    "https://github.com/TheSpeedX/PROXY-List",
    "https://github.com/proxifly/free-proxy-list",
    "https://github.com/Flareonz44/free-proxy-list.net_API",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5.txt",
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
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks5.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/https.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=anonymous",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=5000&country=us",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=5000&country=us",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=2&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=3&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=speed&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=reliability&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&anonymityLevel=elite&sort_by=lastChecked&sort_type=desc",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&anonymityLevel=anonymous&sort_by=lastChecked&sort_type=desc",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://openproxy.space/list",
    "https://openproxy.space/list/http",
    "https://openproxy.space/list/socks4",
    "https://openproxy.space/list/socks5",
    "https://hidemy.name/en/proxy-list/",
    "https://hidemy.name/en/proxy-list/?maxtime=1000&type=h#list",
    "https://hidemy.name/en/proxy-list/?maxtime=1000&type=s#list",
    "https://hidemy.name/en/proxy-list/?maxtime=1000&type=4#list",
    "https://hidemy.name/en/proxy-list/?maxtime=1000&type=5#list",
    "https://hidemy.name/en/proxy-list/?start=64#list",
    "https://hidemy.name/en/proxy-list/?start=128#list",
    "https://vpnoverview.com/privacy/anonymous-browsing/free-proxy-servers/",
    "https://openproxylist.xyz/",
    "https://openproxylist.xyz/http.txt",
    "https://openproxylist.xyz/socks4.txt",
    "https://openproxylist.xyz/socks5.txt",
    "https://proxyhub.me/",
    "https://proxyhub.me/en/http-proxy-list.html",
    "https://proxyhub.me/en/all-proxy-list.html",
    "https://proxyhub.me/en/us-proxy-list.html",
    "https://proxydatabase.net/",
    "https://proxy-list.org/english/index.php",
    "https://proxy-list.org/english/index.php?p=1",
    "https://proxy-list.org/english/index.php?p=2",
    "https://proxy-list.org/english/index.php?p=3",
    "https://premproxy.com/proxy-list/",
    "https://premproxy.com/proxy-list/ip-port/1.htm",
    "https://premproxy.com/proxy-list/ip-port/2.htm",
    "https://premproxy.com/proxy-list/ip-port/3.htm",
    "https://premproxy.com/proxy-list/ip-port/4.htm",
    "https://premproxy.com/proxy-list/ip-port/5.htm",
    "https://www.proxydocker.com/en/proxylist/",
    "https://www.proxydocker.com/en/proxylist/type/http/",
    "https://www.proxydocker.com/en/proxylist/type/https/",
    "https://www.proxydocker.com/en/proxylist/type/socks4/",
    "https://www.proxydocker.com/en/proxylist/type/socks5/",
    "https://www.proxyrotator.com/free-proxy-list/",
    "https://spys.me/proxy.txt",
    "https://proxies.evozi.com/proxies.txt",
    "https://vpnturner.com/proxylist/",
    "https://www.proxyscan.io/",
    "https://www.proxyscan.io/api/proxy?last_check=3600&limit=100",
    "https://www.proxyscan.io/api/proxy?last_check=3600&limit=100&page=2",
    "https://www.proxyscan.io/api/proxy?last_check=3600&limit=100&page=3",
    "https://www.proxyscan.io/api/proxy?format=json&limit=1000",
    "https://www.proxyscan.io/api/proxy?format=txt&limit=1000",
    "https://www.proxyscan.io/api/proxy?level=elite&limit=100",
    "https://www.proxyscan.io/api/proxy?level=anonymous&limit=100",
    "https://www.proxyscan.io/api/proxy?type=http&limit=100",
    "https://www.proxyscan.io/api/proxy?type=https&limit=100",
    "https://www.proxyscan.io/api/proxy?type=socks4&limit=100",
    "https://www.proxyscan.io/api/proxy?type=socks5&limit=100",
    "https://www.xroxy.com/proxylist.htm",
    "https://www.xroxy.com/proxylist.htm?port=&type=All_http&ssl=&country=&latency=&reliability=",
    "https://www.xroxy.com/proxylist.htm?pnum=2",
    "https://www.xroxy.com/proxylist.htm?pnum=3",
    "https://www.ipaddress.com/proxy-list/",
    "https://www.sslproxies24.top/",
    "https://www.proxy-daily.com/",
    "https://proxysearcher.sourceforge.net/Proxy%20List.html",
    "https://checkerproxy.net/",
    "https://checkerproxy.net/api/archive/",
    "https://www.my-proxy.com/free-proxy-list.html",
    "https://www.my-proxy.com/free-proxy-list-2.html",
    "https://www.my-proxy.com/free-proxy-list-3.html",
    "https://www.my-proxy.com/free-proxy-list-4.html",
    "https://www.my-proxy.com/free-proxy-list-5.html",
    "https://www.my-proxy.com/free-proxy-list-6.html",
    "https://www.my-proxy.com/free-proxy-list-7.html",
    "https://www.my-proxy.com/free-proxy-list-8.html",
    "https://www.my-proxy.com/free-proxy-list-9.html",
    "https://www.my-proxy.com/free-proxy-list-10.html",
    "https://www.my-proxy.com/free-elite-proxy.html",
    "https://www.my-proxy.com/free-anonymous-proxy.html",
    "https://www.my-proxy.com/free-socks-4-proxy.html",
    "https://www.my-proxy.com/free-socks-5-proxy.html",
    "https://www.proxy-listen.de/",
    "https://www.proxz.com/",
    "https://www.proxz.com/proxy_list_high_anonymous_0.html",
    "https://www.proxz.com/proxy_list_anonymous_0.html",
    "https://www.proxz.com/proxy_list_transparent_0.html",
    "https://www.proxz.com/proxy_list_port_80_0.html",
    "https://www.proxz.com/proxy_list_port_8080_0.html",
    "https://www.proxz.com/proxy_list_port_3128_0.html",
    "https://www.proxz.com/region_proxy/United_States.html",
    "https://proxy50-50.blogspot.com/",
    "https://rootjazz.com/proxies/proxies.txt",
    "http://proxydb.net/",
    "http://proxydb.net/?protocol=http",
    "http://proxydb.net/?protocol=https",
    "http://proxydb.net/?protocol=socks4",
    "http://proxydb.net/?protocol=socks5",
    "http://proxydb.net/?protocol=http&anonlvl=4",
    "http://proxydb.net/?protocol=https&anonlvl=4",
    "https://hidester.com/proxylist/",
    "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
    "https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt",
    "https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/HTTP.txt",
    "https://raw.githubusercontent.com/proxiesmaster/free-proxy-list/main/proxies.txt",
    "https://raw.githubusercontent.com/geraldino2/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/geraldino2/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/geraldino2/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
    "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1",
    "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-2",
    "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-3",
    "https://list.proxylistplus.com/Socks-List-1",
    "https://list.proxylistplus.com/Socks-List-2",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=http",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=socks5",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=us&ssl=yes&anonymity=elite",
    "https://openproxy.me/list/http",
    "https://openproxy.me/list/socks4",
    "https://openproxy.me/list/socks5",
    "https://github.com/ertugrulturan/proxycrawler/raw/main/proxylist.txt",
    "https://github.com/jetkai/proxy-list/blob/main/archive/txt/proxies-http.txt",
    "https://github.com/jetkai/proxy-list/blob/main/archive/txt/proxies-https.txt",
    "https://github.com/jetkai/proxy-list/blob/main/archive/txt/proxies-socks4.txt",
    "https://github.com/jetkai/proxy-list/blob/main/archive/txt/proxies-socks5.txt",
    "https://anonymous-proxy-servers.net/proxy-list/",
    "https://anonymous-proxy-servers.net/proxy-list/free-proxy-list-1.html",
    "https://anonymous-proxy-servers.net/proxy-list/free-proxy-list-2.html",
    "https://anonymous-proxy-servers.net/proxy-list/free-proxy-list-3.html",
    "https://advanced.name/freeproxy/60fcc85145c7a",
    "https://advanced.name/freeproxy/60fcc85145c7a/1",
    "https://advanced.name/freeproxy/60fcc85145c7a/2",
    "https://advanced.name/freeproxy/60fcc85145c7a/3",
    "https://free-proxy-list.com/",
    "https://free-proxy-list.com/?page=2",
    "https://free-proxy-list.com/?page=3",
    "https://github.com/prxchk/proxy-list/blob/main/http.txt",
    "https://github.com/prxchk/proxy-list/blob/main/socks4.txt",
    "https://github.com/prxchk/proxy-list/blob/main/socks5.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/socks5.txt",
    "https://api.getproxylist.com/proxy",
    "https://proxylist.icu/",
    "https://proxylist.icu/api/",
    "https://github.com/zevtyardt/proxy-list/raw/main/http.txt",
    "https://github.com/zevtyardt/proxy-list/raw/main/socks4.txt",
    "https://github.com/zevtyardt/proxy-list/raw/main/socks5.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
    "https://proxy-spider.com/api/proxies.txt",
    "https://proxypremium.top/full-proxy-list",
    "https://www.proxyrss.com/proxylists/all",
    "https://api.smartproxy.com/free-proxy-list",
    "https://proxy-seller.com/free-proxy-list",
    "https://www.megalink.io/free-proxy-list",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "http://free-proxy.cz/en/proxylist/main/1",
    "http://free-proxy.cz/en/proxylist/main/2",
    "http://free-proxy.cz/en/proxylist/main/3",
    "http://free-proxy.cz/en/proxylist/main/4",
    "http://free-proxy.cz/en/proxylist/main/5",
    "https://www.proxydiscovery.com/api/proxies",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
    "https://proxylist.fatezero.org/proxy.list",
    "https://pubproxy.com/api/proxy?limit=5&format=txt",
    "https://pubproxy.com/api/proxy?limit=5&format=json",
    "https://www.httptunnel.ge/ProxyListForFree.aspx",
    "https://proxyranker.com/api/latest/json/http/1000",
    "https://proxyranker.com/api/latest/json/socks4/1000",
    "https://proxyranker.com/api/latest/json/socks5/1000",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/proxylist-to/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/MTProto/proxy-list/master/proxies.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/master/proxies/http.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/master/proxies/socks4.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4_proxies.txt",
    "https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5_proxies.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/https.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
    "https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt",
    "https://raw.githubusercontent.com/ImRaid/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ImRaid/Proxy-List/master/socks4.txt",
    "https://raw.githubusercontent.com/ImRaid/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/rohan-patra/ProxyListScraper/main/proxies/http_proxies.txt",
    "https://raw.githubusercontent.com/rohan-patra/ProxyListScraper/main/proxies/socks4_proxies.txt",
    "https://raw.githubusercontent.com/rohan-patra/ProxyListScraper/main/proxies/socks5_proxies.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/http.get",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/https.get",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/socks4.get",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/socks5.get",
    "https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/http.txt",
    "https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/https.txt",
    "https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/socks4.txt",
    "https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/socks5.txt",
    "https://api.openproxylist.xyz/http.txt",
    "https://api.openproxylist.xyz/socks4.txt",
    "https://api.openproxylist.xyz/socks5.txt",
    "https://best-proxies.ru/proxylist/free/1#",
    "https://best-proxies.ru/proxylist/free/2#",
    "https://best-proxies.ru/proxylist/free/3#",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/https.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
    "https://api.proxieslive.com/api?token=c622f805f31b50bd0f0976f26d24cba7df9cf154&country=all&anonymity=all&ssl=all&lastchecked=150",
    "https://api.good-proxies.ru/get.php?key=free&type=https&anon=elite&count=100",
    "https://api.good-proxies.ru/get.php?key=free&type=socks4&anon=elite&count=100",
    "https://api.good-proxies.ru/get.php?key=free&type=socks5&anon=elite&count=100",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/tahaluindo/free-proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/tahaluindo/free-proxies/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/tahaluindo/free-proxies/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/http.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/https.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks4.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks5.txt",
    "http://rootjazz.com/proxies/proxies.txt",
    "http://worm.rip/http.txt",
    "http://worm.rip/socks4.txt",
    "http://worm.rip/socks5.txt",
    "https://proxyspace.pro/http.txt",
    "https://proxyspace.pro/https.txt",
    "https://proxyspace.pro/socks4.txt",
    "https://proxyspace.pro/socks5.txt",
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&country=all&protocol=http&timeout=10000&proxy_format=ipport&format=text",
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&country=all&protocol=socks4&timeout=10000&proxy_format=ipport&format=text",
    "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&country=all&protocol=socks5&timeout=10000&proxy_format=ipport&format=text",
    "https://smartproxy.com/api/v1/http_proxies",
    "https://smartproxy.com/api/v1/socks4_proxies",
    "https://smartproxy.com/api/v1/socks5_proxies",
    "https://cyberdude.pro/api/http.txt",
    "https://cyberdude.pro/api/socks4.txt",
    "https://cyberdude.pro/api/socks5.txt",
    "https://cyberdude.pro/api/premium_http.txt",
    "https://cyberdude.pro/api/premium_socks4.txt",
    "https://cyberdude.pro/api/premium_socks5.txt",
    "https://raw.githubusercontent.com/user-tax-dev/free-proxy/main/data.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/zhaoyul/free-http-proxy/main/proxy.txt",
    "https://raw.githubusercontent.com/aslnkys/proxyshttpssocks45/main/https.txt",
    "https://raw.githubusercontent.com/aslnkys/proxyshttpssocks45/main/http.txt",
    "https://raw.githubusercontent.com/aslnkys/proxyshttpssocks45/main/socks4.txt",
    "https://raw.githubusercontent.com/aslnkys/proxyshttpssocks45/main/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/HTTP-Private-Proxy-List/master/proxy.txt",
    "https://raw.githubusercontent.com/sanuwaofficial/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/sanuwaofficial/proxy-list/master/socks4.txt", 
    "https://raw.githubusercontent.com/sanuwaofficial/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/http.txt",
    "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/https.txt", 
    "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/socks4.txt",
    "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/socks5.txt",
    "https://www.freeproxy.world/?type=http&anonymity=&country=&speed=&port=&page=1",
    "https://www.freeproxy.world/?type=http&anonymity=&country=&speed=&port=&page=2",
    "https://www.freeproxy.world/?type=http&anonymity=&country=&speed=&port=&page=3",
    "https://www.freeproxy.world/?type=https&anonymity=&country=&speed=&port=&page=1",
    "https://www.freeproxy.world/?type=https&anonymity=&country=&speed=&port=&page=2",
    "https://www.freeproxy.world/?type=socks4&anonymity=&country=&speed=&port=&page=1",
    "https://www.freeproxy.world/?type=socks5&anonymity=&country=&speed=&port=&page=1",
    "https://proxyservers.pro/proxy/list/order/updated/order_dir/desc",
    "https://proxyservers.pro/proxy/list/order/updated/order_dir/desc/page/2",
    "https://proxyservers.pro/proxy/list/order/updated/order_dir/desc/page/3",
    "https://raw.githubusercontent.com/Bardiafa/Proxy-Leecher/main/http.txt",
    "https://raw.githubusercontent.com/Bardiafa/Proxy-Leecher/main/socks4.txt",
    "https://raw.githubusercontent.com/Bardiafa/Proxy-Leecher/main/socks5.txt",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/http",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/https",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks4",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks5",
    "https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt",
    "https://raw.githubusercontent.com/proxy-spider/proxy-spider/main/proxies_anonymous/http.txt",
    "https://raw.githubusercontent.com/proxy-spider/proxy-spider/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/proxy-spider/proxy-spider/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/proxy-spider/proxy-spider/main/proxies_geolocation/http.txt",
    "https://raw.githubusercontent.com/proxy-spider/proxy-spider/main/proxies_geolocation/socks4.txt",
    "https://raw.githubusercontent.com/proxy-spider/proxy-spider/main/proxies_geolocation/socks5.txt",
    "https://raw.githubusercontent.com/proxy-spider/proxy-spider/main/proxies_residential/http.txt",
    "https://raw.githubusercontent.com/proxy-spider/proxy-spider/main/proxies_residential/socks4.txt",
    "https://raw.githubusercontent.com/proxy-spider/proxy-spider/main/proxies_residential/socks5.txt",
    "https://raw.githubusercontent.com/tuananh131001/ProxyLibrary/master/http.txt",
    "https://raw.githubusercontent.com/tuananh131001/ProxyLibrary/master/https.txt",
    "https://raw.githubusercontent.com/tuananh131001/ProxyLibrary/master/socks4.txt",
    "https://raw.githubusercontent.com/tuananh131001/ProxyLibrary/master/socks5.txt",
    "https://raw.githubusercontent.com/LION5HEART/public-proxy/main/HTTP-Rotating-Proxies.txt",
    "https://raw.githubusercontent.com/LION5HEART/public-proxy/main/HTTP-SSL-Proxies.txt",
    "https://raw.githubusercontent.com/LION5HEART/public-proxy/main/SOCKS4-Proxies.txt",
    "https://raw.githubusercontent.com/LION5HEART/public-proxy/main/SOCKS5-Proxies.txt",
    "https://raw.githubusercontent.com/ProxyListPro/ProxyListPro/main/proxylist_http.txt",
    "https://raw.githubusercontent.com/ProxyListPro/ProxyListPro/main/proxylist_http_premium.txt",
    "https://raw.githubusercontent.com/ProxyListPro/ProxyListPro/main/proxylist_socks4.txt",
    "https://raw.githubusercontent.com/ProxyListPro/ProxyListPro/main/proxylist_socks5.txt",
    "https://raw.githubusercontent.com/PerlaHosting/ProxyList/main/FREE_PROXY_LIST.txt",
    "https://best-proxies.ru/download/main/files/http.txt",
    "https://best-proxies.ru/download/main/files/https.txt",
    "https://best-proxies.ru/download/main/files/socks4.txt",
    "https://best-proxies.ru/download/main/files/socks5.txt",
    "https://fineproxy.de/wp-content/plugins/woo-shop-plugins/common-functions/gen_proxy.php",
    "https://openproxy.space/api/v1/free/http",
    "https://openproxy.space/api/v1/free/socks4",
    "https://openproxy.space/api/v1/free/socks5",
    "https://iparchive.co/freeproxy.html",
    "https://proxyserver.com/proxy-list/",
    "https://worldproxies.net/http-proxies",
    "https://worldproxies.net/https-proxies",
    "https://worldproxies.net/socks4-proxies",
    "https://worldproxies.net/socks5-proxies",
    "https://www.proxyrich.com/27-http-proxies",
    "https://www.proxyrich.com/39-socks4-proxies",
    "https://www.proxyrich.com/41-socks5-proxies",
    "https://raw.githubusercontent.com/KURO-CODE/DDoS-Attack/master/Lists/Proxies/Proxy_list.txt",
    "https://api.openproxy.space/lists/http",
    "https://api.openproxy.space/lists/socks4",
    "https://api.openproxy.space/lists/socks5",
    "https://github.com/UserR3X/proxy-list/raw/main/online/http.txt",
    "https://github.com/UserR3X/proxy-list/raw/main/online/https.txt",
    "https://github.com/UserR3X/proxy-list/raw/main/online/socks4.txt",
    "https://github.com/UserR3X/proxy-list/raw/main/online/socks5.txt",
    "https://github.com/hanwayTech/free-proxy-list/raw/main/http.txt",
    "https://github.com/hanwayTech/free-proxy-list/raw/main/https.txt",
    "https://github.com/hanwayTech/free-proxy-list/raw/main/socks4.txt",
    "https://github.com/hanwayTech/free-proxy-list/raw/main/socks5.txt",
    "https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/http.txt",
    "https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/socks4.txt",
    "https://raw.githubusercontent.com/TuanMinPay/live-proxy/master/socks5.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
    "https://api.proxiestorm.com/api/v1/getproxies?tier=public&proxytype=https",
    "https://api.proxiestorm.com/api/v1/getproxies?tier=public&proxytype=http",
    "https://api.proxiestorm.com/api/v1/getproxies?tier=public&proxytype=socks4",
    "https://api.proxiestorm.com/api/v1/getproxies?tier=public&proxytype=socks5",
    "https://www.live-socks.net/",
    "https://www.live-socks.net/2018/11/27-11-18-socks-5-servers-1732.html",
    "https://www.live-socks.net/2018/11/27-11-18-socks-5-servers_27.html",
    "https://raw.githubusercontent.com/dxxzst/free-proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/dxxzst/free-proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/dxxzst/free-proxy-list/main/http.txt",
    "https://github.com/xf555er/ProxyPool/raw/main/http.txt",
    "https://github.com/xf555er/ProxyPool/raw/main/socks4.txt",
    "https://github.com/xf555er/ProxyPool/raw/main/socks5.txt",
    "https://www.proxyserverlist24.top/",
    "https://github.com/smaicas/ProxyParser/raw/master/Proxies/Free_Proxy_List.txt",
    "https://getfreeproxylists.blogspot.com/"
]

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

        # GitHub raw content or plain text files
        if "raw.githubusercontent.com" in url or url.endswith(".txt"):
            for line in text.splitlines():
                line = line.strip()
                if re.match(r"^\d+\.\d+\.\d+\.\d+:\d+$", line):
                    ip, port = line.split(":")
                    proxies.add((ip, port, proxy_type))
        
        # Geonode
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
        
        #HTML table-based sources
        elif any(domain in url for domain in ["free-proxy-list.net", "sslproxies.org", "us-proxy.org", "proxynova.com"]):
            soup = BeautifulSoup(text, "html.parser")
            table = soup.find("table", {"id": "proxylisttable"}) or soup.find("table")
            if table:
                rows = table.find("tbody").find_all("tr") if table.find("tbody") else table.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        ip = cols[0].text.strip()
                        port = cols[1].text.strip()
                        proxies.add((ip, port, proxy_type))
        
        # Proxyscrape API
        elif "proxyscrape.com" in url or "api.proxyscrape.com" in url:
            for line in text.splitlines():
                line = line.strip()
                if re.match(r"^\d+\.\d+\.\d+\.\d+:\d+$", line):
                    ip, port = line.split(":")
                    proxies.add((ip, port, proxy_type))
        
        # Spys.one and similar sources with encoded IPs
        elif "spys.one" in url:
            soup = BeautifulSoup(text, "html.parser")
            scripts = soup.find_all("script")
            for script in scripts:
                if "document.write" in script.text:
                    encoded_ips = re.findall(r"document\.write\('(.*?)'\)", script.text)
                    for encoded_ip in encoded_ips:
                        decoded_ip = BeautifulSoup(encoded_ip, "html.parser").text
                        match = re.match(r"(\d+\.\d+\.\d+\.\d+):(\d+)", decoded_ip)
                        if match:
                            ip, port = match.groups()
                            proxies.add((ip, port, proxy_type))
        
        # General fallback for any text-based proxy list
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