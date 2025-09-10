import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score, precision_score


wanted_cols = [
    "Date",
    "Winner",
    "WeightClass",
    "Gender",  #filter this later

    "WinDif",
    "LossDif",
    "KODif",
    "SubDif",
    "AgeDif",
    "SigStrDif",
    "AvgSubAttDif",
    "AvgTDDif",

    "BetterRank",  # who higher on P4P (blue red neither)
    "Finish",
    "FinishRound"
]

#fights from 2010-2024
#get the data with only the wanted columns we will use
fights = pd.read_csv("dataset/ufc-master.csv", usecols=wanted_cols)

#filter out all the female fights
fights = fights[fights["Gender"] == "MALE"]

winner_map = {
    "Blue": 0,
    "Red": 1,
    "Draw": 2
}

betterRank_map = {
    "Blue": 0,
    "Red": 1,
    "neither": 2
}

finish_map = { #Dec 0, sub 1, ko/tko, 2
    "S-DEC": 0,
    "U-DEC": 0,
    "M-DEC": 0,
    "SUB": 1,
    "KO/TKO": 2
}

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

#convert each data type to an int or float if not alread
fights["Date"] = pd.to_datetime(fights["Date"])
fights["Winner_code"] = fights["Winner"].map(winner_map)
fights["WeightClass_code"] = fights["WeightClass"].map(weightClass_map)
fights["BetterRank_code"] = fights["BetterRank"].map(betterRank_map)
fights["Finish_code"] = fights["Finish"].map(finish_map)
 

#make classifiers
base_model = RandomForestClassifier(n_estimators=70, min_samples_split=10, random_state=10)
multi_model = MultiOutputClassifier(base_model)


#define the testing and training range
train = fights[fights["Date"] < '2024-01-01']
test = fights[fights["Date"] > '2024-01-01']


#define targets and predictors
predictors = [
    "WeightClass_code",

    "WinDif",
    "LossDif",
    "KODif",
    "SubDif",
    "AgeDif",
    "SigStrDif",
    "AvgSubAttDif",
    "AvgTDDif",

    "BetterRank_code"  # who higher on P4P (blue red neither)

]
targets = ["Winner_code", "Finish_code"]


#clean range to remove rows with empty data
train_clean = train.dropna(subset=predictors+targets)
test_clean = test.dropna(subset=predictors+targets)


#check they are clean
assert train_clean[predictors].isnull().sum().sum() == 0
assert train_clean[targets].isnull().sum().sum() == 0

assert test_clean[predictors].isnull().sum().sum() == 0
assert test_clean[targets].isnull().sum().sum() == 0



multi_model.fit(train_clean[predictors], train_clean[targets])



def predict_fight(data):
    dataframe = pd.DataFrame([data])
    prediction = multi_model.predict(dataframe)
    winner_code = prediction[0][0]
    finish_code = prediction[0][1]

    return (winner_code, finish_code)





#prints accuracies, precision, and importance
def print_accuracies():
    preds = multi_model.predict(test_clean[predictors])

    preds_winner = preds[:, 0]
    preds_finish = preds[:, 1]

    acc_winner = accuracy_score(test_clean["Winner_code"], preds_winner)
    acc_finish = accuracy_score(test_clean["Finish_code"], preds_finish)

    print("winner accuracy:", acc_winner)
    print("finish accuracy:", acc_finish)

    prec_winner = precision_score(test_clean["Winner_code"], preds_winner)
    prec_finish = precision_score(test_clean["Finish_code"], preds_finish, average="macro")


    print("winner precision:", prec_winner)
    print("finish precision:", prec_finish)


    importances = multi_model.estimators_[0].feature_importances_
    feature_importance_df = pd.DataFrame({'feature': predictors, 'importance': importances})
    print(feature_importance_df.sort_values(by='importance', ascending=False).head(10))


