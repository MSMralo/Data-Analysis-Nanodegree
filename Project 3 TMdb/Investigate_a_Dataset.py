#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate TMDb Movies Data
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# >    **In this analysis we are going to investigate TMDb movies database. The database contains all movies data from 1960 to 2015 and has specific details about every movie such as title, budget, revenue, year of release, runtime and generes.**
# 
# >    **We will investigate the database to find out the top 5 years of highest average spending on film production and the movies most spent on in these years.
# Also, we will explore the movies with the heighest revenues of all time and the relation between those movies budgets and revenue.**

# In[58]:


#importing all needed packages for the analysis 
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# > **In this section we will do the following**
#    <lo>
#         <li>load the TMdb database file</li>
#         <li>explore database header, first and last few rows</li>
#         <li>finding columns information such as the column data type and the mean of its values</li>
#         <li>counting duplicates and empty rows</li>
#    </lo>
# </a>
# ### General Properties

# In[59]:


#reading the TMDb database file tmdb-movies.csv
df = pd.read_csv('tmdb-movies.csv')
#checking the data header and first few rows
df.head()


# In[60]:


#checking the data header and last few rows
df.tail()


# In[61]:


#checking data types/counts/empty cells
df.info()


# In[62]:


#checking the data describe for getting an overview on the mean/min/max values of each column
df.describe()


# In[63]:


#counting duplicates rows
sum(df.duplicated())


# In[64]:


#exploring duplicated rows 
df[df.duplicated()]


# ### Data Cleaning 
# > **In our data cleaning we will drop and trim parts of the data we won't be using in our analysis**
#     <lo>
#     <li>dropping all columns we won't use in our analysis </li>
#     <li>trimming duplicated rows as it won't help in giving us better results</li>
#     <li>making sure that movies with no or zero budget or revenue is not under one category by using histograms</li>
#     <li>dropping rows that has no data about movie budget or revenue so it doens't mess our analysis</li>
#     <li>checking that the data is clean and no more errors before starting the analysis</li>
#     </lo>
# 

# In[65]:


#dropping all the columns we won't be using in this analysis
df.drop(['id','imdb_id','cast', 'director','homepage','tagline',
         'overview','keywords','production_companies','genres',
         'release_date','vote_count','budget','revenue'], axis=1, inplace= True)


# In[66]:


#dropping all duplicated rows
df.drop_duplicates(inplace=True)


# In[67]:


#checking agian data types/counts/empty cells
df.info()


# In[68]:


#checking the data header and first few rows after cleaning
df.head()


# In[69]:


#checking the data describe for getting an overview on the mean/min/max values of each column
df.describe()


# In[70]:


#taking a look on budget zero values movies data as it exceeds 50% of the data
df.query('budget_adj ==0.0')


# In[71]:


#taking a look on budget zero values movies histograms as it exceeds 50% of the movies data
df.query('budget_adj ==0.0').hist()


# > histograms shows that Zero budget values are not just in one category and its spreaded over the years

# In[72]:


#checking if movies with zero values budget in a specific group of years
df.query('revenue_adj ==0.0').groupby('release_year')['release_year'].count()


# In[73]:


#drop zero values from a specific column with this funiction
def drop_zero_vals(column):
    df[column]= df[column].replace(0.0, np.NaN)
    df.dropna(inplace= True)


# In[74]:


#drop movies with zero budget/revenue as it won't help with our analysis
drop_zero_vals('budget_adj')
drop_zero_vals('revenue_adj')


# In[75]:


#making sure our data is totally clean before starting our analysis
df.head()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > **In this section**: We will use the cleaned data from the previous section and build our analysis using data visualization to build plots to compare between movies budgets through the years. Also, we will find top movies with highest revenues of all time and compare the relation between its budget and revenue statiscs.
# 
# ### What are the highest years in average spending on film production? and which movies most spent on in the top 5 years?
# 
# 

# In[76]:


#finding the average budget of each movie in each year 
#by getting the mean of grouping release_year column and saving the results in budget_data
budget_data= df.groupby(['release_year']).mean()['budget_adj']


# In[77]:


#buidling a bar plot to see the average movies budget throught the years
budget_data.plot(kind='bar')
#setting the ticks and distance between them on x-axis as well as rotation
plt.xticks(range(0,56,5),range(1960,2020,5) ,rotation=45)
#setting plot name
plt.title('Average Spending on Film Production')
#naming y and x lables
plt.ylabel('Average Budget (10 millions)')
plt.xlabel('Release Year')
#showing the plot
plt.show()


# > **Average spending on Film Production**
# <lo>
#     <li>Movies average budgets changed over the years making a maximum value of 81 million dollars in 1965 and a lowest value of 15 million dollars in 1972.</li>
#     <li>The average movies budgets of all time is 40 million dollars</li>
#     <li>Movies budgets is clearly higher in the period of 1997-2015 compared to the period time of 1960-1996.</li>
# </lo>
#    

# In[78]:


#building the data using a line curve for better overview about the up and down time periods in movies budgets
budget_data.plot()
#setting plot name
plt.title('Average Spending on Film Production')
#naming y and x lables
plt.ylabel('Average Budget (10 millions)')
plt.xlabel('Release Year')


# > **Average spending on Film Production: The line Curve shows:**
# <lo>
#     <li>Significant gradually increase in movies budgets from 1970 to 1997.</li>
#     <li>Gradually slightly decrease from 1997 to 2015.</li>
# </lo>

# In[79]:


#getting movies average budget of all years
budget_data.mean()


# In[80]:


#sorting budgets to see the top movies budgets
budget_data.sort_values(ascending=False).head()


# In[81]:


#this function is taking one parameter (years) and returning the name
#of movie with the highest budget in this year
def get_max_movie(year):
    max_budget = df[df['release_year'] == year].max()['budget_adj']
    max_row = df[df['budget_adj'] == max_budget]
    movie_name = max_row['original_title']
    return movie_name


# #### Getting movies with the highest budget in 1963, 1965, 1997, 1998 and 2000 years by calling the function get_max_movie(year) for each year

# In[82]:


get_max_movie(1963)


# In[83]:


get_max_movie(1965)


# In[84]:


get_max_movie(1997)


# In[85]:


get_max_movie(1998)


# In[86]:


get_max_movie(2000)


# ### What are the movies with the heighest revenues ? and the relation between those movies budgets and revenue?  

# In[87]:


#sorting revenue to see the top movies revenues
df.sort_values('revenue_adj',ascending=False).head()


# In[88]:


#storing top 5 highest revenue movies rows in data
data= df.sort_values('revenue_adj',ascending=False).head()

#storing its budgets in movies_budget
movies_budget = data['budget_adj']
#storing its revenues in  movies_revenue
movies_revenue = data['revenue_adj']

#storing movies names in labels to use on X-axis
labels =data['original_title']


# In[89]:


x = np.arange(5)  # label locations
width = 0.35  # width of the bars
fig, ax = plt.subplots()
#building bars for each budget and revenue for comparison
budget = ax.bar(x - width/2, movies_budget, width, label='Budget')
revenue = ax.bar(x + width/2, movies_revenue, width, label='Revenue')

#setting y and x lables
ax.set_ylabel('Money (billions) ')
ax.set_xlabel('Movies')

#setting histogram title
ax.set_title('Relation between Movies Budgets and Revenue')
#setting ticks distances
ax.set_xticks(x)
#setting x ticks
ax.set_xticklabels(labels)
#showing legneds names
ax.legend()
#using tight layout for lables to show clearly
fig.tight_layout()
plt.show()


# > **Relation between Movies Budgets and Revenue: The bar curve shows:**
# <lo>
#     <li>Significant revenue rates compared to the movies budgets which exceeds 1000% in some movies</li>
#     <li>Although, the Star Wars movie has less than half of the Titanic budget, the Star Wars got much higher revenue than Titanic</li>
#     <li>Jaws and The Exorcist movies has nearly the same budget as Star Wars but got much less revenue in return</li>
# </lo>

# <a id='conclusions'></a>
# ## Conclusions
# 
# > **From Our Analysis** We found that the highest average years of spending on film production are 1963, 1965, 1997 ,1998 and 2000 and each movie budget starting from 57 million dollars in years 1998 and 2000 also, reached a maximum point in 1963 with 81 million dollars budget and an average budget of all times of 39.9 million dollars.
# 
# > **highest budget movies** 
#     <lo>
#         <li>in 1963 : Cleopatra</li>
#         <li>in 1965 : The Greatest Story Ever Told</li>
#         <li>in 1997 : Titanic</li>
#         <li>in 1998 : Armageddon, Lethal Weapon 4</li>
#         <li>in 2000 : Dinosaur</li>
#     </lo>
# 
# > **highest revenues movies of all time**
#     <lo>
#         <li>Avatar : 2.82 billions dollars in 2009 with 7.1 average rate</li>
#         <li>Star Wars : 2.78 billions dollars in 1977 with 7.9 verage rate</li>
#         <li>Titanic : 2.5 billions dollars in 1997 with 7.3 average rate</li>
#         <li>The Exorcist : 2.16 billions dollars in 1973 with 7.2 average rate</li>
#         <li>Jaws : 1.9 billions dollars in 1975 with 7.3 average rate</li>
#     </lo>
# 
# > **From the 'Relation between Movies Budgets and Revenue' histogram:**
# <lo>
#     <li>higher budget value doesn't mean always a higher revenue. </li>
#     <li>Although, the Star Wars movie has less than half of the Titanic budget, the Star Wars got much higher revenue than Titanic</li>
#     <li>Avatar's budget is 240 millions which is much higher than Star Wars that has budget of only 39 millions even though Star Wars got nearly the same revenue of 2.8 billion dollars as Avatar.</li>
# </lo>
# 
# > **Limitation: 
# This analysis has some limitation that might affect the results if not exsit due to:**
# <lo>
#     <li>Missing movies budget and revenue values of about 50% of TMdb database</li>
#     <li>Only using movies released between 1960 to 2015 and in the TMdb database, so the last 4 years movies are not included</li>
#     <li>Movies budgets and revenues is adjusted to 2010 dollars, accounting for inflation over time and not recently adjusted or updated.
#  </li>
# </lo>    

# In[90]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




