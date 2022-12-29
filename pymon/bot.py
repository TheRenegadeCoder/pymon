import discord
from discord import *

from pymon import utils, brain


class Pymon(discord.Client):
    """
    A discord bot for my programming courses.
    """

    def __init__(self,) -> None:
        intents = discord.Intents.default()
        super().__init__(
            intents=intents,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name='student questions'
            ),
            status=discord.Status.idle
        )
        self.tree = app_commands.CommandTree(self)
        self.brain = brain.Brain()
        self.queries, self.keyword_mapping = utils.refresh_knowledge()

    async def on_ready(self):
        """
        Launches when the bot is ready to go.

        :return: None
        """
        self.add_slash_commands()

    async def on_message(self, message: Message):
        """
        The action to be called when a message is sent.

        :param message: the message to scrutinize
        :return: None
        """
        if message.author != self.user:
            await self._react_on_mention(message)

    def add_slash_commands(self):
        """
        A helper method which gives the tree commands access to self.
        All tree commands should go here.
        """

        @self.tree.command(
            name="get",
            description="Looks up the answer to a query by its ID.",
        )
        async def _get(interaction: discord.Interaction, index: int):
            """
            Looks up the answer to a query by its ID.

            :param ctx: the context to send messages to
            :return: None
            """
            embed = discord.Embed(
                title=f"Pymon v{__version__}: Answer to ID-{index}",
                color=discord.Color.red(),
                url=self.queries[index].get(
                    "resource", discord.embeds.EmptyEmbed)
            )
            embed.add_field(
                name=self.queries[index].get("query"),
                value=self.queries[index].get("response"),
                inline=False
            )
            similar_queries = self.queries[index].get(
                "similar_queries", [])[:3]
            if similar_queries:
                embed.add_field(
                    name="Similar Queries",
                    value="\n".join(
                        f"• ID-{i}: {utils.create_md_link(self.queries[i].get('resource'), self.queries[i].get('query'))}"
                        for i in similar_queries
                    ),
                    inline=True
                )

            await interaction.response.send_message(embed=embed)

        @self.tree.command(
            name="study",
            description="Provides a study guide from a set of predetermined tags.",
        )
        @app_commands.choices(tag=[
            app_commands.Choice(name=item, value=item) for item in sorted(utils.generate_tags_set(self.queries))
        ])
        async def _study(interaction: discord.Interaction, tag: str):
            """
            Prints out a list of questions relevant to the tag.

            :param ctx: the context to send messages to
            :return: None
            """
            matches = utils.get_queries_from_tag(self.queries, tag)
            embed = discord.Embed(
                title=f"Pymon v{__version__}: Study Guide for {tag}",
                color=discord.Color.red(),
                description="\n".join(
                    f"• ID-{match[0]}: {utils.create_md_link(match[1].get('resource'), match[1].get('query'))}"
                    for match in matches
                )
            )

            await interaction.response.send_message(embed=embed)

        @self.tree.command(
            name="refresh",
            description="Refreshes the bot's knowledge base.",
        )
        async def _refresh(interaction: discord.Interaction):
            """
            Refreshes the bot's knowledge base.

            :param ctx: the context to send messages to
            :return: None
            """
            new_queries, new_keyword_mapping = utils.refresh_knowledge()
            diff = [x for x in new_queries if x not in self.queries]
            self.queries, self.keyword_mapping = new_queries, new_keyword_mapping
            await interaction.response.send_message(f"{len(diff)} queries modified and/or added.")

    async def _react_on_mention(self, message: Message):
        if self.user.mentioned_in(message) and not message.mention_everyone:
            indices = utils.search(self.keyword_mapping, utils.generate_keywords(message.content))
            if indices:
                reply = list()
                reply.extend([
                    f"{utils.create_md_link(self.queries[i].get('resource'), self.queries[i].get('query'))}"
                    for i in indices[:3]
                ])
                embed = discord.Embed(
                    title=f"Pymon v{__version__}: Do any of these questions match your query?",
                    description="Use the ID with the /get command to get an answer or follow the available links:",
                    color=discord.Color.blue(),
                    url="https://github.com/TheRenegadeCoder/pymon"
                )
                for idx, row in enumerate(reply):
                    embed.add_field(
                        name=f"#{idx + 1}: ID-{indices[idx]}",
                        value=row,
                        inline=True
                    )
                embed.set_footer(
                    text="Learn more about how this bot works by clicking the title.",
                    icon_url="https://therenegadecoder.com/wp-content/uploads/2017/05/the-renegade-coder-icon-cropped.png"
                )
                await message.reply(embed=embed)
            else:
                await message.reply("How about we explore the area ahead of us later? https://tenor.com/bqnuv.gif")
