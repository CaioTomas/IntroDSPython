#!/usr/bin/env python
# coding: utf-8

# # Assignment 2
# For this assignment you'll be looking at 2017 data on immunizations from the CDC. Your datafile for this assignment is in [assets/NISPUF17.csv](assets/NISPUF17.csv). A data users guide for this, which you'll need to map the variables in the data to the questions being asked, is available at [assets/NIS-PUF17-DUG.pdf](assets/NIS-PUF17-DUG.pdf). **Note: you may have to go to your Jupyter tree (click on the Coursera image) and navigate to the assignment 2 assets folder to see this PDF file).**

# ## Question 1
# Write a function called `proportion_of_education` which returns the proportion of children in the dataset who had a mother with the education levels equal to less than high school (<12), high school (12), more than high school but not a college graduate (>12) and college degree.
# 
# *This function should return a dictionary in the form of (use the correct numbers, do not round numbers):* 
# ```
#     {"less than high school":0.2,
#     "high school":0.4,
#     "more than high school but not college":0.2,
#     "college":0.2}
# ```
# 

# In[37]:


def proportion_of_education():
    
    import pandas as pd
    
    df = pd.read_csv('assets/NISPUF17.csv')
    
    total_kids = len(df)
    
    # coluna com a educação da mãe: EDUC1
    # eu chequei e todas as crianças têm dados de escolaridade para as mães:
    # df[df["EDUC1"].isna()] retorna um dataframe com 0 linhas
    
    # column with the data for mother education: EDUC1
    # I checked, and all children have data for their mothers' education levels:
    # df[df["EDUC1"].isna()] returns a 0 line dataframe
    
    proportion = {
        "less than high school": len(df[df["EDUC1"] == 1])/total_kids,
        "high school": len(df[df["EDUC1"] == 2])/total_kids,
        "more than high school but not college": len(df[df["EDUC1"] == 3])/total_kids,
        "college": len(df[df["EDUC1"] == 4])/total_kids
    }
    
    return proportion


# In[38]:


assert type(proportion_of_education())==type({}), "You must return a dictionary."
assert len(proportion_of_education()) == 4, "You have not returned a dictionary with four items in it."
assert "less than high school" in proportion_of_education().keys(), "You have not returned a dictionary with the correct keys."
assert "high school" in proportion_of_education().keys(), "You have not returned a dictionary with the correct keys."
assert "more than high school but not college" in proportion_of_education().keys(), "You have not returned a dictionary with the correct keys."
assert "college" in proportion_of_education().keys(), "You have not returned a dictionary with the correct keys."


# ## Question 2
# 
# Let's explore the relationship between being fed breastmilk as a child and getting a seasonal influenza vaccine from a healthcare provider. Return a tuple of the average number of influenza vaccines for those children we know received breastmilk as a child and those who know did not.
# 
# *This function should return a tuple in the form (use the correct numbers:*
# ```
# (2.5, 0.1)
# ```

# In[72]:


def average_influenza_doses():
    # coluna com a quantidade de doses de vacina pra influenza: P_NUMFLU (tem NA values)
    # coluna com a informação se já foi amamentado alguma vez: CBF_01
        # 1 -> yes
        # 2 -> no
        # 77 -> don't know
        # 99 -> missing
        # aqui não tem NA values, chequei com len(df[df["CBF_01"].isna()])
        
    # column with the amount of vaccines taken for influenza: P_NUMFLU (it has NA values)
    # column with the info if the children was breastfed: CBF_01 (it does not have NA values, checked with len(df[df["CBF_01"].isna()]))
        # 1 -> yes
        # 2 -> no
        # 77 -> don't know
        # 99 -> missing
            
    import pandas as pd
    
    df = pd.read_csv('assets/NISPUF17.csv')
    
    # não faz sentido levar em conta as crianças para as quais não temos info da vacina
    # it does not make sense to count children to whom we don't have vaccine info
    df_flu = df[df['P_NUMFLU'].isna() == False] 
    
    # dataframe só com as linhas das crianças que foram amamentadas
    # dataframe with justs the rows for breastfed children
    df_bf_1 = df_flu[(df_flu['CBF_01'] == 1)]
    
    # dataframe só com as linhas das crianças que não foram amamentadas
    # dataframe with justs the rows for non-breastfed children
    df_bf_2 = df_flu[(df_flu['CBF_01'] == 2)] 
    
    # média do primeiro tipo
    # mean for the first kind
    media_influenza_1 = df_bf_1["P_NUMFLU"].sum() / len(df_bf_1)
    
    # média do segundo tipo
    # mean for the second kind
    media_influenza_2 = df_bf_2["P_NUMFLU"].sum() / len(df_bf_2)
    
    return (media_influenza_1, media_influenza_2)


# In[73]:


assert len(average_influenza_doses())==2, "Return two values in a tuple, the first for yes and the second for no."


# ## Question 3
# It would be interesting to see if there is any evidence of a link between vaccine effectiveness and sex of the child. Calculate the ratio of the number of children who contracted chickenpox but were vaccinated against it (at least one varicella dose) versus those who were vaccinated but did not contract chicken pox. Return results by sex. 
# 
# *This function should return a dictionary in the form of (use the correct numbers):* 
# ```
#     {"male":0.2,
#     "female":0.4}
# ```
# 
# Note: To aid in verification, the `chickenpox_by_sex()['female']` value the autograder is looking for starts with the digits `0.0077`.

# In[77]:


def chickenpox_by_sex():
    # coluna com as doses de varicella: P_NUMVRC
        # aqui tem NA, não tem info pra mais da metade das crianças
            # chequei usando len(df[df["P_NUMVRC"].isna()])
    # coluna com a contração de chickenpox: HAD_CPOX
        # 1 -> sim
        # 2 -> não
        # 77, 99 -> sem info por motivos diversos
    # coluna com o sexo da criança: SEX
        # não tem NA values (ainda bem né)
        # 1 -> male
        # 2-> female
        
    # column with the varicella vaccine info: P_NUMVRC (it has NA values, almost half of the data; checked with len(df[df["P_NUMVRC"].isna()]))
    # column with the chickenpox info: HAD_CPOX
        # 1 -> yes
        # 2 -> no
        # 77, 99 -> no info for some reason
    # column with children sex: SEX (no NA values)
        # 1 -> male
        # 2 -> female
    
    import pandas as pd
    
    df = pd.read_csv('assets/NISPUF17.csv')
    
    df_vacc = df[df['P_NUMVRC'] > 0]
    
    df_cpox_1 = df_vacc[df_vacc['HAD_CPOX'] == 1] # vacinadas que tiveram
    df_cpox_2 = df_vacc[df_vacc['HAD_CPOX'] == 2] # vacinadas que não tiveram
    
    df_male_1 = df_cpox_1[df_cpox_1['SEX'] == 1] # meninos vacinados que tiveram
    df_male_2 = df_cpox_2[df_cpox_2['SEX'] == 1] # meninos vacinados que não tiveram
    
    df_female_1 = df_cpox_1[df_cpox_1['SEX'] == 2] # meninas vacinadas que tiveram
    df_female_2 = df_cpox_2[df_cpox_2['SEX'] == 2] # meninas vacinadas que não tiveram
    
    male_ratio = len(df_male_1) / len(df_male_2)
    female_ratio = len(df_female_1) / len(df_female_2)
    
    ratios = {
        "male": male_ratio,
        "female": female_ratio
    }
    
    return ratios


# In[78]:


assert len(chickenpox_by_sex())==2, "Return a dictionary with two items, the first for males and the second for females."


# ## Question 4
# A correlation is a statistical relationship between two variables. If we wanted to know if vaccines work, we might look at the correlation between the use of the vaccine and whether it results in prevention of the infection or disease [1]. In this question, you are to see if there is a correlation between having had the chicken pox and the number of chickenpox vaccine doses given (varicella).
# 
# Some notes on interpreting the answer. The `had_chickenpox_column` is either `1` (for yes) or `2` (for no), and the `num_chickenpox_vaccine_column` is the number of doses a child has been given of the varicella vaccine. A positive correlation (e.g., `corr > 0`) means that an increase in `had_chickenpox_column` (which means more no’s) would also increase the values of `num_chickenpox_vaccine_column` (which means more doses of vaccine). If there is a negative correlation (e.g., `corr < 0`), it indicates that having had chickenpox is related to an increase in the number of vaccine doses.
# 
# Also, `pval` is the probability that we observe a correlation between `had_chickenpox_column` and `num_chickenpox_vaccine_column` which is greater than or equal to a particular value occurred by chance. A small `pval` means that the observed correlation is highly unlikely to occur by chance. In this case, `pval` should be very small (will end in `e-18` indicating a very small number).
# 
# [1] This isn’t really the full picture, since we are not looking at when the dose was given. It’s possible that children had chickenpox and then their parents went to get them the vaccine. Does this dataset have the data we would need to investigate the timing of the dose?

# In[95]:


def corr_chickenpox():
    import scipy.stats as stats
    import numpy as np
    import pandas as pd
    
    df = pd.read_csv('assets/NISPUF17.csv')
    
    # this is just an example dataframe
    # df=pd.DataFrame({"had_chickenpox_column":np.random.randint(1,3,size=(100)),
    #               "num_chickenpox_vaccine_column":np.random.randint(0,6,size=(100))})

    # here is some stub code to actually run the correlation
    # corr, pval=stats.pearsonr(df["had_chickenpox_column"],df["num_chickenpox_vaccine_column"])
    
    # just return the correlation

    # filtro os NA values dos dois campos
    # filter NA values from both columns
    df_vacc = df[ ( df['P_NUMVRC'] >= 0 ) & ( df['HAD_CPOX'] <= 2 ) ]
    
    corr, pval=stats.pearsonr(df_vacc["HAD_CPOX"], df_vacc["P_NUMVRC"])
    
    return corr


# In[96]:


assert -1<=corr_chickenpox()<=1, "You must return a float number between -1.0 and 1.0."

