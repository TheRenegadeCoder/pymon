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
5. "What is debugging?" by Xining Feng, Jeremy Grifski
6. "What is correctness?" by Jeremy Grifski
7. "What is JUnit?" by Jeremy Grifski
8. "What is unit testing?" by Jeremy Grifski
9. "What is an expression tree?" by Jeremy Grifski
10. "What is confidence building?" by Jeremy Grifski
11. "What is the declared type of a variable?" by Jeremy Grifski
12. "What is the static type of a variable?" by Jeremy Grifski
13. "What is method overriding?" by Jeremy Grifski, Alexia Scarvelli, Zihe Fang, Tae Yeon Kim, Le Chang
14. "What is method overloading?" by Jeremy Grifski
15. "What is the implements relationship?" by Yibo Gan, Jeremy Grifski
16. "What is the extends relationship?" by Yi-You (Joseph) Chiu, Jeremy Grifski
17. "What is a mathematical string?" by Jeremy Grifski
18. "What is mathematical string notation for concatenation?" by Jeremy Grifski
19. "What is a parameter mode?" by Jeremy Grifski
20. "What is restores mode?" by Jeremy Grifski
21. "What is a queue?" by Jeremy Grifski
22. "What is a set?" by Jeremy Grifski
23. "What is a stack?" by Jeremy Grifski
24. "What does FIFO mean?" by Jeremy Grifski
25. "What does LIFO mean?" by Jeremy Grifski
26. "What is the object type of a variable?" by Kelvin Nguyen
27. "What is an immutable type?" by Jacob Skarsten, Ziqing Zhao
28. "What is replaces mode?" by Shaan Patel
29. "What is updates mode?" by Colin Russel
30. "Are arrays immutable or mutable?" by Jessica Molitor
31. "What is inheritance?" by Xingzhi Dai
32. "What is clears mode?" by Ethan Chilton
33. "What is the default parameter mode when none is specified in the method contract?" by Dan Brace
34. "What is the drawback and/or problem with aliasing?" by Michael Grady
35. "What is a superclass?" by Ben Janita
36. "Will you be my girlfriend?" by Ben Janita
37. "What is an interface?" by Chenmeinian Guo, Tim Keck
38. "Is testing an expensive waste of time?" by Jason Su
39. "What is the purpose of the queue data structure?" by Ying Liang
40. "What is Recursion?" by Gani Sagiev, Tim Keck
41. "What is the difference between unit and integration testing?" by Jacob Kolaczkowski
42. "What is the difference between testing and debugging?" by Ahmed Mohamed, John DiFilippo
43. "What is object-oriented programming (OOP)?" by Felix Ji
44. "What type of method is a JUnit test case?" by Matthew Alfieri
45. "What is aliasing?" by Yuhang Huang
46. "Is XMLTree a mutable or immutable type?" by Drishti Mittal
47. "Is a string a mutable or immutable type?" by Grant McGeehen
48. "What is the difference between copyFrom and transferFrom?" by Jashira Herrera Brito
49. "What is the purpose of testing and what can it not prove?" by Nick Cheong
50. "What does the method `.divide()` for NaturalNumber return?" by Kate Goertz
51. "What is the benefit of interval halving?" by Ashir Faruq
52. "What is mathematical induction?" by Om Amin
53. "What is the Set data type?" by Luke Thompson
54. "What is the correct expression to see if an integer is odd in Java?" by Yi-You (Joseph) Chiu, Kurt Wanner
55. "What is XML?" by Tim Keck
56. "What is mutability?" by Tim Keck
57. "What is a comparator?" by Tim Keck
58. "What is a method contract?" by Tim Keck
59. "How do I trace a variable through a recursive method?" by Tim Keck
60. "What is the difference between a remainder and a modulus?" by Darrel Jobin
61. "What are the four parameter modes?" by Darrel Jobin
62. "What are NaturalNumberKernel's three methods?" by Alyssa Wiegman, Catherine Wu
63. "What is a procedure?" by Amit Bharathan
64. "What is the implementer's role?" by Daniel Han
65. "What is the Standard interface?" by Andrew Nida
66. "What are some ways to iterate over non-ordered data structures like sets?" by Josh Grismer
67. "Is restores mode a default parameter mode?" by Allen Zhang
68. "What is the difference between parameter and argument?" by Lucas Curran
69. "What is the difference between an expression and a statement?" by Peter Sung
70. "What is API?" by Yingqi Gao
71. "What is a boolean?" by Oliver Gwynn
72. "What is the difference between a public and private method?" by Sammy Schwartz
73. "What is design by contract for?" by Darin Renusch
74. "What is RSS?" by Andy Vong
75. "What is the difference between inheritance and polymorphism?" by Jatin Mamtani
76. "What is a precondition?" by Akshaya Iyer
77. "What is short-circuit evaluation?" by Junbo Chen
78. "What makes two if statements independent?" by Jarrett Reeves, Jeremy Grifski
79. "What is polymorphism?" by Angstrom Sarkar
80. "Why can't interfaces have constructors?" by Yingqi Gao
81. "What is abstraction?" by Yingqi Gao
82. "What is the difference between interface and abstract class?" by Yingqi Gao
83. "When should I use newInstance?" by Shivam Engineer
84. "What is an observer pattern?" by Jayshuk Pandrangi
85. "What is a loop invariant?" by Jayshuk Pandrangi
86. "What is MVC?" by Yuheng Long (Simon)

---

This README was automatically generated using SnakeMD.