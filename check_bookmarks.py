#!/usr/bin/env python3

from collections import namedtuple
import xml.etree.ElementTree as ET
import threading
import signal
import asyncio
import async_timeout
import aiohttp
import sys

Link = namedtuple('Link', "href title")
num_tasks = 0


async def fetch(session, link, timeout=None):
    global num_tasks
    status = -1
    #print('GET', link.href)
    try:
        with async_timeout.timeout(timeout):
            async with session.get(link.href, timeout=timeout) as resp:
                status = resp.status
                
    except ValueError:
        pass
    except (aiohttp.ServerTimeoutError, asyncio.TimeoutError):
        status = -2
        
    if status != 200:
        print((status, link.href, link.title))

    num_tasks -= 1
    print(num_tasks, 'left')


async def bound_fetch(sem, session, link, timeout=None):
    async with sem:
        await fetch(session, link, timeout)


async def fetch_all(links, loop):
    sem = asyncio.Semaphore(20)
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [bound_fetch(sem, session, link, 8) for link in links]
        await asyncio.wait(tasks)
    

def run_event_loop(loop, bookmarks_file):
    global num_tasks
    root = ET.parse(bookmarks_file).getroot()
    print('reading links file...')
    links = [Link(p.attrib['href'], p.attrib['description']) for p in root]
    print('reading finished.')
    num_tasks = len(links)
    loop.run_until_complete(fetch_all(links, loop))


loop = asyncio.get_event_loop()
sigint_called = False


def quit_program(signum, frame):
    print('Stopping loop...')
    asyncio.gather(*asyncio.Task.all_tasks()).cancel()    
    loop.stop()
    loop.close()
    sigint_called = True


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        sys.stderr.write('links file name arg. missing')
        sys.exit(1)

    signal.signal(signal.SIGINT, quit_program)
    t = threading.Thread(target=run_event_loop, args=(loop, args[1]))
    t.start()
    t.join()
    if sigint_called:
        sys.exit(1)

# def failing_links(links):
#     for link in links:
#         try:
#             r = requests.get(link.href, timeout=5, headers={'user-agent':'bot'})
#             if r.status_code != 200:
#                 yield (r.status_code, link.href, link.title)

#         except requests.exceptions.RequestException as e:
#             pass
    
# def failing_links_from_xml(links_data):
#     root = ET.fromstring(links_data)
#     links = (Link(p.attrib['href'], p.attrib['description']) for p in root)
#     sys.stdout.write(failing_links(links))

