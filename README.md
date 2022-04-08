# Pymon

Pymon was developed to help students find answers to course questions. It is not currently hosted for public use, but you can self-host it using the code found in this repo. Currently, I am running the bot on a home desktop.

## How to Run the Bot

If you'd like to use this bot in your own server, start by cloning/forking this repo. After that, you'll want to create a .env file in the root directory of the repo with the following contents:

```env
DISCORD_TOKEN=[insert token here]
```

If you'd like to include your own knowledge base, you can do so by also creating a KNOWLEDGE_PATH environment variable in your .env file. This should point to a local file or a remote URL. Otherwise, the bot will use the queries.json file, which is designed specifically for a course I am teaching.

```env
KNOWLEDGE_PATH=[insert path here]
```

After that, you'll want to install all requirements. Luckily, I've included a requirements.txt file. You can use the following code to install all requirements:

```shell
pip install -r requirements.txt
```

From there, you can run the bot like any other Python script:

```shell
python3 pymon.py
```

## How to Use the Bot

Pymon currently has two main services. First, you can directly @ the bot to get it to respond with the top three matching questions to your query. The response will include an ID which you can lookup with the `/get` command. Alternatively, you can use the list in the next section directly. Note that the questions don't have any organization, so asking the bot to give you some matches is sometimes a better start.

## Question IDs

Currently, the bot can answer the following questions. The numbers map directly to the lookup IDs, so if you want an answer to any of these questions, just ask the bot with `/get`.

1. "What is a magic number?" by Jeremy Grifski
2. "What is a primitive type?" by Jeremy Grifski
3. "How can I create a constant?" by Jeremy Grifski
4. "What is testing?" by Jeremy Grifski
5. "What is debugging?" by Jeremy Grifski, Xining Feng
6. "What is correctness?" by Jeremy Grifski
7. "What is JUnit?" by Jeremy Grifski
8. "What is unit testing?" by Jeremy Grifski
9. "What is an expression tree?" by Jeremy Grifski
10. "What is confidence building?" by Jeremy Grifski
11. "What is the declared type of a variable?" by Jeremy Grifski
12. "What is method overriding?" by Jeremy Grifski, Le Chang
13. "What is method overloading?" by Jeremy Grifski
14. "What is the implements relationship?" by Jeremy Grifski, Yibo Gan
15. "What is the extends relationship?" by Jeremy Grifski
16. "What is a mathematical string?" by Jeremy Grifski
17. "What is mathematical string notation for concatenation?" by Jeremy Grifski
18. "What is a parameter mode?" by Jeremy Grifski
19. "What is restores mode?" by Jeremy Grifski
20. "What is a queue?" by Jeremy Grifski
21. "What is a set?" by Jeremy Grifski
22. "What is a stack?" by Jeremy Grifski
23. "What does FIFO mean?" by Jeremy Grifski
24. "What does LIFO mean?" by Jeremy Grifski
25. "What is the object type of a variable?" by Kelvin Nguyen
26. "What is an immutable type?" by Jacob Skarsten, Ziqing Zhao
27. "What is replaces mode?" by Shaan Patel
28. "What is updates mode?" by Colin Russel
29. "Are arrays immutable or mutable?" by Jessica Molitor
30. "What is inheritance?" by Xingzhi Dai
31. "What is clears mode?" by Ethan Chilton
32. "What is the default parameter mode when none is specified in the method contract?" by Dan Brace
33. "What is the drawback and/or problem with aliasing?" by Michael Grady
34. "What is a superclass?" by Ben Janita
35. "Will you be my girlfriend?" by Ben Janita
36. "What is an interface?" by Chenmeinian Guo
37. "Is testing an expensive waste of time?" by Jason Su
38. "What is the purpose of the queue data structure?" by Ying Liang
39. "What is Recursion?" by Gani Sagiev
40. "What is the difference between unit and integration testing?" by Jacob Kolaczkowski
41. "What is the difference between testing and debugging?" by John DiFilippo
42. "What is object-oriented-programming?" by Felix Ji

---

This README was automatically generated using SnakeMD.