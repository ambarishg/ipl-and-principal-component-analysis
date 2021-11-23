import pandas as pd
DATA_DIR = ''
BATSMAN_RUNS = "runs_batsman"


def get_batsman_stats(filename,ipl_season = ""):
    
    all_data = pd.read_csv(DATA_DIR + filename)
    all_data = get_filtered_ipl_data(ipl_season, all_data)

    
    batsman_runs = get_batsman_runs(all_data)
    batsman_fours = get_boundary(all_data,4,"batsman_fours")
    batsman_six = get_boundary(all_data,6,"batsman_six")
    batman_del = get_batsman_del(all_data)
    batsman_outs = get_batsman_outs(all_data)

    batsman_all_stats = batsman_runs.merge(batsman_fours,how = "left")
    batsman_all_stats = batsman_all_stats.merge(batsman_six,how = "left")
    batsman_all_stats = batsman_all_stats.merge(batman_del,how = "left")
    batsman_all_stats = batsman_all_stats.merge(batsman_outs,how = "left")
    batsman_all_stats["average"] = round(batsman_all_stats["batsman_runs"] / batsman_all_stats["player_out"],2)
    batsman_all_stats["strike_rate"] =round(batsman_all_stats["batsman_runs"]  / batsman_all_stats["deliveries"] *100,2)

    batsman_thirty = get_batsman_milestone(all_data,
    "thirty", 30, ubound = 50)
    batsman_fifty = get_batsman_milestone(all_data,
    "fifty", 50, ubound = 100)
    batsman_century = get_batsman_milestone(all_data,
    "century",100)

    batsman_all_stats = batsman_all_stats.merge(batsman_thirty,how = "left")
    batsman_all_stats = batsman_all_stats.merge(batsman_fifty,how = "left")
    batsman_all_stats = batsman_all_stats.merge(batsman_century,how = "left")
    batsman_all_stats = batsman_all_stats.fillna(0)

    batsman_all_stats["CHT"] = 2*batsman_all_stats["century"]+ 1.5*batsman_all_stats["fifty"] + batsman_all_stats["thirty"]

    return(batsman_all_stats)

def get_filtered_ipl_data(ipl_season, all_data):
    if ipl_season == "2007":
        all_data = all_data[all_data["season"] == "2007/08"]
    elif ipl_season == "2009":
        all_data = all_data[all_data["season"] == "2009"]
    elif ipl_season == "2010":
        all_data = all_data[all_data["season"] == "2009/10"]
    elif ipl_season == "2011":
        all_data = all_data[all_data["season"] == "2011"]
    elif ipl_season == "2012":
        all_data = all_data[all_data["season"] == "2012"]
    elif ipl_season == "2013":
        all_data = all_data[all_data["season"] == 2013]
    elif ipl_season == "2014":
        all_data = all_data[all_data["season"] == 2014]
    elif ipl_season == "2015":
        all_data = all_data[all_data["season"] == 2015]
    elif ipl_season == "2016":
        all_data = all_data[all_data["season"] == 2016]
    elif ipl_season == "2017":
        all_data = all_data[all_data["season"] == 2017]
    elif ipl_season == "2018":
        all_data = all_data[all_data["season"] == 2018]
    elif ipl_season == "2019":
        all_data = all_data[all_data["season"] == 2019]
    elif ipl_season == "2020":
        all_data = all_data[all_data["season"] == "2020/21"]
    return all_data

def get_bowler_stats(filename,ipl_season = ""):
    
    all_data = pd.read_csv(DATA_DIR + filename)
    all_data = get_filtered_ipl_data(ipl_season, all_data)
    
    runs_bowler = all_data.groupby(["bowler"])["runs_total"].sum()
    runs_bowler = runs_bowler.reset_index()

    deliveries_bowler = all_data.groupby(["bowler"])["bowler"].count()
    deliveries_bowler = deliveries_bowler.reset_index(name = "deliveries")

    wickets_bowler = all_data[all_data["player_out"].isna() == False]
    wickets_bowler = wickets_bowler.groupby(["bowler"])["bowler"].count()
    wickets_bowler = wickets_bowler.reset_index(name = "wickets")

    bowler_stats = runs_bowler.merge(deliveries_bowler, how = "left")
    bowler_stats = bowler_stats.merge(wickets_bowler, how="left")
    bowler_stats = bowler_stats[bowler_stats["deliveries"] > bowler_stats["deliveries"].median()]

    bowler_stats["average"] = round(bowler_stats["runs_total"] / bowler_stats["wickets"],2)
    bowler_stats["strike_rate"] = round(bowler_stats["deliveries"] / bowler_stats["wickets"],2)
    bowler_stats["econ"] = round((bowler_stats["runs_total"] / bowler_stats["deliveries"])*6,2)

    return(bowler_stats)


def get_batsman_milestone(all_data,milestone_name, lbound, ubound = -1):
    batsman_milestone = all_data.groupby(["batsman","match_no"])[BATSMAN_RUNS].sum()
    batsman_milestone = batsman_milestone.reset_index(name = milestone_name)
    if ubound == -1:
        batsman_milestone_players = batsman_milestone[(batsman_milestone[milestone_name] >= lbound)]
    else:
        batsman_milestone_players = batsman_milestone[(batsman_milestone[milestone_name] >= lbound) & 
                                                (batsman_milestone[milestone_name] < ubound)]

    batsman_milestone_players = batsman_milestone_players.groupby("batsman")["batsman"].count()
    batsman_milestone_players = batsman_milestone_players.reset_index(name = milestone_name)
    batsman_milestone_players = batsman_milestone_players.sort_values( by = milestone_name,ascending = False) 
    return(batsman_milestone_players)

def get_batsman_del(all_data):
    batsman_del = all_data.groupby(["batsman"])[BATSMAN_RUNS].count() \
.reset_index( name = 'deliveries').sort_values( by = 'deliveries',ascending = False) 
  
    return(batsman_del)

def get_batsman_outs(all_data):
    batsman_outs = all_data[["batsman","player_out"]]
    batsman_outs = batsman_outs.groupby("batsman")["player_out"].count() \
.reset_index( name = 'player_out').sort_values( by = 'player_out',ascending = False) 
    batsman_outs = batsman_outs.replace(0, 1)
  
    return(batsman_outs)

def get_batsman_runs(all_data):
    batsman_runs = all_data.groupby(["batsman"])[BATSMAN_RUNS].sum()
    batsman_runs = batsman_runs.reset_index( name = 'batsman_runs').sort_values( by = 'batsman_runs',ascending = False) 
  
    return(batsman_runs)

def get_boundary(all_data,boundary,boundary_name):
    
    all_data_boundary = all_data[(all_data[BATSMAN_RUNS] == boundary)]
    boundary_runs = all_data_boundary.groupby(["batsman"])["batsman"].count() \
.reset_index( name = boundary_name).sort_values( by = boundary_name,ascending = False) 
   
    return(boundary_runs)
    

