#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('conda install -yc conda-forge ipython-sql')


# In[3]:


get_ipython().run_cell_magic('capture', '', '%load_ext sql\n%sql sqlite:///factbook.db')


# In[4]:


get_ipython().run_cell_magic('sql', '', "SELECT *\nfrom sqlite_master\nWHERE type='table';")


# In[5]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nfrom facts\nLIMIT 5;')


# In[6]:


get_ipython().run_cell_magic('sql', '', 'SELECT MIN(population), MAX(population), MIN(population_growth), MAX(population_growth)\nfrom facts')


# In[7]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\n  FROM facts\n WHERE population == (SELECT MAX(population)\n                        FROM facts\n                     );')


# In[9]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM facts\nWHERE population==(SELECT MAX(population) from facts)')


# In[25]:


get_ipython().run_cell_magic('sql', '', 'SELECT MIN(population), MAX(population), MIN(population_growth), MAX(population_growth)\nfrom facts\nWHERE population <> (SELECT MAX(population) from facts) OR 0;')


# In[27]:


get_ipython().run_cell_magic('sql', '', "SELECT AVG(population),AVG(area)\nfrom facts\nWHERE name <> 'World';")


# In[29]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nfrom facts\nWHERE population > (SELECT AVG(population) from facts) AND area < (SELECT AVG(area) from facts);')


# In[31]:


get_ipython().run_cell_magic('sql', '', "SELECT name\nfrom facts\nWHERE population == (SELECT MAX(population) from facts WHERE name <> 'World')")


# In[35]:


get_ipython().run_cell_magic('sql', '', "SELECT name, MAX(population*population_growth)\nfrom facts\nWHERE name <> 'World'")


# In[ ]:




