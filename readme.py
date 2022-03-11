import snakemd
import json

queries = json.load(open("queries.json"))

doc = snakemd.new_doc("README")

doc.add_header("CS Query Bot")

doc.add_paragraph(
    """
    The CS Query Bot was developed to help students find answers to course questions.
    It is not currently hosted for public use, but you can self-host it using the
    code found in this repo. Currently, I am running the bot on a home desktop.
    """
)

doc.add_header("How to Run the Bot", 2)

doc.add_paragraph(
    """
    If you'd like to use this bot in your own server, start by cloning/forking this repo.
    After that, you'll want to create a .env file in the root directory of the repo
    with the following contents:
    """
)

doc.add_code(
    "DISCORD_TOKEN=[insert token here]",
    "env"
)

doc.add_paragraph(
    """
    After that, you'll want to install all requirements. Luckily, I've included a
    requirements.txt file. You can use the following code to install all
    requirements:
    """
)

doc.add_code(
    "pip install -r requirements.txt",
    "shell"
)

doc.add_paragraph(
    """
    From there, you can run the bot like any other Python script:
    """
)

doc.add_code(
    "python3 code_bot.py",
    "shell"
)

doc.add_header("Bot Features", 2)

doc.add_paragraph(
    """
    Currently, the bot can answer the following questions:
    """
)

questions = []
for query in queries:
    if query.get("query"):
        questions.append(query.get("query"))

doc.add_ordered_list(questions)

doc.output_page()
