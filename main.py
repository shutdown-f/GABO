#################          Project   G. A. B. O.         ###################
def main():
    print("GABO v0.1")
    print("System online.")
    print("Type 'exit' to shut down.\n")

    while True:
        command = input("You: ")

        if command.lower() == "exit":
            print("Gabo: Shutting down.")
            break

        print(f"Gabo: I received: {command}")


if __name__ == "__main__":
    main()