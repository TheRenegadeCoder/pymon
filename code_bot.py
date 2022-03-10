import json
import os
import string

import discord
from discord import Message

from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv


# Helper methods
def generate_keyword_mapping(queries: list) -> dict:
    """
    Creates a mapping of keywords to queries.

    :param queries: a list of queries with responses
    :return: a dictionary of keywords to query indices
    """
    keyword_to_queries = dict()
    for i, question in enumerate(queries):
        if question.get('query'):
            keywords = generate_keywords(question.get("query"))
            keywords.extend(generate_keywords(question.get("response")))
            for keyword in keywords:
                keyword_to_queries.setdefault(keyword, []).append(i)
    return keyword_to_queries


def generate_keywords(query: string) -> list:
    """
    Create a list of keywords from a query.

    :param query: a search query
    :return: the list of keywords from that query
    """
    stop_words = ["", "is", "a", "the", "can", "i", "to", "in", "by", "from", "be", "of"]
    keywords = query \
        .translate(str.maketrans('', '', string.punctuation)) \
        .lower() \
        .split(" ")
    keywords = [word for word in keywords if word not in stop_words]
    return keywords


def search(keyword_to_queries: dict, keywords: list) -> list:
    """
    Looks up the list of queries that satisfy a keyword.

    :param keyword_to_queries: a mapping of keywords to query indices
    :param keywords: a list of keywords to lookup
    :return: a list of query indices
    """
    query_count = dict()
    for keyword in keywords:
        query_indices = keyword_to_queries.get(keyword, [])
        for i in query_indices:
            query_count.setdefault(i, 0)
            query_count[i] += 1
    best_matches = list(dict(sorted(query_count.items(), key=lambda item: item[1])).keys())
    return best_matches


def create_md_link(url: string, text: string) -> string:
    """
    Creates a markdown link.

    :param url: the url to link to
    :param text: the text to display
    :return: the markdown link
    """
    if url:
        return f"[{text}]({url})"
    return text


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
queries = json.load(open("queries.json"))
keyword_mapping = generate_keyword_mapping(queries)


# Discord bot code
async def _react_on_mention(message: Message):
    if client.user.mentioned_in(message):
        indices = search(keyword_mapping, generate_keywords(message.content))
        reply = list()
        reply.extend([
            f"{create_md_link(queries[i].get('resource'), queries[i].get('query'))}" 
            for i in indices[:3]
        ])
        embed = discord.Embed(
            title="Do any of these questions match your query?",
            description="Use the ID with the /lookup command to get an answer:",
            color=discord.Color.blue()
        )
        for idx, row in enumerate(reply):
            embed.add_field(
                name=f"#{idx + 1}: ID-{indices[idx]}", 
                value=row, 
                inline=True
            )
        embed.set_footer(
            text="Learn more about how this bot works @ https://github.com/TheRenegadeCoder/cs-query-bot.",
            icon_url="https://therenegadecoder.com/wp-content/uploads/2017/05/the-renegade-coder-icon-cropped.png"
        )
        await message.reply(embed=embed)


@client.event
async def on_message(message: Message):
    """
    The action to be called when a message is sent.

    :param message: the message to scrutinize
    :return: None
    """
    if message.author != client.user:
        await _react_on_mention(message)


@client.event
async def on_ready():
    channel = client.get_channel(309845675946934274)
    await channel.send("Ask me anytime.")


@slash.slash(
    name="lookup",
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
async def _lookup(ctx, index: int):
    """
    Looks up the answer to a query by its ID.

    :param ctx: the context to send messages to
    :return: None
    """
    await ctx.send(queries[index]["response"])


client.run(os.environ.get("DISCORD_TOKEN"))
