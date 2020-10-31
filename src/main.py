import discord, json, praw, re, asyncio
import logger, erLists

class EnforcerRed(discord.Client):

    def __init__(self):
        super().__init__()

        self.version = "0.3.5"
        self.logger = logger.Logger(debug=True, log=False, parent=self)
        
        with open('config.json', 'r') as file:
            self.settings = json.load(file)

        self.lists = erLists.initialize()

        self.reddit = praw.Reddit('erBot')
        self.subreddit = self.reddit.subreddit(self.settings['Reddit']['target'])
        self.run(self.settings['DiscordBot']['token'])



    async def on_ready(self):
        """
        Startup function.
        """
        self.logger.out_message('Initialization complete... Running bot.')
        self.loop.create_task(self.get_new_posts())

        #Create botmod list
        self.guards = [name for name in self.settings["Security"]["Guards"].split(' ') if len(name) > 2]


    async def on_message(self, message):
        if message.author == self.user:
            return

        #Convert message to command and args using ioTable
        if message.content[0] in self.ioTable:
            
            self.logger.out_message(f'Message recieved: {message.content} from {message.author}.')

            fmessage = message.content.split(' ')
            cmd, args = fmessage[0], fmessage[1:]
            func = self.ioTable[cmd[0]][cmd[1:]]
            await func(self, message, *args)

    #Auto
    async def get_new_posts(self):

        lastPost = None
        while True:         
            if self.settings["Settings"]["LiveFeedChannel"] != "":
                for post in self.subreddit.new(limit=1):

                    if lastPost != post and lastPost != None:    
                        self.logger.out_message(f'New post detected from {post.author}...')                        
                        channel = self.get_channel(self.settings["Settings"]["LiveFeedChannel"])
                        await channel.send(embed=self.post_to_embed(post, mode='full', secretMode=False)[0])

                        self.logger.out_message(f'last post set to: {post}')
                        lastPost = post
                    elif lastPost == None:
                        self.logger.out_message(f'Most recent post not new, setting last post set to: {post}')
                        lastPost = post
            
            await asyncio.sleep(self.settings["Settings"]["TickRate"])



    #Commands
    async def purge_messages(self, message, range, *args):
        """
        Purges 'range' messages in channel 'channel'
        :param range: The amount of messages to delete (including the message with the purge command)
        """
        range = int(range)
        messageNum = 0
        try:
            async for msg in message.channel.history(limit=range):
                await msg.delete()
                messageNum += 1

            self.logger.out_success(f"{messageNum} messages deleted successfully from {message.channel}")
        except Exception as e:
            await message.channel.send(f"Error printed to logs: {e}")
            self.logger.out_error(f"Exception: {e}")


    async def set_channel_live(self, message, *args):
        if "stop" in message.content:
            self.settings["Settings"]["LiveFeedChannel"] = ""
            self.logger.out_message('Live Feed Stopped...')
            return
        elif "here" in message.content:
            self.settings["Settings"]["LiveFeedChannel"] = message.channel.id
            self.logger.out_message(f'Live Feed set to {message.channel.name}')


    async def set_guard(self, message, command=None, *args):
        """
        Adds or removes guards from the guard list. 
        :param command: Whether to add or remove.
        :param *args: the list of users to add or remove
        """

        if command.lower() == 'add':
            for user in args:
                self.guards.append(user)
        elif command.lower() == 'remove':
            for user in args:
                if user in self.guards:
                    self.guards.remove(user)

        #Save updated list
        try:
            with open("config.json", 'w') as file:
                json.dump(self.settings, file)
        except Exception as e:
            self.logger.error(f'Exception: {e}')


    #Queries
    async def fetch_posts(self, message, range=5, *args):
        """
        Fetches posts from reddit and prints them to the channel it was requested in. 
        :param message: This is the message calling the command.
        :param range: The amount of posts to fetch from reddit
        """
        range = int(range)
        postLists = []
        
        for post in self.subreddit.new(limit=range):
            postLists.append(post)

        for post in postLists:
            await message.channel.send(embed=self.post_to_embed(post, mode='standard', secretMode=False)[0])
        self.logger.out_success(f'successfully fetched {range} posts.')



    async def fetch_posts_minimal(self, message, range=5, *args):
        """
        Fetches the post in a smaller, more compact style.
        :param message: the message with the command.
        :param range: the range to search.
        """
        range = int(range)
        postLists = []
        for post in self.subreddit.new(limit=range):
            postLists.append(post)

        for post in postLists:
            await message.channel.send(embed=self.post_to_embed(post, mode='compact', secretMode=False)[0])
        
        self.logger.out_success(f'successfully fetched {range} posts.')



    async def find_posts(self, message, *args):
        """
        Find posts is more of a targetted fetch, looking for specific criteria. The function takes a target string
        and determines from the string if it is a username, regex, or a search term.
        :param message: the message the command was sent in.
        :param *args: the target text.
        """

        if len(args) < 1:
            await message.channel.send(f"```Please provide a search term!\nBegin with u/ if username search.\nExample: ?find u/someUsername\n\nr/ if regex search.\nExample: ?find r/{self.settings['expressions']['outsideGroups']}\n\n plain text in quotes for text search.\nExample: ?find i need help.```")
            return

        await message.channel.send('Searching...')
        outString = " ".join(list(args))
        postList = []

        #User search
        if outString[:2] == 'u/':
            self.logger.out_message(f'searching reddit for user {outString}')
            for post in self.subreddit.new(limit=2000):
                if post.author == outString[2:]:
                    postList.append(post)
                    if len(postList) >= self.settings['Settings']['MaxSearch']:
                        break

        #Regex search
        elif outString[:2] == 'r/':
            self.logger.out_message(f'searching reddit for expression {outString}')
            for post in self.subreddit.new(limit=2000):
                if re.search(outString[2:], post.title) or re.search(outString[2:], post.selftext):
                    postList.append(post)
                    if len(postList) >= self.settings['Settings']['MaxSearch']:
                        break
        #Text search
        else:
            self.logger.out_message(f'searching reddit for string {outString}')
            for post in self.subreddit.new(limit=2000):
                if outString in post.title or outString in post.selftext:
                    postList.append(post)
                    if len(postList) >= self.settings['Settings']['MaxSearch']:
                        break

        #Print results
        if len(postList) < 1:
            self.logger.out_message(f'{outString} could not be found.')
            await message.channel.send(f'{outString} could not be found.')

        for post in postList:
            await message.channel.send(embed=self.post_to_embed(post, mode='compact', secretMode=False)[0])

        self.logger.out_success(f"Completed search for {outString}.")


    #Utility Functions

    def classify_post(self, post):
        pass

    def post_to_embed(self, post, mode='standard', color=True, secretMode=True, comments=False):
        """
        post_to_embed converts a post to an embed, but actually returns a tuple containing both
        the embed and also an "importance" int. Certain things in the post add to importance
        which can later be used to weigh up priority posts.
        :param post: the post to be converted.
        :param mode: Mode of the embed display, standard, full or compact.
        :param secret: Whether to color code the suspicious/rule breakers.
        """

        importance = 0
        
        #if Mod
        if post.author in self.subreddit.moderator():
            embedColor = discord.colour.Color.from_rgb(*self.colorTable["green"])
        else:
            embedColor = discord.colour.Color.from_rgb(*self.colorTable["blue"])
        
        #Check for predatory posts, under 13's, under 16's, etc.
        if secretMode == False:

            if ( re.search(self.settings['expressions']['outsideGroups'], post.title) or
                re.search(self.settings['expressions']['outsideGroups'], post.selftext)):
                embedColor = discord.colour.Color.from_rgb(*self.colorTable["orange"])
                importance += 1

            if ( re.search(self.settings['expressions']['predator'], post.title) or
                re.search(self.settings['expressions']['predator'], post.selftext)):
                embedColor = discord.colour.Color.from_rgb(*self.colorTable["red"])
                importance += 2

        #Check comments
        #for comment in post.comments:    
            #print(comment.author)


        #Build the embed
        try:
            embed = discord.Embed(
                                    title=post.title[:180],
                                    author=post.author,
                                    type="rich",
                                    color=embedColor
                                )

            if mode == 'standard':
                embed.description = post.selftext[:120]
            elif mode == 'full':
                embed.description = post.selftext
                embed.add_field(name='score', value=post.score, inline=False)
            embed.add_field(name='post_id', value=post.id, inline=False)
            embed.add_field(name='url', value=post.url, inline=False)
        
        except Exception as e:
            self.logger.out_error(f'Error creating embed: {e}')

        return (embed, importance)


    #Database related functions
    def db_add_user(self, message, *args):
        """
        Add user to database. Aside from actually adding the user to the database, this function
        can also take other usernames (reddit accounts) to connect to their identity.

        :param *args: list of names to provide.
        """

        if len(args) <= 0:
            self.logger.out_error('Unable to add to database: no user provided...')
            message.channel.send('Unable to add to the database! You need to provide a username to add!')
            return
        
        for username in args:

            if username[:2] != 'u/' or re.search(self.settings['expressions']['validUser'], username) == False:
                self.logger.out_error(f'Invalid user {username} added! db write aborted!')
                message.channel.send(f'username {username} not valid.. Must have either u/ to start, or digits (#0000) to end!')
                return
        
        #Checks successful. Add users
        try:
            self.db.add_user(args)
        except Exception as e:
            logger.out_error(f'Error adding to database: {e}')


    """
    The IO table is a lookup table for users to interact with the bot via a set of function pointers.
    Input commands are split into dictionary access, such as ioTable["!"]["purge"], whos value is a
    function pointer to the purge function.
    """
    ioTable = {
        "!" : {
            "purge" : purge_messages,
            "feed" : set_channel_live,
            "guard" : set_guard 
        },
        "?" : {
            "fetch" : fetch_posts,
            "tinyfetch" : fetch_posts_minimal,
            "find" : find_posts
        }
    }


    """
    The Color lookup is less about the reusing of colors and more about the ability to see (at a glance)
    what color each alert type will be using.
    """
    colorTable = {
        "green" : (120, 255, 120),
        "blue" : (50, 150, 255),
        "red" : (255, 100, 100),
        "orange" : (230, 120, 18)
    }


if __name__ == '__main__':

    erBot = EnforcerRed()
