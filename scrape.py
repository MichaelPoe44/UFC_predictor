from bs4 import BeautifulSoup
import requests


SINGLE_URL = 'https://www.ufc.com/athlete/'


stats = {
    "sig_str_per_min":None,
    "sig_str_absorbed_per_min":None,
    "tkd_per_15_min":None,
    "sub_per_15_min":None,
    "sig_str_defense":None,
    "tkd_defense":None,
    "knockdown_per_15_min":None,
    "avg_fight_time":None
}




fighter_info = {
    "Weightclass": None,
    "Wins":None,
    "Losses": None,
    "KO": None,
    "Sub": None,
    "Age": None,
    "AvgSigStr":None,
    "AvgSubAtt":None,
    "AvgTDD":None,
    "p4p_rank": None
}


def get_fighter_stats(name):

    #clean the name to put into url
    name = name.strip().lower().replace(" ", "-")

    #send a request and get the page content in a soup
    page = requests.get(f"{SINGLE_URL}{name}")
    if (page.status_code != 200):
        print("Couldn't find that fighter!")
        print("Please try full name as written on the UFC website")
        return False
    soup = BeautifulSoup(page.content,'html.parser')


    #find current dvision
    try:
        fighter_info["Weightclass"] = soup.find(class_="hero-profile__division-title").text.replace(" Division", "")
    
    except:
        print("Couldn't find that fighter!")
        print("Please try full name as written on the UFC website")
        return False
     
    
    #find record
    record = soup.find(class_="hero-profile__division-body").text.split(" ")[0]
    (wins, losses, draws) = map(int, record.split("-"))
    fighter_info["Wins"] = int(wins)
    fighter_info["Losses"] = int(losses)


    #find other stats and clean data
    info = (soup.find_all(class_="c-stat-compare__number"))
    for index,key in enumerate(stats):
        temp = info[index].text
        temp = temp.replace("\n","").replace(" ","").replace("%","")
        stats[key] = temp

    fighter_info["AvgSigStr"] = float(stats["sig_str_per_min"])
    fighter_info["AvgSubAtt"] = float(stats["sub_per_15_min"])
    fighter_info["AvgTDD"] = float(stats["tkd_per_15_min"])

        

    percent_win_by = ["KO", "Dec", "Sub"]
    #find types of wins and clean
    wins = soup.find_all(class_="c-stat-3bar__value")
    Ko = wins[3].text.split()[0]
    Sub = wins[5].text.split()[0]
    
    fighter_info["KO"] = int(Ko)
    fighter_info["Sub"] = int(Sub)

    #look for a PFP rank
    tags = soup.find_all(class_="hero-profile__tag")
    for tag in tags:
        if ("PFP" in tag.text):
            rank = tag.text.split(" ")[0].replace("#","")
            fighter_info["p4p_rank"] = int(rank)
    

    #get the age
    age = soup.find(class_="field field--name-age field--type-integer field--label-hidden field__item").text
    fighter_info["Age"] = int(age)
    return fighter_info



