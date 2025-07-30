from llm import call_deepseek

def main():
    user_input = "Tell me a joke about hotel rooms."
    response = call_deepseek(user_input)
    print("🤖 DeepSeek Response:\n", response)

if __name__ == "__main__":
    main()