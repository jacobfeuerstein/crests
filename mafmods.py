import marfc_list as ma
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import cartopy
import cartopy.crs as ccrs
import re
import cartopy.feature as cf
import datetime
from datetime import datetime as dt
from datetime import timedelta

from IPython.display import HTML


def loadriverdata():
    bigtext = open("nationalrivers.txt", "r")
    bigtext = (bigtext.read())
    import ast
    bigtext = ast.literal_eval(bigtext)

    Title = []
    Latitude=[]
    Longitude = []
    Location = []
    Rankings = []
    One = []
    for i in bigtext:
        Title.append(i[0])
        Latitude.append(float(i[1][0]))
        Longitude.append(float(i[1][1]))
        Location.append(i[1])
        Rankings.append(i[2])

    df = {'Title':Title,
        'Location':Location,
        'Latitude':Latitude,
        'Longitude':Longitude,
        'Rankings':Rankings}
    df = pd.DataFrame(df)

    #df = df[df['Latitude']>36]
    #df = df[df['Longitude']<82]
    df=df.reset_index()


    return(df)

def createdf():

    df=loadriverdata()

    One = []
    Two = []
    Three = []
    Four=[]
    Five=[]

    for i in df['Rankings']:
        oneb = i.index('(1)')+4
        i = i[oneb:]
        oneb = i.index('on') + 3
        onee = i.index('<b')
        one = i[oneb:onee]
        One.append(one)

        twob = i.index('(2)')+4
        i = i[twob:]
        twob = i.index('on') + 3
        twoe = i.index('<b')
        two = i[twob:twoe]
        Two.append(two)

        try:
            threeb = i.index('(3)')+4
            i = i[threeb:]
            threeb = i.index('on') + 3
            threee = i.index('<b')
            three = i[threeb:threee]
            Three.append(three)

        except:
            Three.append('01/01/1900')

        try:
            fourb = i.index('(4)')+4
            i = i[fourb:]
            fourb = i.index('on') + 3
            foure = i.index('<b')
            four = i[fourb:foure]
            Four.append(four)
        except:
            Four.append('01/01/1900')

        try:
            fiveb = i.index('(5)')+4
            i = i[fiveb:]
            fiveb = i.index('on') + 3
            fivee = i.index('<b')
            five = i[fiveb:fivee]
            Five.append(five)
        except:
            Five.append('01/01/1900')

    df['OneD'] = One
    df['TwoD'] = Two
    df['ThreeD'] = Three
    df['FourD'] = Four
    df['FiveD'] = Five

    MY = []
    yearl = []
    months=[]
    for i in df['OneD']:
        month = i[:2]
        year = i[6:10]
        yearl.append(str(year))
        months.append(int(year[:3]))
        MY.append(month + '/' + year)

    df['MY1'] = MY
    df['month'] = months
    df['year1'] = yearl

    MY2 = []
    yearl2=[]
    for i in df['TwoD']:
        month = i[:2]
        year = i[6:10]
        yearl2.append(year)
        MY2.append(month + '/' + year)

    df['MY2'] = MY2
    df['year2'] = yearl2

    MY3 = []
    yearl3=[]
    for i in df['ThreeD']:
        month = i[:2]
        year = i[6:10]
        yearl3.append(year)
        MY3.append(month + '/' + year)

    df['MY3'] = MY3
    df['year3'] = yearl3

    MY4 = []
    yearl4=[]
    for i in df['FourD']:
        month = i[:2]
        year = i[6:10]
        yearl4.append(year)
        MY4.append(month + '/' + year)

    df['MY4'] = MY4
    df['year4'] = yearl4

    MY5 = []
    yearl5=[]
    for i in df['FiveD']:
        month = i[:2]
        year = i[6:10]
        yearl5.append(year)
        MY5.append(month + '/' + year)

    df['MY5'] = MY5
    df['year5'] = yearl5


    recordyear = []
    beginyear = []

    df=df.reset_index()
    n=0
    while n < len(df['Rankings']):
        ranklist = df['Rankings'][n]
        firstyear=3000
        while 'on' in ranklist:
            year = int(ranklist[(ranklist.index('on') + 9):(ranklist.index('on') + 13)])
            if firstyear > year:
                firstyear=year
            ranklist=ranklist[(ranklist.index('on') + 15):]

        beginyear.append(firstyear)
        n=n+1

    df['Firstyear'] = beginyear


    return(df)

def topMY():
    df=createdf()
    newdf={}
    newdf = pd.DataFrame(newdf)
    ones = df['MY1'].value_counts()
    newdf['ones'] = ones
    twos = df['MY2'].value_counts()
    newdf['twos'] = twos
    threes = df['MY3'].value_counts()
    newdf['threes'] = threes
    fours = df['MY4'].value_counts()
    newdf['fours'] = fours
    fives = df['MY5'].value_counts()
    newdf['fives'] = fives
    return(newdf)

def topyear():
    df=createdf()
    newdf={}
    newdf = pd.DataFrame(newdf)
    ones = df['year1'].value_counts()
    newdf['ones'] = ones
    twos = df['year2'].value_counts()
    newdf['twos'] = twos
    threes = df['year3'].value_counts()
    newdf['threes'] = threes
    fours = df['year4'].value_counts()
    newdf['fours'] = fours
    fives = df['year5'].value_counts()
    newdf['fives'] = fives
    return(newdf)

def nplotmonth(number, df, MY, msize, coorlist):
    mult_lon=10*((coorlist[1]-coorlist[0])/60)
    mult_lat=1.5*((coorlist[3]-coorlist[2])/25)

    clist=['blue','green','red','orange','grey']
    for i in range(number):
        i=number-i
        i=str(i)
        June1972 = df[df['MY'+i]==str(MY)]

        for x in June1972['Location']:
            plt.plot(-float(x[1]), float(x[0]), color=clist[int(i)-1], markersize=msize, marker='o', transform=ccrs.Geodetic())

        plt.text(coorlist[0]+mult_lon*(int(i)-1), coorlist[2]-mult_lat, '#'+str(i)+  ' (n = ' + str(len(June1972)) + ')', fontsize=20, transform=ccrs.PlateCarree(), color=clist[int(i)-1])

def plotmonth(MY, n, coorlist, msize):

    df=createdf()

    fig = plt.figure(figsize=(15, 15))

    proj = ccrs.PlateCarree()
    ax1 = fig.add_subplot(1,1,1,projection=proj)
    ax1.set_title("Gages With Top-"+str(n)+" Crest Records From "+str(MY), loc='left', size = 20)

    border_resolution = '50m'  # Adjust the resolution as needed
    ax1.coastlines(resolution=border_resolution, linewidth=0.8)
    ax1.add_feature(cf.BORDERS.with_scale(border_resolution), edgecolor=[.3, .3, .3], linewidth=0.5, linestyle=':')
    ax1.add_feature(cf.STATES.with_scale(border_resolution), edgecolor='gray', linewidth=0.5)
    ax1.set_extent(coorlist,crs=ccrs.PlateCarree()) # select region

    nplotmonth(n, df, MY, msize, coorlist)

    plt.savefig(MY[:2]+MY[3:]+'fl.png', bbox_inches = 'tight', pad_inches = 0.1)

    return(MY[:2]+MY[3:]+'fl.png')

def nplotday(MYD, n, coorlist, msize, df):
    mult_lon=10*((coorlist[1]-coorlist[0])/60)
    mult_lat=1.5*((coorlist[3]-coorlist[2])/25)
    numlist=['One','Two','Three','Four','Five']

    clist=['blue','green','red','orange','grey']
    sumlist=[]
    for i in range(n):
        print(i)

        June1972 = df[df[numlist[i]+'D']==str(MYD)]

        for x in June1972['Location']:
            plt.plot(-float(x[1]), float(x[0]), color=clist[int(i)-1], markersize=msize, marker='o', transform=ccrs.Geodetic())

        sumlist.append(len(June1972))

    return(sumlist)


def plotdates(d1, d2, n, coorlist, msize):

    df=createdf()

    fig = plt.figure(figsize=(15, 15))
    proj = ccrs.PlateCarree()
    ax1 = fig.add_subplot(1,1,1,projection=proj)
    ax1.set_title("Gages With Top-"+str(n)+" Crest Records From "+d1 + ' to ' + d2, loc='left', size = 20)
    border_resolution = '50m'  # Adjust the resolution as needed
    ax1.coastlines(resolution=border_resolution, linewidth=0.8)
    ax1.add_feature(cf.BORDERS.with_scale(border_resolution), edgecolor=[.3, .3, .3], linewidth=0.5, linestyle=':')
    ax1.add_feature(cf.STATES.with_scale(border_resolution), edgecolor='gray', linewidth=0.5)
    ax1.set_extent(coorlist,crs=ccrs.PlateCarree()) # select region
    dtobj = dt.strptime(d1, '%m/%d/%Y')
    isumlist=[]
    while dtobj != dt.strptime(d2, '%m/%d/%Y'):
        isumlist.append(nplotday(dtobj.strftime('%m/%d/%Y'), n, coorlist, msize, df))
        dtobj = dtobj + timedelta(days=1)

    sumlist = [sum(x) for x in zip(*isumlist)]
    mult_lon=10*((coorlist[1]-coorlist[0])/60)
    mult_lat=1.5*((coorlist[3]-coorlist[2])/25)

    n=0
    clist=['blue','green','red','orange','grey']

    while n < len(sumlist):
        plt.text(coorlist[0]+mult_lon*(n), coorlist[2]-mult_lat, '#'+str(n+1)+  ' (n = ' + str(sumlist[n]) + ')', fontsize=20, transform=ccrs.PlateCarree(), color=clist[n])
        n=n+1

    plt.savefig(dtobj.strftime('%m.%d.%Y')+'fl.png', bbox_inches = 'tight', pad_inches = 0.1)


def nplotyear(number, df, year, msize, coorlist):
    clist=['blue','green','red','orange','grey']
    for i in range(number):
        i=number-i
        i=str(i)
        June1972 = df[df['year'+i]==str(year)]


        for x in June1972['Location']:
            plt.plot(-float(x[1]), float(x[0]), color=clist[int(i)-1], markersize=msize, marker='o', transform=ccrs.Geodetic())

        plt.text(coorlist[0]+10*(int(i)-1), coorlist[2]-1.5, '#'+str(i)+  ' (n = ' + str(len(June1972)) + ')', fontsize=20, transform=ccrs.PlateCarree(), color=clist[int(i)-1])

def plotyear(year, n, coorlist, msize, title2):

    df=createdf()

    fig = plt.figure(figsize=(15, 15))

    proj = ccrs.PlateCarree()
    ax1 = fig.add_subplot(1,1,1,projection=proj)
    ax1.set_title("Record Floods in "+str(year) + ' ' + title2, loc='left', size = 20)

    border_resolution = '50m'  # Adjust the resolution as needed
    ax1.coastlines(resolution=border_resolution, linewidth=0.8)
    ax1.add_feature(cf.BORDERS.with_scale(border_resolution), edgecolor=[.3, .3, .3], linewidth=0.5, linestyle=':')
    ax1.add_feature(cf.STATES.with_scale(border_resolution), edgecolor='gray', linewidth=0.5)
    ax1.set_extent(coorlist,crs=ccrs.PlateCarree()) # select region
    print(df)
    nplotyear(n, df, year, 7, coorlist)

#    plt.text(coorlist[1]-2, coorlist[3]+0.5, '#'+str(title2), fontsize=20, transform=ccrs.PlateCarree())

    plt.savefig(str(year)+'fl.png', bbox_inches = 'tight', pad_inches = 0.1)

    return(str(year)+'fl.png')

def animate(images, title):
    image_list = []
    from PIL import Image
    import imageio

    for file_name in images:
        image_list.append(imageio.imread(file_name))
    from pygifsicle import optimize
    imageio.mimwrite('era5.gif', image_list, duration= 2)
    optimize('era5.gif', title+'.gif')

def trend():
    bigtext = open("nationalrivers.txt", "r")
    bigtext = (bigtext.read())
    import ast
    bigtext = ast.literal_eval(bigtext)
    #print(bigtext)

    Title = []
    Location = []
    Rankings = []
    Latitude=[]
    Longitude = []
    One = []
    for i in bigtext:
        Title.append(i[0])
        Latitude.append(float(i[1][0]))
        Longitude.append(float(i[1][1]))
        Location.append(i[1])
        Rankings.append(i[2].split('<br'))

    df = {'Title':Title,
        'Location':Location,
        'Latitude':Latitude,
        'Longitude':Longitude,
        'Rankings':Rankings}
    df = pd.DataFrame(df)

    #df = df[df['Latitude']>36]
    #df = df[df['Longitude']<82]
    df=df.reset_index()
    recordyear = []
    beginyear = []
    n=0
    while n < len(df['Rankings']):
        ranklist = df['Rankings'][n]
        x=1
        while x < len(ranklist)-1:
            if x == 1:
                recordyear.append(int(ranklist[x][ranklist[x].index('on')+9:ranklist[x].index('on')+14]))
                firstyear = int(ranklist[x][ranklist[x].index('on')+9:ranklist[x].index('on')+14])
            else:
                tempyear = int(ranklist[x][ranklist[x].index('on')+9:ranklist[x].index('on')+14])
                if tempyear < firstyear and tempyear > 1500:
                    firstyear = tempyear
            x=x+1
        beginyear.append(firstyear)
        n=n+1

    df['Firstyear'] = beginyear
    df['Recordyear'] = recordyear


    n=0
    yearlist=[]
    recordlist=[]
    startlist=[]
    percent=[]
    for year in range(2023-1900):
        year=year+1900
        print(year)
        rcounter = 0
        scounter = 0
        n=0
        while n < len(df['Recordyear']):
            if df['Recordyear'][n] == year:
                rcounter = rcounter + 1
            if df['Firstyear'][n] < year+1:
                scounter = scounter + 1
            n=n+1
        recordlist.append(rcounter)
        startlist.append(scounter)
        percent.append((rcounter/scounter) * 100)
        yearlist.append(year)


    df2 = {'Year':yearlist,
        'Starts':startlist,
        'Records':recordlist,
        'Percent':percent}
    df2 = pd.DataFrame(df2)
    df2=df2.sort_values(by=['Percent'], ascending = False)

    return(df2)

def idksavedis():
    df=df2

    fig = plt.figure(figsize=(15, 15))

    proj = ccrs.PlateCarree()
    ax1 = fig.add_subplot(1,1,1,projection=proj)
    ax1.set_title("Mississippi River Record Flood Events", loc='left', size = 20)

    coorlist=[-125, -65, 25, 50]

    border_resolution = '50m'  # Adjust the resolution as needed
    ax1.coastlines(resolution=border_resolution, linewidth=0.8)
    ax1.add_feature(cf.BORDERS.with_scale(border_resolution), edgecolor=[.3, .3, .3], linewidth=0.5, linestyle=':')
    ax1.add_feature(cf.STATES.with_scale(border_resolution), edgecolor='gray', linewidth=0.5)
    ax1.set_extent(coorlist,crs=ccrs.PlateCarree()) # select region

    June1972 = df


    for x in June1972['Location']:
        plt.plot(-float(x[1]), float(x[0]), color='black', markersize=5, marker='o', transform=ccrs.Geodetic())

    plt.text(coorlist[0]+30, coorlist[2]-1.5, 'Other', fontsize=20, transform=ccrs.PlateCarree())

    June1972 = df[df['year1']=='2011']


    for x in June1972['Location']:
        plt.plot(-float(x[1]), float(x[0]), color='grey', markersize=7, marker='o', transform=ccrs.Geodetic())

    plt.text(coorlist[0]+25, coorlist[2]-1.5, '2011', color='grey',fontsize=20, transform=ccrs.PlateCarree())

    June1972 = df[df['year1']=='2008']


    for x in June1972['Location']:
        plt.plot(-float(x[1]), float(x[0]), color='green', markersize=7, marker='o', transform=ccrs.Geodetic())

    plt.text(coorlist[0]+20, coorlist[2]-1.5, '2008', color='green',fontsize=20, transform=ccrs.PlateCarree())


    June1972 = df[df['year1']=='1993']


    for x in June1972['Location']:
        plt.plot(-float(x[1]), float(x[0]), color='orange', markersize=7, marker='o', transform=ccrs.Geodetic())

    plt.text(coorlist[0]+15, coorlist[2]-1.5, '1993', color='orange',fontsize=20, transform=ccrs.PlateCarree())


    June1972 = df[df['year1']=='1965']


    for x in June1972['Location']:
        plt.plot(-float(x[1]), float(x[0]), color='red', markersize=7, marker='o', transform=ccrs.Geodetic())

    plt.text(coorlist[0]+10, coorlist[2]-1.5, '1965', color='red',fontsize=20, transform=ccrs.PlateCarree())


    June1972 = df[df['year1']=='1937']


    for x in June1972['Location']:
        plt.plot(-float(x[1]), float(x[0]), color='purple', markersize=7, marker='o', transform=ccrs.Geodetic())

    plt.text(coorlist[0]+5, coorlist[2]-1.5,  '1937', color='purple', fontsize=20, transform=ccrs.PlateCarree())


    plt.savefig('Mississippi River fl.png', bbox_inches = 'tight', pad_inches = 0.1)



    June1972 = df[df['year1']=='1927']


    for x in June1972['Location']:
        plt.plot(-float(x[1]), float(x[0]), color='blue', markersize=7, marker='o', transform=ccrs.Geodetic())

    plt.text(coorlist[0], coorlist[2]-1.5,  '1927', color='blue', fontsize=20, transform=ccrs.PlateCarree())


    plt.savefig('Mississippi River fl.png', bbox_inches = 'tight', pad_inches = 0.1)

def rankit(m,y,data):

    target_month = m  # January (you can change this to any month number)
    target_year = y  # Year (you can change this to any year)

    # Pattern to match the required date format
    pattern = rf"\((\d+)\) \d+\.\d+ ft on {target_month:02d}/\d+/{target_year}"

    matches = re.findall(pattern, data)

    # Get the lowest ranking among all matches for the specified month and year
    if matches:
        rankings = [int(match) for match in matches]
        lowest_rank = min(rankings)
        return(lowest_rank)
    else:
        return(0)

def compare(m,y,m2,y2):
    df=createdf()
    r96=[]
    rag=[]
    for row in df['Rankings']:
        r96.append(rankit(m,y,row))
        rag.append(rankit(m2,y2,row))

    df['rag']=rag
    df['r96']=r96
    df=df[df['r96']!=0]
    df=df[df['rag']!=0]
    df.reset_index(drop=True, inplace=True)
    print(df[:50])
    dfag = df[df['r96'] > df['rag']]
    df96 = df[df['rag'] > df['r96']]


    fig = plt.figure(figsize=(15, 15))

    proj = ccrs.PlateCarree()
    ax1 = fig.add_subplot(1,1,1,projection=proj)
    ax1.set_title("Which flood was worse?", loc='left', size = 20)

    coorlist=[-95, -65, 35, 50]

    border_resolution = '50m'
    ax1.coastlines(resolution=border_resolution, linewidth=0.8)
    ax1.add_feature(cf.BORDERS.with_scale(border_resolution), edgecolor=[.3, .3, .3], linewidth=0.5, linestyle=':')
    ax1.add_feature(cf.STATES.with_scale(border_resolution), edgecolor='gray', linewidth=0.5)
    ax1.set_extent(coorlist,crs=ccrs.PlateCarree())

    #sc = ax1.scatter(-df['Longitude'], df['Latitude'], c=df['Firstyear'], cmap='ocean', s=10+((df['Firstyear']-1700)/50), transform=ccrs.PlateCarree())
    #plt.colorbar(sc, fraction = 0.015)

    for x in df96['Location']:
        plt.plot(-float(x[1]), float(x[0]), color='blue', markersize=5, marker='o', transform=ccrs.Geodetic())
    plt.text(coorlist[0], coorlist[2]-.75,  str(y), color='blue', fontsize=20, transform=ccrs.PlateCarree())

    for x in dfag['Location']:
        plt.plot(-float(x[1]), float(x[0]), color='red', markersize=5, marker='o', transform=ccrs.Geodetic())
    plt.text(coorlist[0]+5, coorlist[2]-.75,  str(y2), color='red', fontsize=20, transform=ccrs.PlateCarree())

    plt.savefig(str(y)+'vs'+str(y2)+'.png', bbox_inches = 'tight', pad_inches = 0.1)
