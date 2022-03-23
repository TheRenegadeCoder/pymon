import json
import os

from code_bot_utils import *

import discord
from discord import Message

from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv


__version__ = "0.2.0"


# Global variables
client = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f'student questions'
    ),
    status=discord.Status.idle
)
slash = SlashCommand(client, sync_commands=True)
load_dotenv()
queries = load_knowledge()
keyword_mapping = generate_keyword_mapping(queries)
generate_similar_queries(queries, keyword_mapping)


# Discord bot code
async def _react_on_mention(message: Message):
    if client.user.mentioned_in(message):
        indices = search(keyword_mapping, generate_keywords(message.content))
        if indices:
            reply = list()
            reply.extend([
                f"{create_md_link(queries[i].get('resource'), queries[i].get('query'))}"
                for i in indices[:3]
            ])
            embed = discord.Embed(
                title=f"CS Query Bot v{__version__}: Do any of these questions match your query?",
                description="Use the ID with the /get command to get an answer or follow the available links:",
                color=discord.Color.blue(),
                url="https://github.com/TheRenegadeCoder/cs-query-bot"
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
        title=f"CS Query Bot v{__version__}: Answer to ID-{index}",
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
            name=f"Similar Queries",
            value="\n".join(f"• ID-{i}: {create_md_link(queries[i].get('resource'), queries[i].get('query'))}" 
                for i in similar_queries
            ),
            inline=True
        )

    await ctx.send(embed=embed)


client.run(os.environ.get("DISCORD_TOKEN"))
