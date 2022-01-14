#!/usr/bin/env python
# coding: utf-8

# # Assignment 4
# ## Description
# In this assignment you must read in a file of metropolitan regions and associated sports teams from [assets/wikipedia_data.html](assets/wikipedia_data.html) and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in [assets/nfl.csv](assets/nfl.csv)), MLB (baseball, in [assets/mlb.csv](assets/mlb.csv)), NBA (basketball, in [assets/nba.csv](assets/nba.csv) or NHL (hockey, in [assets/nhl.csv](assets/nhl.csv)). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!
# 
# For each sport I would like you to answer the question: **what is the win/loss ratio's correlation with the population of the city it is in?** Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with [`pearsonr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html), so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%\*4=80%) of the grade for this assignment. You should only use data **from year 2018** for your analysis -- this is important!
# 
# ## Notes
# 
# 1. Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
# 2. I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
# 3. It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
# 4. There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!

# ## Question 1
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NHL** using **2018** data.

# In[7]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

# para cada questão, foi feita uma função que limpa os dados e monta o df que será usado; deixei apenas o passo a passo do primeiro comentado, pois os demais seguem a mesma linha e as mudanças são evidentes
# for each question, a function was made to clean the data and build the df to be used; I left only the fist one commented because the other ones are similar and the changes are self-evident
def clean_nhl_df():
    nhl_df = pd.read_csv("assets/nhl.csv")
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0,3,5,6,7,8]]
    
    # vamos limpar o df cities, tirando os []  e substituindo alguns nomes (aqui é importante não dar espaço entre as vírgulas)
    # let's clean cities df, removing the [] and replacing some of the names (you should not have space between commas)
    cities["NHL"] = cities["NHL"].apply(lambda x: re.sub(r"\[.+\]", "", x))
    cities["NHL"] = cities["NHL"].replace({"RangersIslandersDevils": "Rangers,Islanders,Devils",
                                           "KingsDucks": "Kings,Ducks",
                                           "Red Wings": "Red,Wings", 
                                           "Maple Leafs": "Maple,Leafs", 
                                           "Blue Jackets": "Blue,Jackets",
                                           "Golden Knights": "Golden,Knights" })
    
    # depois damos um split na vírgula, para separar os times de cada região
    # then we split on the comma to separate the teams of each region
    cities["NHL"] = cities["NHL"].apply(lambda x: x.split(","))
    
    # e criamos um df a partir da series NHL
    # and we create a dataframe from the NHL column
    cities = cities.explode("NHL")

    # agora vamos limpar o dataframe nhl_df, pegando só os dados de 2018 e ajustando os nomes de alguns times
    # let's clean the nhl_df dataframe, taking only the 2018 data e adjusting some teams' names
    nhl_df = nhl_df[nhl_df["year"] == 2018]
    nhl_df["team"] = nhl_df["team"].apply(lambda x: x.replace("*", ""))

    # damos split e pegamos a segunda palavra do nome, porque a primeira é a cidade
    # we split and get only the second word of the teams' name, since the first one is the city
    nhl_df["team"] = nhl_df["team"].apply(lambda x: x.split(" ")[-1])

    # e aí damos merge para fazer o W-L ratio
    # then we merge the dataframes to get the W-L ratio
    df = pd.merge(cities, nhl_df, left_on="NHL", right_on="team")
    
    # pego só as colunas de interesse
    # consider only the columns we're interested in
    df = df[["Metropolitan area", "Population (2016 est.)[8]", "NHL", "team", "W", "L"]]
    
    # faz a razão
    # compute the ratio
    df["W-L%"] = df["W"].astype("int")/(df["W"].astype("int") + df["L"].astype("int"))

    # converte para float
    # convert to float
    df["Population (2016 est.)[8]"] = df["Population (2016 est.)[8]"].astype("float")
    df["W-L%"] = df["W-L%"].astype("float")

    # NY tem 3 times e LA tem 2, então trocamos os W-L% de cada um pelas médias
    # NY has 3 teams and LA has 2, so we change the W-L% for the means
    df.loc[df["Metropolitan area"] == "New York City", "W-L%"] = 0.5182013333333334 # mean of NY W-L%
    df.loc[df["Metropolitan area"] == "Los Angeles", "W-L%"] = 0.6228945 # mean of LA W-L%
    
    # tiramos as linhas duplicadas, resetamos o índice e removemos a coluna "index"
    # remove the duplicate rows, reset the index and remove the column "index"
    df = df.drop_duplicates(subset="Metropolitan area").reset_index()
    df = df.drop(columns="index")
    
    return df

def nhl_correlation(): 
    df = clean_nhl_df()
    
    population_by_region = df["Population (2016 est.)[8]"] # pass in metropolitan area population from cities
    win_loss_by_region = df["W-L%"] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    result = stats.pearsonr(population_by_region, win_loss_by_region)
    
    return result[0]


# In[ ]:





# ## Question 2
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NBA** using **2018** data.

# In[33]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def clean_nba_df():
    nba_df = pd.read_csv("assets/nba.csv")
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1,[0,3,5,6,7,8]]
    
    cities["NBA"] = cities["NBA"].apply(lambda x: re.sub(r"\[.+\]", "", x))
    cities["NBA"] = cities["NBA"].replace({"KnicksNets": "Knicks,Nets",
                                           "LakersClippers": "Lakers,Clippers",
                                           "Trail Blazers": "Trail,Blazers"})
    
    cities["NBA"] = cities["NBA"].apply(lambda x: x.split(","))

    cities = cities.explode("NBA")

    nba_df = nba_df[nba_df["year"] == 2018]
    nba_df["team"] = nba_df["team"].apply(lambda x: re.sub(r"(\*)*\s\(\d+\)", "", x))

    nba_df["team"] = nba_df["team"].apply(lambda x: x.split(" ")[-1])

    df = pd.merge(cities, nba_df, left_on="NBA", right_on="team")
    
    df.rename(columns={"W/L%": "W-L%"}, inplace=True)
    
    df = df[["Metropolitan area", "Population (2016 est.)[8]", "NBA", "team", "W", "L", "W-L%"]]

    df["Population (2016 est.)[8]"] = df["Population (2016 est.)[8]"].astype("float")
    df["W-L%"] = df["W-L%"].astype("float")

    df.loc[df["Metropolitan area"] == "New York City", "W-L%"] = 0.3475 # mean of NY W-L%
    df.loc[df["Metropolitan area"] == "Los Angeles", "W-L%"] = 0.4695 # mean of LA W-L%
    
    df = df.drop_duplicates(subset="Metropolitan area").reset_index()
    df = df.drop(columns="index")
    
    return df

def nba_correlation():
    df = clean_nba_df()
    
    population_by_region = df["Population (2016 est.)[8]"] # pass in metropolitan area population from cities
    win_loss_by_region = df["W-L%"] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    result = stats.pearsonr(population_by_region, win_loss_by_region)
    
    return result[0]


# In[ ]:





# ## Question 3
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **MLB** using **2018** data.

# In[35]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def clean_mlb_df():
    mlb_df = pd.read_csv("assets/mlb.csv")
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1,[0,3,5,6,7,8]]
    
    cities["MLB"] = cities["MLB"].apply(lambda x: re.sub(r"\[.+\]", "", x))
    cities["MLB"] = cities["MLB"].replace({"YankeesMets": "Yankees,Mets",
                                           "DodgersAngels": "Dodgers,Angels",
                                           "GiantsAthletics": "Giants,Athletics",
                                           "CubsWhite Sox": "Cubs,White,Sox",
                                           "Red Sox": "Red,Sox",
                                           "Blue Jays": "Blue,Jays"})
    
    cities["MLB"] = cities["MLB"].apply(lambda x: x.split(","))

    cities = cities.explode("MLB")

    mlb_df = mlb_df[mlb_df["year"] == 2018]

    mlb_df["team"] = mlb_df["team"].apply(lambda x: x.split(" ")[-1])

    df = pd.merge(cities, mlb_df, left_on="MLB", right_on="team")
    
    df = df[["Metropolitan area", "Population (2016 est.)[8]", "MLB", "team", "W", "L", "W-L%"]]

    df["Population (2016 est.)[8]"] = df["Population (2016 est.)[8]"].astype("float")
    df["W-L%"] = df["W-L%"].astype("float")

    df.loc[df["Metropolitan area"] == "New York City", "W-L%"] = 0.546 # mean of NY W-L%
    df.loc[df["Metropolitan area"] == "Los Angeles", "W-L%"] = 0.529 # mean of LA W-L%
    df.loc[df["Metropolitan area"] == "San Francisco Bay Area", "W-L%"] = 0.525 # mean of SF W-L%
    df.loc[df["Metropolitan area"] == "Chicago", "W-L%"] = 0.482769 # mean of CH W-L%
    df.loc[df["Metropolitan area"] == "Boston", "W-L%"] = 0.666667 # mean of BO W-L%
    
    df = df.drop_duplicates(subset="Metropolitan area").reset_index()
    df = df.drop(columns="index")
    
    return df

def mlb_correlation():
    df = clean_mlb_df()
    
    population_by_region = df["Population (2016 est.)[8]"] # pass in metropolitan area population from cities
    win_loss_by_region = df["W-L%"] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    result = stats.pearsonr(population_by_region, win_loss_by_region)
    
    return result[0]


# In[ ]:





# ## Question 4
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NFL** using **2018** data.

# In[10]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def clean_nfl_df():
    nfl_df = pd.read_csv("assets/nfl.csv")
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1,[0,3,5,6,7,8]]
    
    cities["NFL"] = cities["NFL"].apply(lambda x: re.sub(r"\[.+\]", "", x))
    cities["NFL"] = cities["NFL"].replace({"GiantsJets": "Giants,Jets",
                                           "RamsChargers": "Rams,Chargers",
                                           "49ersRaiders": "49ers,Raiders"})
    
    cities["NFL"] = cities["NFL"].apply(lambda x: x.split(","))

    cities = cities.explode("NFL")

    nfl_df = nfl_df[nfl_df["year"] == 2018]
    nfl_df["team"] = nfl_df["team"].apply(lambda x: re.sub(r"(\*|\+)", "", x))

    nfl_df["team"] = nfl_df["team"].apply(lambda x: x.split(" ")[-1])

    df = pd.merge(cities, nfl_df, left_on="NFL", right_on="team")
    
    df = df[["Metropolitan area", "Population (2016 est.)[8]", "NFL", "team", "W", "L", "W-L%"]]

    df["Population (2016 est.)[8]"] = df["Population (2016 est.)[8]"].astype("float")
    df["W-L%"] = df["W-L%"].astype("float")

    df.loc[df["Metropolitan area"] == "New York City", "W-L%"] = 0.2815 # mean of NY W-L%
    df.loc[df["Metropolitan area"] == "Los Angeles", "W-L%"] = 0.7815 # mean of LA W-L%
    df.loc[df["Metropolitan area"] == "San Francisco Bay Area", "W-L%"] = 0.25 # mean of SF W-L%
    
    df = df.drop_duplicates(subset="Metropolitan area").reset_index()
    df = df.drop(columns="index")
    
    return df

def nfl_correlation(): 
    df = clean_nfl_df()
    
    population_by_region = df["Population (2016 est.)[8]"] # pass in metropolitan area population from cities
    win_loss_by_region = df["W-L%"] # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    result = stats.pearsonr(population_by_region, win_loss_by_region)
    
    return result[0]


# In[ ]:





# ## Question 5
# In this question I would like you to explore the hypothesis that **given that an area has two sports teams in different sports, those teams will perform the same within their respective sports**. How I would like to see this explored is with a series of paired t-tests (so use [`ttest_rel`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html)) between all pairs of sports. Are there any sports where we can reject the null hypothesis? Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this assignment.

# In[27]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df = pd.read_csv("assets/mlb.csv")
nhl_df = pd.read_csv("assets/nhl.csv")
nba_df = pd.read_csv("assets/nba.csv")
nfl_df = pd.read_csv("assets/nfl.csv")
cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1,[0,3,5,6,7,8]]

def clean_dfs():
    nfl_df = clean_nfl_df()[["Metropolitan area", "W-L%"]]
    nba_df = clean_nba_df()[["Metropolitan area", "W-L%"]]
    nhl_df = clean_nhl_df()[["Metropolitan area", "W-L%"]]
    mlb_df = clean_mlb_df()[["Metropolitan area", "W-L%"]]
    
    return (nfl_df, nba_df, nhl_df, mlb_df)

def calculate_p_values(leagues):
    p_values = pd.DataFrame(columns=leagues.keys(), index=leagues.keys())
    for (league_name1, league_df1) in leagues.items():
        for (league_name2, league_df2) in leagues.items():
            merged_league = pd.merge(league_df1, league_df2, on="Metropolitan area")
            p_values.loc[league_name1, league_name2] = stats.ttest_rel(merged_league["W-L%_x"], merged_league["W-L%_y"])[1]
            
    return p_values

def sports_team_performance():
    (nfl_df, nba_df, nhl_df, mlb_df) = clean_dfs()
    
    leagues = {"NFL": nfl_df, "NBA": nba_df, "NHL": nhl_df, "MLB": mlb_df}
    p_values_dict = calculate_p_values(leagues)
    p_values = pd.DataFrame(p_values_dict).astype("float")
    
    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    
    #sports = ['NFL', 'NBA', 'NHL', 'MLB']
    #p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)
     
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values


# In[ ]:




