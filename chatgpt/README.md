# ChatGPT Unofficial API

- It makes use of Selenium. 
- The webdriver can't run in `headless` mode.

## How to use

Install the dependencies
```
python -r install requirements.txt
```

Start the cli and follow the instructions. You can now communicate with ChatGPT.
```
python chatgpt_cli.py
```

## Demo
- Once you give the email and password for your openai account, you can interact with ChatGPT via the CLI.
- Type 'quit' if you want to quit the CLI.
- In __yellow__ it's what you send to ChatGPT, and in __green__ it's what it answers.
- There's a delay in the output of ChatGPT's answer in the terminal, because the CLI uses a dynamic delay to figure out
when the answer is complete. This delay is __tunable__!
![](chatgpt-demo.gif)
