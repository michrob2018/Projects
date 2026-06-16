#!/usr/bin/env python
# coding: utf-8

# # Exploring Hackers News Posts
# 
# In this project, we'll compare two different types of posts from Hacker News, a popular site where technology related stories (or 'posts') are voted and commented upon. The two types of posts we'll explore begin with either Ask HN or Show HN.
# 
# Users submit Ask HN posts to ask the Hacker News community a specific question, such as "What is the best online course you've ever taken?" Likewise, users submit Show HN posts to show the Hacker News community a project, product, or just generally something interesting.
# 
# We'll specifically compare these two types of posts to determine the following:
# 
# Do Ask HN or Show HN receive more comments on average?
# Do posts created at a certain time receive more comments on average?
# It should be noted that the data set we're working with was reduced from almost 300,000 rows to approximately 20,000 rows by removing all submissions that did not receive any comments, and then randomly sampling from the remaining submissions.

# In[16]:


# Read the file containing the data set
from csv import reader

### Hacker News data set ###
opened_file = open('hacker_news.csv')
read_file = reader(opened_file)
hn = list(read_file)
hn_header = hn[0]
hn = hn[1:]


# To make it easier to explore the data set, the function named explore_data() will be used to explore rows in a more readable way. There's also an option for the function to show the number of rows and columns for the data set.

# In[17]:


# Exploring the data set with an explore function
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

print(hn_header)
print('\n')
explore_data(hn, 0, 5, True)


# In[4]:


### Extracting Ask HN and Show HN Posts. ###
ask_posts = [] 
show_posts = [] 
other_posts = []

for post in hn:
    title = post[1]
    if title.lower().startswith("ask hn"):
        ask_posts.append(post)
    elif title.lower().startswith("show hn"):
        show_posts.append(post)
    else:
        other_posts.append(post)
    
print('Number of ask_post:', len(ask_posts))
print('\n')
print('Number of show_post:', len(show_posts))
print('\n')
print('Number of other_post:', len(other_posts))


# In[6]:


### Exploring Ask HN posts. ###
print(hn_header)
print('\n')
explore_data(ask_posts, 0, 5, True)


# In[7]:


### Exploring Show HN posts. ###
print(hn_header)
print('\n')
explore_data(show_posts, 0, 5, True)


# In[10]:


# Calculate the average number of comments `Ask HN` posts received.
total_ask_comments = 0

for post in ask_posts:
    total_ask_comments += int(post[4])
    
avg_ask_comments = round(total_ask_comments / len(ask_posts), 2)
print(avg_ask_comments)


# In[11]:


# Calculate the average number of comments `Show HN` posts received. 
total_show_comments = 0

for post in show_posts:
    total_show_comments += int(post[4])
    
avg_show_comments = round(total_show_comments / len(show_posts), 2)
print(avg_show_comments)


# **On average, in the data set, Ask posts receive approximately 14 comments, whereas Show posts receive approximately 10. Since Ask posts receive more comments on average, the remaining analysis will be focused just on these posts.**

# # Finding the Amount of Ask Posts and Comments by Hour Created
# 
# Now, we'll analyze if we can maximize the amount of comments an Ask post receives by creating it at a certain time. 
# 
# First, we'll find the amount of Ask posts created during each hour of day, along with the number of comments those posts received. 
# 
# Then, we'll calculate the average amount of comments Ask posts created at each hour of the day receive.

# In[12]:


# Calculate the amount of ask posts created during each hour of day and the number of comments received.
import datetime as dt

result_list = []

for post in ask_posts:
    result_list.append(
        [post[6], int(post[4])]
    )

comments_by_hour = {}
counts_by_hour = {}
date_format = "%m/%d/%Y %H:%M"

for each_row in result_list:
    date = each_row[0]
    comment = each_row[1]
    time = dt.datetime.strptime(date, date_format).strftime("%H")
    if time in counts_by_hour:
        comments_by_hour[time] += comment
        counts_by_hour[time] += 1
    else:
        comments_by_hour[time] = comment
        counts_by_hour[time] = 1

comments_by_hour


# In[13]:


# Calculate the average amount of comments `Ask HN` posts created at each hour of the day receive.
avg_by_hour = []

for hour in comments_by_hour:
    avg_by_hour.append([hour, comments_by_hour[hour] / counts_by_hour[hour]])

avg_by_hour


# # Sorting and Printing Values from a List of Lists
# 
# We'll finish by sorting the list of lists and printing the five highest values in a format that's easier to read.

# In[14]:


# Create a list that equals avg_by_hour with swapped columns.
swap_avg_by_hour = []

for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])
    
print(swap_avg_by_hour)

sorted_swap = sorted(swap_avg_by_hour, reverse=True)

sorted_swap


# In[15]:


# Sort the values and print the the 5 hours with the highest average comments.

print("Top 5 Hours for 'Ask HN' Comments")
for avg, hr in sorted_swap[:5]:
    print(
        f"{dt.datetime.strptime(hr, '%H').strftime('%H:%M')}: {avg:.2f} average comments per post"
    )


# The hour that receives the most comments per post on average is 15:00, with an average of 38.59 comments per post. There's about a 60% increase in the number of comments between the hours with the highest and second highest average number of comments.
# 
# According to the data set documentation, the timezone used is Eastern Time in the US. So, we could also write 15:00 as 3:00 pm est.
# 
# # Conclusion
# In this project, we analyzed ask posts and show posts to determine which type of post and time receive the most comments on average. Based on our analysis, to maximize the amount of comments a post receives, we'd recommend the post be categorized as ask post and created between 15:00 and 16:00 (3:00 pm est - 4:00 pm est).
# 
# However, it should be noted that the data set we analyzed excluded posts without any comments. Given that, it's more accurate to say that of the posts that received comments, ask posts received more comments on average and ask posts created between 15:00 and 16:00 (3:00 pm est - 4:00 pm est) received the most comments on average.

# In[ ]:




