# In the task, a database dump was given in which there were 8 browsable tables. I visited all one by one, among which i found a notification table. Here i found 7 rows showing toast messages. These seemed to be a bit suspecious, and my idea was right. All the answers were in these toast messages.

Copy all the messages in an html file and format them in a readable way. Search for each answer and you will find it in this formatted file.

One tricky question was the 7th one in which we had to tell the UTC time. This time was given in the browser format in the same message header. I wrote a python script using ai to convert it into the UTC and it gave me the correct flag.
