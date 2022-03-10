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
        keywords = generate_keywords(question.get("query"))
        for keyword in keywords:
            keyword_to_queries.setdefault(keyword, []).append(i)
    return keyword_to_queries


def generate_keywords(query: string) -> list:
    """
    Create a list of keywords from a query.

    :param query: a search query
    :return: the list of keywords from that query
    """
    stop_words = ["is", "a", "the"]
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
        top_queries = "\n".join([f"{queries[i].get('query')} (i = {i})" for i in indices[:5]])
        await message.reply(f"**Here are the top queries:**\n{top_queries}")


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
