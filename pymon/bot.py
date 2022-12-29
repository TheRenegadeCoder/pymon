import logging

import discord
from discord import *

from pymon import VERSION, brain, models, utils

log = logging.getLogger(__name__)


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
            query = self.brain.get_query(index)
            embed = discord.Embed(
                title=f"Pymon v{VERSION}: Answer to ID-{index}",
                color=discord.Color.red(),
                url=query.resources[0] if query.resources else None
            )
            embed.add_field(
                name=query.query,
                value=query.response,
                inline=False
            )

            similar_queries = self.brain.search(
                query.query.removesuffix("?"))[1:4]
            log.debug(f"Similar queries: {similar_queries}")
            if similar_queries:
                embed.add_field(
                    name="Similar Queries",
                    value="\n".join(
                        f"• ID-{curr.query_id}: {utils.create_md_link(curr.resources[0] if curr.resources else None, curr.query)}"
                        for curr in similar_queries
                    ),
                    inline=True
                )

            await interaction.response.send_message(embed=embed)

        @self.tree.command(
            name="study",
            description="Provides a study guide from a set of predetermined tags.",
        )
        @app_commands.choices(tag=[
            app_commands.Choice(name=item, value=item) for item in self.brain.get_tags()
        ])
        async def _study(interaction: discord.Interaction, tag: str):
            """
            Prints out a list of questions relevant to the tag.

            :param ctx: the context to send messages to
            :return: None
            """
            matches = self.brain.get_queries_by_tag(tag)
            embed = discord.Embed(
                title=f"Pymon v{VERSION}: Study Guide for {tag}",
                color=discord.Color.red(),
                description="\n".join(
                    f"• ID-{match.query_id}: {utils.create_md_link(match.resources[0] if match.resources else None, match.query)}"
                    for match in matches
                )
            )

            await interaction.response.send_message(embed=embed)

    async def _react_on_mention(self, message: Message):
        if self.user.mentioned_in(message) and not message.mention_everyone:
            queries: list[models.Query] = self.brain.search(
                message.clean_content.removeprefix("@Pymon"))
            if queries:
                reply = list()
                reply.extend([
                    f"{utils.create_md_link(query.resources[0] if query.resources else None, query.query)}"
                    for query in queries[:3]
                ])
                embed = discord.Embed(
                    title=f"Pymon v{VERSION}: Do any of these questions match your query?",
                    description="Use the ID with the /get command to get an answer or follow the available links:",
                    color=discord.Color.blue(),
                    url="https://github.com/TheRenegadeCoder/pymon"
                )
                for idx, row in enumerate(reply):
                    embed.add_field(
                        name=f"#{idx + 1}: ID-{queries[idx].query_id}",
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
