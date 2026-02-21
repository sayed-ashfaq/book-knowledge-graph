# Interview Questions

### Questions before you build anything

1. You're about to start a real Python project that has maybe 15-20 different libraries — things like PDF readers, LLM clients, graph libraries, visualization tools.
If you just did pip install everything directly on your machine — what problem do you think could happen? --- Take a guess. There's no wrong answer here. Think about what happens if you have two different projects on the same machine that need different versions of the same library.--- What do you think? 

2. If you were organizing this project into folders, what folders would you create and why?
Don't worry about being perfect. Just think like someone who wants to find any file in this project 6 months later without confusion.

### Module 0 — Exit Quiz
You must answer these before we move to Module 1. Take your time, think it through.

Q1. What is the purpose of a virtual environment and what specific problem does it solve?

Q2. You're working on this project 3 months from now on a brand new laptop. You have your code but nothing else. What single file tells you exactly which libraries to install and at what versions — and what command would you run to restore everything instantly using UV?

Q3. Your friend clones your GitHub repo but your project crashes immediately because the LLM can't authenticate. You checked — all your code is correct. What's the most likely reason and what did you probably forget to tell your friend?


### Module 1
1. Why do you think we use Path from pathlib instead of just writing file paths as plain strings like "data/mybook.pdf"?

so that it can work in any environment or laptop or cloud and we can add extra features to it such as assign a root path and then add them to the folder path. hardcoding string is slow and manual which might cause issues.
* Exactly right. The technical term for what you described is cross-platform compatibility. On Windows paths look like data\mybook.pdf and on Mac/Linux they look like data/mybook.pdf. Path handles that difference automatically so your code works everywhere without you thinking about it.
* And your second point about building paths dynamically — spot on. Path("data") / "mybook.pdf" is cleaner and safer than string concatenation.

Q1. Our clean_text() function removes standalone numbers to eliminate page numbers. Can you think of a case where this regex might accidentally remove something important?

Q1 is exactly right — this is a real limitation we're accepting for now. In a production system you'd write smarter regex or use a proper NLP tokenizer to distinguish "page 47" from "revenue grew 47%". Good catch.

Q2. 3 pages were skipped because they had less than 50 characters after cleaning. What kind of pages were those likely to be in a real book?

Q2 — chapter titles and acknowledgements yes, also likely blank pages and full-image pages like diagrams or covers with no extractable text.