"""Python 3 unoffical, simplified, resource friendly rank script for beginners on mobstar.cc"""

__author__ = 'Jonathan Teel'
__credits__ = ['Jonathan Teel']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Jonathan Teel'
__status__ = 'Development'

import sys
import requests
import time
import datetime
import json
from bs4 import BeautifulSoup
import threading
from tkinter import *
from tkinter.ttk import *

def outp(say):
    reslbl.configure(text=f'[{datetime.datetime.now()}] {uemail} : {say}')

params = {}
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Origin': 'https://www.mobstar.cc'
})
req = requests.Session()
url = "https://mobstar.cc"
rank = ''
cash = ''
plane = ''
nextClickTime = 0
drDrug1 = 'LSD'
drCountry1 = 'Great Britain'
drDrug2 = 'XTC'
drCountry2 = 'Russia'
uemail = ''
upword = ''
drugs = ['Nederwiet', 'XTC', 'LSD', 'Speed', 'Paddos', 'Opium', 'Fireworks', 'OptDrug1']
playerInfo_data = {'switchRow':'1'}
login_url = f'{url}/main/login.php'
playerInfo_url = f'{url}/mobstar/playerinfo_updater.php'
gta_url = f'{url}/mobstar/money/gta.php'
crime_url = f'{url}/mobstar/money/crime.php'
drug_url = f'{url}/mobstar/money/drugs.php'
airport_url = f'{url}/mobstar/airport.php'
jail_url = f'{url}/mobstar/jail.php'
injail_url = f'{url}/mobstar/injail.php'

# Nederwiet=20&XTC=0&LSD=0&Speed=0&Paddos=0&Opium=0&Fireworks=0&OptDrug1=0&buy=Buy
def updateDrug(d):
    if d.lower() == 'weed': return 'Nederwiet'
    if d.lower() == 'xtc': return 'XTC'
    if d.lower() == 'lsd': return 'LSD'
    if d.lower() == 'speed': return 'Speed'
    if d.lower() == 'shrooms': return 'Paddos'
    if d.lower() == 'heroin': return 'Opium'
    if d.lower() == 'cocaine': return 'Fireworks'
    if d.lower() == 'fireworks': return 'OptDrug1'
    quit('drug format bad')

def buildDrugData(d, amt, bs):
    ddate = {}
    for drug in drugs:
        if d == drug:
            ddate[drug] = amt
        else:
            ddate[drug] = '0'
    if bs == 'buy':
        ddate['buy'] = 'Buy'
    else:
        ddate['sell'] = 'Sell'
    return ddate

def pdoDrug(drug, amount, type):
    dobj = buildDrugData(drug, amount, type)
    req.post(drug_url, dobj, headers=headers)

def getBestGta():
    gtaPage = req.get(gta_url, headers=headers)
    gpercsoup = BeautifulSoup(gtaPage.text, 'html.parser')
    gpercTbl = gpercsoup.find('table', class_='userprof')
    try:
        gpercRows = gpercTbl.findChildren('tr')
    except Exception:
        doLogin()
        return False
    bestGta = 0
    maxGta = 0
    for idx, gperRow in enumerate(gpercRows):
        if idx > 4: break
        if idx > 0:
            gty = gperRow.select('.footer')
            perc = 0
            try:
                perc = int(gty[1].text.split(' ')[0].split('%')[0])
            except Exception:
                outp('getBestGta footer select error')
            if perc > maxGta:
                maxGta = perc
                bestGta = idx - 1  
    return bestGta

def pdoFly(flyto):
    airport_data = {'flyto':flyto}
    outp('flying to ' + flyto)
    req.post(airport_url, airport_data, headers=headers)

def isInJail():
    ijresp = req.get(injail_url, headers=headers)
    injsoup = BeautifulSoup(ijresp.text, 'html.parser')
    injh = injsoup.find_all('h1')
    for h in injh:
        if 'You are in jail' in h.string:
            return True
    return False

def getPlayerDrugAmt():
    dresp = req.get(drug_url, headers=headers)
    dsoup = BeautifulSoup(dresp.text, 'html.parser')
    diall = dsoup.find_all('i')
    for di in diall:
        if 'You can carry' in di.string:
            outp('player drug carry amount : ' + str(di.string.split(' ')[3]))
            return di.string.split(' ')[3]
     
def getPossibleFlights():
    aresp = req.get(airport_url, headers=headers)
    asoup = BeautifulSoup(aresp.text, 'html.parser')
    atbls = asoup.find('table', class_='userprof')
    arows = atbls.findChildren('tr')
    availLocs = []
    for arow in arows:
        aid = arow.findChildren('input')
        for aa in aid:
            if aa.has_attr('id'):
                availLocs.append(aa['id'])
    return availLocs

def getCrimeType():
    # first one is best
    cresp = req.get(crime_url, headers=headers)
    soup = BeautifulSoup(cresp.text, 'html.parser')
    ptbl = soup.find('table', class_='userprof')
    prows = ptbl.findChildren('tr')
    carr = []
    for idx, pr in enumerate(prows):
        if idx == 0: continue
        pds = pr.findChildren('td')
        for pd in pds:
            la = pd.select('label')
            if len(la) > 0:
                return la[0]['id'].split('e')[1]

# main crimes

def pdoCrime():
    crimeType = getCrimeType()
    crime_data = {'crime2':crimeType}
    req.post(crime_url, crime_data, headers=headers)

def pdoGta():
    gtaType = getBestGta()
    gta_data = {'stealcar': gtaType, 'takefromcrewname': ''}
    gtaResp = req.post(gta_url, gta_data, headers=headers)
    gsoup = BeautifulSoup(gtaResp.text, 'html.parser')
    gpAll = gsoup.find_all('p')
    for gp in gpAll:
        if "You failed! Those wheels ain't yours." in gp.text:
            return False

def pdoJb():
    jresp = req.get(jail_url, headers=headers)
    html = jresp.content.decode(jresp.encoding)
    soup = BeautifulSoup(html, 'html.parser')
    jTbl = soup.find(id='JailTable')
    if jTbl is None:
        return False
    jrows = jTbl.findChildren('tr')
    ii = 0
    noop = [0, 1, 2]
    for jr in jrows:
        if ii in noop:
            ii += 1
            continue
        jcells = jr.findChildren('td')
        if jcells[3].string == 'Bust out':
            outp('doing bust out')
            jhref = jcells[3].findChildren('a')
            jid = jhref[0]['href']
            jurl = f'{url}/mobstar/{jid}'
            jresp = req.get(jurl, headers=headers)
            jsoup = BeautifulSoup(jresp.text, 'html.parser')
            jp = list(reversed(jsoup.find_all('p')))
            for p in jp:
                if 'Users in jail:' in p.string:
                    outp('Busted')
                    return False
                elif 'Bummer, that player was freed already' in p.string:
                    outp(p.string)
                elif 'Success!' in p.string:
                    outp(p.string)     

def pdoDrugRun():
    amt = getPlayerDrugAmt()
    flyto = ''
    fdr = ''
    posFlights = getPossibleFlights()
    if drCountry1 in posFlights: 
        flyto = drCountry1
        fdr = drDrug1
    else: 
        flyto = drCountry2
        fdr = drDrug2
    pdoDrug(fdr, amt, 'buy')
    pdoFly(flyto)
    pdoDrug(fdr, amt, 'sell')

####
 
def getPlayerInfo():
    global rank
    global cash
    global plane
    try:
        pres = req.post(playerInfo_url, playerInfo_data, headers=headers)
        pinfo = json.loads(pres.text)
        rank = pinfo['playerinfo']['rank']
        cash = pinfo['playerinfo']['cash']
        plane = pinfo['playerinfo']['plane']
    except Exception:
        outp('getPlayerInfoError')

def doMove():
    if isInJail():
        doMove.nextClickTime = time.time() + 20
        return False
    pres = req.post(playerInfo_url, playerInfo_data, headers=headers)
    pinfo = ''
    try:
        pinfo = json.loads(pres.text)
    except Exception:
        doMove.nextClickTime = time.time() + 30
        doLogin()
        return False

    times = []
    doCrime = False
    crTime = 0
    rank = pinfo['playerinfo']['rank']
    crimeTime = pinfo['character']['crime'][0]
    lastCrimeTime = pinfo['character']['crime'][1]
    if lastCrimeTime > crimeTime:
        doCrime = True
    else:
        times.append(crimeTime - lastCrimeTime)

    doGta = False
    gTime = 0
    gtaTime = pinfo['character']['gta'][0]
    lastGtaTime = pinfo['character']['gta'][1]
    if lastGtaTime > gtaTime:
        doGta = True
    elif int(gtaTime) > 0:
        times.append(gtaTime - lastGtaTime)

    doAir = False
    aTime = 0
    airTime = pinfo['character']['airport'][0]
    lastAirTime = pinfo['character']['airport'][1]
    drBuyTime = pinfo['character']['drugs'][0]
    lastDrBuyTime = pinfo['character']['drugs'][1]
    if lastAirTime > airTime:
        if lastDrBuyTime > drBuyTime:
            doAir = True
        else:
            times.append(drBuyTime - lastDrBuyTime)
    else:
        times.append(airTime - lastAirTime)

    minTime = 120
    for t in times:
        if t < minTime: minTime = t
    doMove.nextClickTime = time.time() + minTime + 2

    if doCrime:
        pdoCrime()
    if doGta:
        pdoGta()
    if doAir:
        pdoDrugRun()
    
def doLogin():
    login_data = {'email':uemail, 'password':upword}
    loginReq = req.post(login_url, login_data, headers=headers)
    if loginReq.status_code != 200:
        outp('login failed : ' + str(loginReq.status_code))
        quit("login failed")

def start():
    global drDrug1
    global drDrug2
    start.dostop = False
    doLogin()
    getPlayerInfo()
    drDrug1 = updateDrug(drDrug1)
    drDrug2 = updateDrug(drDrug2)
    getPlayerInfo()
    doMove()
    while True:
        time.sleep(15)
        if time.time() > doMove.nextClickTime:        
            try:    
                doMove()
            except requests.exceptions.ConnectionError:
                outp('connection error in main while loop')
                time.sleep(5)
                doLogin()
            except Exception:
                outp('exception caught in main while loop')
                time.sleep(5)
                doLogin()
        if not isInJail():
            pdoJb()
        if start.dostop:
            return False

def stopBtnClick():
    reslbl.configure(text='stopping...')
    start.dostop = True
    t.join()
    window.destroy()

def startBtnClick():
    global uemail
    global upword
    global drCountry1
    global drCountry2
    global drDrug1
    global drDrug2
    global t
    uemail = em.get()
    upword = pw.get()
    drCountry1 = drc1.get()
    drCountry2 = drc2.get()
    drDrug1 = drd1.get()
    drDrug2 = drd2.get()
    if uemail is None or upword is None:
        reslbl.configure(text='empty email/password')
        return False
    reslbl.configure(text='ranking starting')
    print('starting')
    t = threading.Thread(target=start)
    t.start()
    
t = None
window = Tk()
window.title('Mob Simple Script')
window.geometry('600x200')

elbl = Label(window, text="Enter the email : ")
elbl.grid(column=0, row=0)
em = Entry(window, width=40)
em.grid(column=1, row=0)

plbl = Label(window, text="Enter the password : ")
plbl.grid(column=0, row=1)
pw = Entry(window, width=40)
pw.grid(column=1, row=1)

Label(window, text="Select country for DR 2").grid(column=0, row=2)
drc1 = Combobox(window)
drc1['values']= ('Colombia', 'Netherland', 'Italy', 'Russia', 'China', 'Great Britain')
drc1.current(0)
drc1.grid(column=1, row=2)

Label(window, text="Select drug for DR 1").grid(column=0, row=3)
drd1 = Combobox(window)
drd1['values']= ('Weed', 'XTC', 'LSD', 'Speed', 'Shrooms', 'Heroin', 'Cocaine', 'Fireworks')
drd1.current(0)
drd1.grid(column=1, row=3)

Label(window, text="Select country for DR 2").grid(column=0, row=4)
drc2 = Combobox(window)
drc2['values']= ('Colombia', 'Netherland', 'Italy', 'Russia', 'China', 'Great Britain')
drc2.current(1)
drc2.grid(column=1, row=4)

Label(window, text="Select drug for DR 2").grid(column=0, row=5)
drd2 = Combobox(window)
drd2['values']= ('Weed', 'XTC', 'LSD', 'Speed', 'Shrooms', 'Heroin', 'Cocaine', 'Fireworks')
drd2.current(1)
drd2.grid(column=1, row=5)

startBtn = Button(window, text="Start", command=startBtnClick, width=20)
startBtn.grid(column=0, row=12)
stopBtn = Button(window, text="Stop", command=stopBtnClick, width=20)
stopBtn.grid(column=0, row=13)
reslbl = Label(window)
reslbl.grid(column=0, row=15)

window.mainloop()