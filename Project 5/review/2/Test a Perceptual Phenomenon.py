#!/usr/bin/env python
# coding: utf-8

# ### Analyzing the Stroop Effect
# (1) What is the independent variable? What is the dependent variable?

# >**Independant variable:**  the word condition congruent or congruent 
#  <br>**Dependant variable:** time taken to choose between the word conditions

# (2) What is an appropriate set of hypotheses for this task? Specify your null and alternative hypotheses, and clearly define any notation used. Justify your choices.

# >$H_0 : \mu_{incongruent} >= \mu_{congruent} $ <br>
# >$H_1 : \mu_{congruent} > \mu_{incongruent} $

# The $\mu_{incongruent}$ means the average time taken for reading incongruent words across the population.<br>
# The $\mu_{congruent}$ means the average time taken for reading congruent words across the population.<br>
# our null hypotheses suggests that the average of time taken for incongruent word condition is heigher than or equal to the time taken for reading congruent words condition. <br>
# our Alternative suggests that the average of time taken for congruent word condition is heigher than the time taken for reading incongruent words condition.
# The test is one tail since we are testing one direction.
# we used t-test because the sample is too small and we will use parid t-test since our data is for one group of people who done the same test twice.

# (3) Report some descriptive statistics regarding this dataset. Include at least one measure of central tendency and at least one measure of variability. The name of the data file is 'stroopdata.csv'.

# In[12]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

df = pd.read_csv('stroopdata.csv')
df.head()


# In[13]:


df.info()


# >Getting congruent and incongruent mean and median to see which of them are higher

# In[14]:


df.Congruent.mean()


# In[15]:


df.Congruent.median()


# In[16]:


df.Incongruent.mean()


# In[17]:


df.Incongruent.median()


# In[18]:


np.std(df)


# In[19]:


np.var(df)


# >**From the numbers showing above we see that there is signficant difference in the time people take to read Incongruent words and Congruent words.
# The mean and median shows that Incongruent words takes people more time to read than Congruent by 8 seconds in average.**

# (4) Provide one or two visualizations that show the distribution of the sample data. Write one or two sentences noting what you observe about the plot or plots.

# In[20]:


plt.hist(df.Congruent, alpha= 0.3, label ='Congruent')
plt.hist(df.Incongruent, alpha= 0.3, label='Incongruent')
plt.title('Time people take to read Congruent VS Incongruent clored words')
plt.xlabel('Seconds')
plt.ylabel('People')
plt.legend()


# >in the plot above it shows a signficant difference in time taken by people to read words of Incongruent than Congruent words.<br>
# most people take 15 seconds to read Congruent words and 22 seconds to read Incongruent words.<br>
# we can also see that there are 2 people who takes them much more time to read the Incongruent words more than the rest of people by at least 7 seconds.

# In[21]:


plt.hist(df.Incongruent- df.Congruent, alpha= 0.3)
plt.title('Differnece in Time people take to read Congruent and Incongruent clored words')
plt.xlabel('Seconds')
plt.ylabel('People')
plt.legend()


# >in the histogram above it shows that all people takes less time to finish reading Congruent words comparing to reading Incongruent words and most of people takes 2 to 12 seconds more to finish the Incongruent words reading.

# (5)  Now, perform the statistical test and report your results. What is your confidence level or Type I error associated with your test? What is your conclusion regarding the hypotheses you set up? Did the results match up with your expectations? **Hint:**  Think about what is being measured on each individual, and what statistic best captures how an individual reacts in each environment.

# In[22]:


import scipy.stats as stats
stat, p_value = stats.ttest_rel(df.Incongruent, df.Congruent)


# In[23]:


p_value/2


# In[24]:


stat


# **The p_value is too small which suggests that the average time people take in reading Incongruent words are less than reading Congruent words. <br>
# since the p_value is less than the alpha (0.05) then we have enough evidence to reject the null.**

# (6) What do you think is responsible for the effects observed? Can you think of an alternative or similar task that would result in a similar effect? Some research about the problem will be helpful for thinking about these two questions!

# **It might happen for several reason and primarly practicing, someone who is reading this for the first time might get confused easily but someone who have done this thousands of times might not feel any difference.<br>
# An example of similar case a baby might take 1 minute or more to walk for 10 meters while he can do the same in few seconds when he grow up.**

# In[ ]:





# In[ ]:




