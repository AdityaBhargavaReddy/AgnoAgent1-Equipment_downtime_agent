from agent import Mainagent
from inputs import (
    get_text_input,
    get_voice_input,
    get_image_input
)
from dotenv import load_dotenv
load_dotenv()

def main():
    print("""
Choose input type:
1. Text
2. Voice
3. Image
""")

    choice = input("Enter choice (1/2/3): ")

    if choice == "1":
        text = get_text_input()
    elif choice == "2":
        text = get_voice_input()
    elif choice == "3":
        text = get_image_input()
    else:
        print("Invalid choice")
        return

    print("\n--- Extracted Text ---")
    Mainagent.print_response(text, stream=True)

    # print("\n--- AGNO AGENT RESPONSE ---")
    # response = run_agent(text)
    # print(response)


if __name__ == "__main__":
    main()
