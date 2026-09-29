from gabo_core import think


print("================================")
print("          GABO TEXT MODE        ")
print("================================")
print("Type 'exit' to shut down GABO.\n")


while True:
    user_input = input("You: ")

    if user_input.lower().strip() == "exit":
        print("GABO: Shutting down.")
        break

    if not user_input.strip():
        continue

    response = think(user_input)

    print(f"GABO: {response}")
    print()