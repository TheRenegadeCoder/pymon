# CS Query Bot

The CS Query Bot was developed to help students find answers to course questions. It is not currently hosted for public use, but you can self-host it using the code found in this repo. Currently, I am running the bot on a home desktop.

## How to Run the Bot

If you'd like to use this bot in your own server, start by cloning/forking this repo. After that, you'll want to create a .env file in the root directory of the repo with the following contents:

```env
DISCORD_TOKEN=[insert token here]
```

After that, you'll want to install all requirements. Luckily, I've included a requirements.txt file. You can use the following code to install all requirements:

```shell
pip install -r requirements.txt
```

From there, you can run the bot like any other Python script:

```shell
python3 code_bot.py
```

## How to Use the Bot

The CS Query Bot currently has two main services. First, you can directly @ the bot to get it to respond with the top three matching questions to your query. The response will include an ID which you can lookup with the `/get` command. Alternatively, you can use the list in the next section directly. Note that the questions don't have any organization, so asking the bot to give you some matches is sometimes a better start.

## Question IDs

Currently, the bot can answer the following questions. The numbers map directly to the lookup IDs, so if you want an answer to any of these questions, just ask the bot with `/get`.

1. What is a magic number?
2. What is a primitive type?
3. How can I create a constant?
4. What is testing?
5. What is debugging?
6. What is correctness?
7. What is JUnit?
8. What is unit testing?
9. What is an expression tree?
10. What is confidence building?
11. What is the declared type of a variable?
12. What is method overriding?
13. What is method overloading?
14. What is the implements relationship?
15. What is the extends relationship?

---

This README was automatically generated using SnakeMD.