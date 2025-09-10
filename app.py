import Fight_predictor
import scrape




weightClass_map = {
    "Flyweight": 125,
    "Bantamweight": 135,
    "Featherweight": 145,
    "Lightweight": 155,
    "Welterweight": 170,
    "Middleweight": 185,
    "Light Heavyweight": 205,
    "Heavyweight": 265,
}








def compare_ranks(rank1, rank2):
    # 0 for blue (fighter 1)
    # 1 for red (fighter 2)
    # 2 for neither

    if (rank1 == None):
        if (rank2 == None):
            return 2 
        else:
            return 1
    
    if (rank2 == None):
        if(rank1):
            return 0
    
    if (rank1 and rank2):

        if (rank1 < rank2): #if has a greater rank then lower on p4p rank 15 worst than rank 1
            return 0
        elif (rank2 < rank1):
            return 1


def create_date(fighter_1, fighter_2, wc):


    data = {
        "WeightClass_code": wc,

        "WinDif": (fighter_1["Wins"]-fighter_2["Wins"]),
        "LossDif": (fighter_1["Losses"]-fighter_2["Losses"]),
        "KODif": (fighter_1["KO"]-fighter_2["KO"]),
        "SubDif": (fighter_1["Sub"]-fighter_2["Sub"]),
        "AgeDif": (fighter_1["Age"]-fighter_2["Age"]),
        "SigStrDif": (fighter_1["AvgSigStr"]-fighter_2["AvgSigStr"]),
        "AvgSubAttDif": (fighter_1["AvgSubAtt"]-fighter_2["AvgSubAtt"]),
        "AvgTDDif": (fighter_1["AvgTDD"]-fighter_2["AvgTDD"]),

        "BetterRank_code": compare_ranks(fighter_1["p4p_rank"], fighter_2["p4p_rank"])   
    }

    return data



while (True):

    while (True):
        print("----------------------------------")
        print("Please enter two fighters")
        print("press control and C to exit")

        name1 = input("Fighter 1: ")
        fighter1 = scrape.get_fighter_stats(name1)
        if (fighter1 == False):
            continue

        name2 = input("Fighter 2: ")
        fighter2 = scrape.get_fighter_stats(name2)
        if (fighter2 == False):
            continue

        if (fighter1["Weightclass"] != fighter2["Weightclass"]):
            print("These fighters are not in the same weightclass!")
            print("Try agian")
            continue

        both_weightclass = weightClass_map[fighter1["Weightclass"]]
        break


    matchup = create_date(fighter1, fighter2, both_weightclass)
    winner_code, finish_code = Fight_predictor.predict_fight(matchup)
    
    winner_map = {0.0: name1, 1.0: name2, 2.0: "draw"}
    finish_map = {"DEC": 0,"SUB": 1,"KO/TKO": 2}
    finish_map = {0:"DEC",1:"SUB",2:"KO/TKO"}

    if (winner_code == 2.0):
        print("Most likely outcome is a draw")

    else:
        print("The most probable outcome is:")
        print(f"\t{winner_map[winner_code]} wins")
        print(f"\tBy {finish_map[finish_code]}")


    
