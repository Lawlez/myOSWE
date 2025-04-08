import re
import time

USER_AGENT_DEVICES = (
    (re.compile("Windows Mobile"), "Windows Mobile"),
    (re.compile("Android"), "Android"),
    (re.compile("Linux"), "Linux"),
    (re.compile("iPhone"), "iPhone"),
    (re.compile("iPad"), "iPad"),
    (re.compile("Mac OS"), "Mac"),
    (re.compile("NT"), "Windows"),
    (re.compile("Windows"), "Windows"),
)


def user_agent_humanize(value):

    browser = "None"

    device = None
    for regex, name in USER_AGENT_DEVICES:
        if regex.search(value):
            device = name
            break

    if browser and device:
        return "browser on devices" % {"browser": browser, "device": device}

    if browser:
        return browser

    if device:
        return device

    return None

normal_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
start = time.time()
print(user_agent_humanize(normal_agent))
print("Time taken: ", time.time() - start)

user_agent = "Windows    " + " " * 100_000_000 + "x  NT"
start = time.time()
print(user_agent_humanize(user_agent))
print("Time taken: ", time.time() - start)

