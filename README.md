 <br/>
 EnforcerRed is my little discord bot to connect up a discord server to it's reddit server, specifically for admin-like roles. 
<br/><br/><br/>

 # Commands and Queries
Commands can be called with the ! prefix, and queries with the ? prefix.

## Command
* !purge 50 - Purges 50 messages.

* !feed here/stop  - The feed command can start/stop a live feed from reddit. Typing "!feed here", turns the feed on and the bot will then query reddit as often as the tick rate (config) allows and post any new posts into the channel in which the command was called. Typing "!feed stop" will turn the feed off.

<br/><br/>

## Query
* ?fetch 20 - Fetches the 20 most recent posts from the target subreddit
  
* ?tinyfetch 20 - Same as above but uses a more compact embed in discord.
  
* ?find u/testUser - The find command has 4 options. By entering a string of text, the bot will search for said string in the subreddit (titles and bodies of posts). By prefixing with a u/, the bot will search for a user. By prefixing with an r/ you can enter a regex statement and the bot will return posts with matches. Otherwise you can search a post directly with i/ to find it by postid. All of these searches will return the results saved in your max search field in the config except for i/, which will return just the 1 post that you searched for.

<br/><br/>
## Config
---

### Discord & reddit bot
In the config, the discord and reddit bot fields are fairly self explanatory. If you don't understand them, follow a tutorial for setting up the discord and reddit bot applications on your account and the details such as the clientID etc are given to you.

The only custom one is the reddit target field. This should be set to the subreddit you wish to call information from.

<br/>

### Settings

* Logfile - The value of this should be the name you want your logfile to be.
* MaxSearch - This is the default maximum amount of results returned (to help prevent the bot returning massive amounts of results and flooding your discord).
* LiveFeedChannel - This is the channel that the live feed will pump information to. By default it is an empty string which is equivelant to "off". To turn it on, refer to the !feed command.
* TickRate - This is the rate at which the live feed will check the subreddit for new posts.

<br/>

### Other settings
* expressions - Expressions is for saving long regex expressions. This is likely to change as regex expressions saved into the log file are a bad way to do things.
