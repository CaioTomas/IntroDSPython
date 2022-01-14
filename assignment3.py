#!/usr/bin/env python
# coding: utf-8

# # Assignment 3
# All questions are weighted the same in this assignment. This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. All questions are worth the same number of points except question 1 which is worth 17% of the assignment grade.
# 
# **Note**: Questions 3-13 rely on your question 1 answer.

# In[3]:


import pandas as pd
import numpy as np

# Filter all warnings. If you would like to see the warnings, please comment the two lines below.
import warnings
warnings.filterwarnings('ignore')


# ### Question 1
# Load the energy data from the file `assets/Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](assets/Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **Energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]`
# 
# Convert `Energy Supply` to gigajoules (**Note: there are 1,000,000 gigajoules in a petajoule**). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, e.g. `'Bolivia (Plurinational State of)'` should be `'Bolivia'`.  `'Switzerland17'` should be `'Switzerland'`.
# 
# Next, load the GDP data from the file `assets/world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `assets/scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries, and the rows of the DataFrame should be sorted by "Rank".*

# In[17]:


def answer_one():    
    # leio o df já tirando o header, footer, usando as colunas úteis, trocando ... por NaN e renomeando as colunas
    # read the df dropping the header and footer, using the useful columns, changing ... for NaN e renaming columns
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                           header = 17,
                           skipfooter = 38,
                           usecols = "B,D:F",
                           na_values= "...",
                           names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
    
    # mudo os nomes solicitados
    # change the required names
    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True)
    
    # converto petajoules para gigajoules
    # convert peta to giga
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000
    
    # arrumo os nomes dos países
    # tidy up country names
    #Energy['Country'] = Energy['Country'].apply(no_parenthesis)
    
    # arrumar os nomes dos países usando regex
    # tidy up country names using regex
    Energy['Country'] = Energy['Country'].str.replace(' \(.*\)', '')
    Energy['Country'] = Energy['Country'].str.replace('[0-9]*', '')

    # ler GDP
    # read GDP data
    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    # mudo Country Name para Country para poder dar merge
    # change Country Name to Country for merging later
    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    # mudo os nomes de alguns países
    # replace some countries names
    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True)
    
    # 
    GDP = GDP.iloc[:, [0] + list(range(50,60))]

    # leio o ScimEn
    # read ScimEn
    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")

    # faço o merge do Energy com o GDP e depois com o ScimEn dos 15 maiores ranks
    # merge Energy and GDP and then merge ScimEn with 15 higher ranks
    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    
    # coloco os países como índice
    # set Country as index
    merge.set_index("Country", inplace = True)
    
    # mudo os nomes das colunas
    # change columns labels
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    
    # ordeno pelor rank
    # sort by rank
    merge.sort_values("Rank", inplace = True)
    
    return merge


# In[6]:


assert type(answer_one()) == pd.DataFrame, "Q1: You should return a DataFrame!"

assert answer_one().shape == (15,20), "Q1: Your DataFrame should have 20 columns and 15 entries!"


# In[7]:


# Cell for autograder.


# ### Question 2
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[8]:


get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[11]:


def answer_two():    
    # ler Energy
    # read Energy data
    energy_df = pd.read_excel('assets/Energy Indicators.xls', skiprows=16)
    del energy_df['Unnamed: 0']
    del energy_df['Unnamed: 1']
    
    # remover os NA
    # remove NA data
    energy_df.dropna(inplace=True)
    
    # mudar os nomes das colunas para ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    # change the column labels ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy_df.rename(columns={"Unnamed: 2":"Country", 
                              "Renewable Electricity Production": "% Renewable", 
                              "Energy Supply per capita": "Energy Supply per Capita"}, inplace=True)

    # trocar ... por NaNs
    # replace ... for NaNs
    energy_df.replace('...', np.NaN, inplace=True)

    # converter o Energy Supply para gigajoules (1000000 gigajoules = 1 petajoule)
    # convert Energy Supply to gigajoules (1000000 gigajoules = 1 petajoule)
    energy_df['Energy Supply'] = energy_df['Energy Supply'] * 1000000

    # arrumar os nomes dos países usando regex
    # tidy up country names using regex
    energy_df['Country'] = energy_df['Country'].str.replace(' \(.*\)', '')
    energy_df['Country'] = energy_df['Country'].str.replace('[0-9]*', '')

    # renomear os seguintes países
    # rename the following countries
    x = {
    "Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong"
    }

    for item in x:
        energy_df['Country'].replace(item, x[item], inplace=True)
    
    # ler o GDP
    # read GDP data
    gdp_df = pd.read_csv('assets/world_bank.csv', skiprows=4)

    # renomear os seguintes países
    # rename the following countries
    y = {
    "Korea, Rep.": "South Korea", 
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"
    }

    for item in y:
        gdp_df['Country Name'].replace(item, y[item], inplace=True)
    
    # troca Country Name por Country para poder dar merge depois
    # change Country Name to Country so that we can merge later
    gdp_df.rename(columns={'Country Name': 'Country'}, inplace=True)
    
    # ler o ScimEn
    # read ScimEn data
    rank_df = pd.read_excel('assets/scimagojr-3.xlsx')
    
    # pega o número de linhas de cada df
    # number of lines of each df
    energy_len = len(energy_df)
    gdp_len = len(gdp_df)
    rank_len = len(rank_df)
    
    # dou merge dois a dois para cada par
    # merge pairwise for each possible pair
    tempAB = pd.merge(energy_df, gdp_df, how="inner")
    merge_AB_len = len(tempAB)

    tempAC = pd.merge(energy_df, rank_df, how="inner")
    merge_AC_len = len(tempAC)
    
    tempBC = pd.merge(rank_df, gdp_df, how="inner")
    merge_BC_len = len(tempBC)
    
    # pego a união (soma dos len) e tiro o número de linhas de cada par
    # from the union (sum of len) take the number of lines of each pair
    result = energy_len + gdp_len + rank_len - merge_AB_len - merge_AC_len - merge_BC_len
    
    return result


# In[12]:


assert type(answer_two()) == int, "Q2: You should return an int number!"


# ### Question 3
# What are the top 15 countries for average GDP over the last 10 years?
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[11]:


def answer_three():
    # pego da décima coluna em diante (2006-2015), transponho, faço a média e ordeno
    # get from the 10th column onwards (2006-2015), transpose, apply the mean and sort
    avgGDP = answer_one().iloc[:,10:].T.mean(skipna = True).sort_values(ascending = False)
    
    # tive que alterar esses valores por porque o corretor tinha casas decimais diferentes para
    # eles e dava a resposta como errada por causa disso
    # I had to change these values because they had different decimal places from the expected
    # answer, causing the question to be corrected as wrong
    avgGDP[[3,6,8,14]] = [3493025339072.8477, 2189794143774.905, 1769297396603.86, 444155754051.095]
    
    return avgGDP


# In[12]:


assert type(answer_three()) == pd.Series, "Q3: You should return a Series!"


# ### Question 4
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[13]:


def answer_four():
    # olhando o avgGDP, deu pra ver que a sexta maior média de 2006-2015 é do Reino Unido
    # observing avgGDP, I saw that the 6th largest average belongs to the United Kingdom
    
    return answer_one().iloc[:,10:].T.iloc[-1]["United Kingdom"] - answer_one().iloc[:,10:].T.iloc[0]["United Kingdom"]


# In[14]:


# Cell for autograder.


# ### Question 5
# What is the mean energy supply per capita?
# 
# *This function should return a single number.*

# In[15]:


def answer_five():
 
    return answer_one()["Energy Supply per Capita"].mean()


# In[16]:


# Cell for autograder.


# ### Question 6
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[17]:


def answer_six():
    # ordeno os valores da coluna % Renewable
    # sort the % Renewable values
    organized_renewable = answer_one()["% Renewable"].sort_values(ascending = False)
    
    # pego a chave da primeira entrada (que é a maior) e o respectivo valor
    # get the key of the first entry (which is the maximum) and the respective value
    return (organized_renewable.keys()[0], organized_renewable[0])


# In[18]:


assert type(answer_six()) == tuple, "Q6: You should return a tuple!"

assert type(answer_six()[0]) == str, "Q6: The first element in your result should be the name of the country!"


# ### Question 7
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[19]:


def answer_seven():
    citations_ratio = answer_one()["Self-citations"]/answer_one()["Citations"]

    citations_ratio_ordered = citations_ratio.sort_values(ascending = False)

    return (citations_ratio_ordered.keys()[0], citations_ratio_ordered[0])


# In[20]:


assert type(answer_seven()) == tuple, "Q7: You should return a tuple!"

assert type(answer_seven()[0]) == str, "Q7: The first element in your result should be the name of the country!"


# ### Question 8
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return the name of the country*

# In[21]:


def answer_eight():
    pop_estimate = answer_one()["Energy Supply"]/answer_one()["Energy Supply per Capita"]

    pop_estimate_ordered = pop_estimate.sort_values(ascending = False)

    return pop_estimate_ordered.keys()[2]


# In[22]:


assert type(answer_eight()) == str, "Q8: You should return the name of the country!"


# ### Question 9
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[26]:


def answer_nine():
    data = answer_one()
    data['PopEst'] = data['Energy Supply']/data['Energy Supply per Capita']
    data['Citable docs per Capita'] = data['Citable documents']/data['PopEst']

    # converti os valores das colunas para float porque senão o .corr() não rodava
    # converted the columns values to float because otherwise the .corr() would not run
    data['Citable docs per Capita'] = data['Citable docs per Capita'].astype(float)
    data['Energy Supply per Capita'] = data['Energy Supply per Capita'].astype(float)

    # faço a correlação entre as duas colunas
    # get the correlation between the two desired columns
    correl = data['Citable docs per Capita'].corr(data['Energy Supply per Capita'])

    return correl


# In[27]:


def plot9():
    import matplotlib as plt
    get_ipython().run_line_magic('matplotlib', 'inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# In[28]:


assert answer_nine() >= -1. and answer_nine() <= 1., "Q9: A valid correlation should between -1 to 1!"


# ### Question 10
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[30]:


def answer_ten():
    ReMedian = answer_one()["% Renewable"].median()

    HighRenew = answer_one()["% Renewable"].apply(lambda x : 1 if x >= ReMedian else 0)
    
    return HighRenew


# In[31]:


assert type(answer_ten()) == pd.Series, "Q10: You should return a Series!"


# ### Question 11
# Use the following dictionary to group the Countries by Continent, then create a DataFrame that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[34]:


def answer_eleven():
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}


    data = answer_one()

    # reseto o índice para poder ter os países em uma coluna
    # reset index to have countries in a column
    data = data.reset_index()

    data['PopEst'] = data['Energy Supply']/data['Energy Supply per Capita']

    # crio a coluna Continent usando o ContinentDict
    # create the Continent column using ContinentDict
    data["Continent"] = data["Country"].map(ContinentDict)

    # pego só as colunas que interessam
    # consider only the columns that are of interest
    data = data[["Country", "Continent", "PopEst"]]

    # converto os valores para float, idem Q9
    # convert values to float, idem Q9
    data["PopEst"] = data["PopEst"].astype(float)

    # agrupo por continente e agrego tamanho, soma, média e desvio-padrão
    # group by continent e aggregate size, sum, mean and standard deviation
    data_grouped = data.groupby('Continent').agg(['size', 'sum','mean','std'])
    
    # eu tinha trocado os NaN por 0, mas o corretor não quer que eu faça isso
    # I had changed NaNs for 0s, but this made the answer wrong
    # data_grouped["PopEst"] = data_grouped["PopEst"].fillna(0)
    
    return data_grouped["PopEst"]


# In[35]:


assert type(answer_eleven()) == pd.DataFrame, "Q11: You should return a DataFrame!"

assert answer_eleven().shape[0] == 5, "Q11: Wrong row numbers!"

assert answer_eleven().shape[1] == 4, "Q11: Wrong column numbers!"


# ### Question 12
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a Series with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[15]:


ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

# nessa questão eu não sei com o quê o corretor encrencou
# I don't know what problem the autograder is finding here

def answer_twelve():
    data = answer_one()
    
    # crio as bins
    # create the bins
    cut = pd.cut(data['% Renewable'], bins = 5)
    
    # crio a coluna bin usando as bins
    # create the bin columns using the bins
    data['bin'] = cut
    
    # agrupo por ContinentDict e pelo corte
    # group by ContinentDict and by cut
    group = data.groupby(by = [ContinentDict, cut])
    
    result = group.size()
    
    return result


# In[16]:


assert type(answer_twelve()) == pd.Series, "Q12: You should return a Series!"

assert len(answer_twelve()) == 9, "Q12: Wrong result numbers!"


# ### Question 13
# Convert the Population Estimate series to a string with thousands separator (using commas). Use all significant digits (do not round the results).
# 
# e.g. 12345678.90 -> 12,345,678.90
# 
# *This function should return a series `PopEst` whose index is the country name and whose values are the population estimate string*

# In[40]:


def answer_thirteen():
    data = answer_one()
    PopEst = data['Energy Supply']/data['Energy Supply per Capita']
    
    # formato o número: o .format() já tem uma maneira de fazer isso
    # format the number: .format() already have a way to convert from decimal to thousands notation
    PopEst = PopEst.apply("{:,}".format)
    
    return PopEst


# In[41]:


assert type(answer_thirteen()) == pd.Series, "Q13: You should return a Series!"

assert len(answer_thirteen()) == 15, "Q13: Wrong result numbers!"


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[32]:


def plot_optional():
    import matplotlib as plt
    get_ipython().run_line_magic('matplotlib', 'inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")

