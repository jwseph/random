# pip install requests beautifulsoup4 Pillow lxml

import requests
from bs4 import BeautifulSoup
import json
import random
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

class SchoologySession(requests.Session):
    def __init__(self, email: str, password: str):
        super().__init__()
        schoology_resp = requests.get('https://mukilteo.schoology.com/')
        schoology_soup = BeautifulSoup(schoology_resp.content, features='lxml')
        login_resp = requests.post('https://sts.mukilteo.wednet.edu'+schoology_soup.find('form', {'id': 'loginForm'})['action'], {'UserName': email, 'Password': password})
        login_soup = BeautifulSoup(login_resp.content, features='lxml')
        try:
            login_soup_SAMLResponse = login_soup.find('form').find('input', {'name': 'SAMLResponse'})['value']
        except TypeError:
            raise ValueError(
                'Incorrect user ID or password\n'
                'Maybe you forgot the @mukilteo.wednet.edu?'
            )
        receive_resp = self.post('https://mukilteo.schoology.com/login/saml/receive', {'SAMLResponse': login_soup_SAMLResponse})
        receive_soup = BeautifulSoup(receive_resp.content, features='lxml')
        user_data = json.loads(receive_soup.select_one('#body > script').text.removeprefix('window.siteNavigationUiProps='))['props']['user']
        self.uid = str(user_data['uid'])

    def get_soup(self, url: str):
        r = self.get(url)
        while not r.ok: #  r.status_code == 429:
            r = self.get(url)
            if r.status_code != 429: print(r.status_code)
            if r.status_code == 403: return None
        return BeautifulSoup(r.content, features='lxml')

    def get_courses(self):
        url = 'https://mukilteo.schoology.com/iapi2/site-navigation/courses'
        j = s.get(url).json()
        res = {}
        for c in j['data']['courses']:
            res[c['nid']] = c['courseTitle']
        return res

    def get_course_members(self, cid: str):
        url = f'https://mukilteo.schoology.com/enrollments/edit/members/course/{cid}' '/ajax?ss=&p={}'
        soup = self.get_soup(url.format(1))
        per_page = int(soup.select_one('.end-count').text) + 1
        total = int(soup.select_one('.total').text)
        res = {}
        for p in range(1, (total+per_page-1)//per_page+1):
            soup = self.get_soup(url.format(p))
            for tr in soup.select('tr'):
                sid = tr.attrs['id']
                name = tr.select_one('.user-name').text.strip()
                img = tr.select_one('img').attrs['src'].replace('profile_tiny', 'profile_reg')
                res[sid] = {'name': name, 'img': img}
        return res

def download_image(url, filename) -> bool:
    # This function assumes correct images are .jpg
    if '.svg' in url: return False
    try:
        r = requests.get(url)
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    except Exception as e:
        print(e)
        return False
    return '.jpg' in url

def tk_main(members):
    A = list(members.keys())
    random.shuffle(A)
    B = []
    N = len(A)

    last_sid = A[0]
    def get_image(sid, bw=False):
        nonlocal last_sid
        last_sid = sid
        img = Image.open(f'tmp/{sid}.jpg')
        if bw: img = img.convert('L')
        return ImageTk.PhotoImage(img)

    master = Tk()
    master.title('Flashcards')

    l1 = Label(master, text='Do you know your class?', justify='center', font=('Arial', 12))
    l1.grid(row=0, column=0, columnspan=2, pady=2)

    sub = Label(master, text=f'{0}/{N} cards', justify='center')
    sub.grid(row=1, column=0, columnspan=2, pady=2)

    img = get_image(A[0])
    li = Label(master, image=img)
    li.grid(row=2, column=0, columnspan=2, rowspan=2, padx=5, pady=5)

    ln = Label(master, text='???', justify='center')
    ln.grid(row=4, column=0, columnspan=2)

    def show_done():
        nonlocal img
        sub.config(text='Flashcards complete!')
        ln.config(text='')
        ba.config(state='disabled')
        bg.config(state='disabled')
        img = get_image(last_sid, bw=True)
        li.config(image=img)

    def show():
        show_bag()
        ln.config(text=members[A[0]]['name'])

    def again():
        B.append(A.pop(0))
        show_bs()

    def good():
        del A[0]
        show_bs()

    def show_bs():
        nonlocal img
        sub.config(text=f'{N-len(A)-len(B)}/{N} cards')
        if not A:
            random.shuffle(B)
            A[:] = B
            del B[:]
        if not A:
            show_done()
            return
        ba.grid_forget()
        bg.grid_forget()
        bs.grid(row=5, column=0, columnspan=2, padx=5, pady=5, ipadx=63, ipady=10)
        img = get_image(A[0])
        li.config(image=img)
        ln.config(text='???')

    def show_bag():
        bs.grid_forget()
        ba.grid(row=5, column=0, sticky=W, padx=5, pady=5, ipadx=10, ipady=10)
        bg.grid(row=5, column=1, sticky=E, padx=5, pady=5, ipadx=10, ipady=10)

    style = Style()
    style.configure('Green.TButton', foreground='#004d00')
    style.configure('Red.TButton', foreground='#711321')
    bs = Button(master, text='Show', command=show)
    ba = Button(master, text='Again', style='Red.TButton', command=again)
    bg = Button(master, text='Good', style='Green.TButton', command=good)

    show_bs()

    mainloop()

if __name__ == '__main__':
    from getpass import getpass
    suffix = '@mukilteo.wednet.edu'
    email = input('Enter school ID: ').strip().removesuffix(suffix) + suffix
    password = getpass('Enter password: ')
    s = SchoologySession(email, password)
    print('Logged in!')
    print('Your courses')
    courses = list(s.get_courses().items())
    for i, (cid, course) in enumerate(courses):
        print(f'[{i+1}] {course}')

    cid, course = courses[int(input('Enter course number: ').strip()) - 1]
    print('You selected:', course)

    print('Downloading images...')
    members = {}
    for sid, sdata in s.get_course_members(cid).items():
        if not download_image(sdata['img'], f'tmp/{sid}.jpg'):
            print('Error')
            continue
        members[sid] = sdata
    print('Starting GUI')
    tk_main(members)