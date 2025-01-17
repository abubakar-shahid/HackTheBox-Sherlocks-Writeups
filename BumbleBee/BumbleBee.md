# BumbleBee

## Challenge Information
- **Challenge Name**: BumbleBee
- **Category**: Log Analysis
- **Difficulty Level**: Easy

## Investigation Steps

0. First of all, I opened the logs file and the db dump on kali. The db file opened in db browser where all the information of the database was available. I opened the logs file in cursor and got a thorough overview of the file using ai.

1. For the first task, i analyzed the tables of the database in which there was a `users` table as well. in that table, there was a user in the last, since when the database dump got captured, the victim would be last registered user. Hence, this guess was correct and `apoole1` was the answer.

2. The ipaddress of the attacker was also present in the same table `10.10.0.78`.

3. Each user in the database was given a unique `userid`. For the last post by the attacker, i visited the posts table in the database and there was a post against the unique userid, and hence found the required `post_id=9`.

4. In the `posts` table, the `post_text` column contained some html and js code. I copied that code and pasted it in an html file to see it in a formatted way. Here i observed two forms in which one malicious form gave call to a link when the malicious js function executed. this link `http://10.10.0.78/update.php` was the required flag for this part.

5. In the logs file, we can observe that the request initiated at `11:53:12` is a post request to get the admin index page, and the response to this request is also successful. So this was the time when the attacker successfully logged as an admin. This time is according to the `Africa/Algiers` time. To change it into UTC, subtract 1 hour since the time is `26/Apr/2023:11:53:12 +0100` where we can observe `+0100` representing the difference with UTC. Hence the answer is `26/04/2023 10:53:12`.

6. The plain text password for the `LDAP` connection can be found in the `config` table of the database. We can also use the filter of `ldap` when browsing in the tables.

7. The user agent information `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36` refers to the browser that the attacker was using at that time. It is present in the successful login request as an admin, in the logs file.

8. In the post request at time `26/Apr/2023:11:53:51 +0100`, we can observe that the attacker is now trying to manage something, which will be most probably adding something. Here, he is adding himself to admins. So the flag is subtracting 1 hour from the highlighted time, in required format.

9. Similarly, the time when the database copy was saved, can be observed at `26/Apr/2023:12:01:38 +0100`.

10. The size for the backup file `34707` is also present in the request, where the file is being sent to the required destination.
