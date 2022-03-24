import os

import discord
from discord import Message
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

import pymon_utils as utils

__version__ = "0.4.0"


# Global variables
client = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name='student questions'
    ),
    status=discord.Status.idle
)
slash = SlashCommand(client, sync_commands=True)
queries, keyword_mapping = utils.refresh_knowledge()


# Discord bot code
async def _react_on_mention(message: Message):
    if client.user.mentioned_in(message):
        indices = utils.search(keyword_mapping, utils.generate_keywords(message.content))
        if indices:
            reply = list()
            reply.extend([
                f"{utils.create_md_link(queries[i].get('resource'), queries[i].get('query'))}"
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


@client.event
async def on_message(message: Message):
    """
    The action to be called when a message is sent.

    :param message: the message to scrutinize
    :return: None
    """
    if message.author != client.user:
        await _react_on_mention(message)


@slash.slash(
    name="get",
    description="Looks up the answer to a query by its ID.",
    options=[
        create_option(
            name="index",
            description="Select a question index",
            option_type=4,
            required=True
        )
    ]
)
async def _get(ctx, index: int):
    """
    Looks up the answer to a query by its ID.

    :param ctx: the context to send messages to
    :return: None
    """
    embed = discord.Embed(
        title=f"Pymon v{__version__}: Answer to ID-{index}",
        color=discord.Color.red(),
        url=queries[index].get("resource", discord.embeds.EmptyEmbed)
    )
    embed.add_field(
        name=queries[index].get("query"),
        value=queries[index].get("response"),
        inline=False
    )
    similar_queries = queries[index].get("similar_queries", [])[:3]
    if similar_queries:
        embed.add_field(
            name="Similar Queries",
            value="\n".join(
                f"• ID-{i}: {utils.create_md_link(queries[i].get('resource'), queries[i].get('query'))}"
                for i in similar_queries
            ),
            inline=True
        )

    await ctx.send(embed=embed)


@slash.slash(
    name="refresh",
    description="Refreshes the bot's knowledge base.",
)
async def _refresh(ctx):
    """
    Refreshes the bot's knowledge base.

    :param ctx: the context to send messages to
    :return: None
    """
    new_queries, new_keyword_mapping = utils.refresh_knowledge()
    global queries, keyword_mapping
    diff = [x for x in new_queries if x not in queries]
    queries, keyword_mapping = new_queries, new_keyword_mapping
    await ctx.send(f"{len(diff)} queries modified and/or added.")


client.run(os.environ.get("DISCORD_TOKEN"))
