import os
import sys

from gabo_core import think
from provider_gemini import chat as gemini_chat
from provider_groq import chat as groq_chat

# ============================================================
# GABO CONSOLE
# ============================================================

VOICE_RUNNING = False


# ============================================================
# DISPLAY
# ============================================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_banner():
    print("""
========================================
              GABO
        CONTROL CONSOLE
========================================

Type 'help' for commands.
Type 'chat' to enter chat mode.
""")


# ============================================================
# STATUS
# ============================================================

def show_status():
    print("""
GABO STATUS
-----------
Core:       ONLINE
Voice:      {}
STT:        READY
TTS:        READY
""".format("ON" if VOICE_RUNNING else "OFF"))


# ============================================================
# HELP
# ============================================================

def show_help():
    print("""
GABO CONTROL COMMANDS
----------------------

chat
    Enter conversational chat mode.

status
    Show GABO system status.

voice on
    Start the voice system.

voice off
    Stop the voice system.

clear
    Clear the console.

help
    Show this help message.

exit
    Shut down the console.


CHAT MODE
---------

Inside chat mode:

    Normal text
        → sent to GABO

    /status
        → show system status

    /help
        → show chat commands

    /exit
        → leave chat mode
""")


# ============================================================
# VOICE
# ============================================================

def start_voice():
    global VOICE_RUNNING

    if VOICE_RUNNING:
        print("Voice system is already running.")
        return

    try:
        import wake_listen

        VOICE_RUNNING = True

        print("Starting voice system...")

        wake_listen.start()

    except AttributeError:
        print(
            "wake_listen.py does not have a "
            "'start()' function yet."
        )

        VOICE_RUNNING = False

    except Exception as e:
        print(f"Failed to start voice system: {e}")
        VOICE_RUNNING = False


def stop_voice():
    global VOICE_RUNNING

    if not VOICE_RUNNING:
        print("Voice system is already off.")
        return

    try:
        import wake_listen

        wake_listen.stop()

        VOICE_RUNNING = False

        print("Voice system stopped.")

    except AttributeError:
        print(
            "wake_listen.py does not have a "
            "'stop()' function yet."
        )

    except Exception as e:
        print(f"Failed to stop voice system: {e}")


# ============================================================
# CHAT MODE
# ============================================================

def chat_mode():

    print("""
========================================
             GABO CHAT
========================================

Type /help for chat commands.
Type /exit to return to the console.
""")

    while True:

        try:
            user_input = input("You: ").strip()

        except KeyboardInterrupt:
            print("\nLeaving chat mode.")
            return

        if not user_input:
            continue

        # -------------------------
        # Chat commands
        # -------------------------

        if user_input == "/exit":
            print("Leaving chat mode.\n")
            return

        if user_input == "/help":
            print("""
CHAT COMMANDS
-------------

/status
    Show GABO status.

/help
    Show these commands.

/exit
    Return to control console.
""")
            continue

        if user_input == "/status":
            show_status()
            continue

        # -------------------------
        # Normal conversation
        # -------------------------

        try:
            response = think(user_input)

            print()
            print(f"GABO: {response}")
            print()

        except Exception as e:
            print()
            print(f"GABO ERROR: {e}")
            print()

# ============================================================
# GEMINI PROVIDED GCHAT
# ============================================================


def gemini_chat_mode():

    print("""
========================================
           GABO GEMINI CHAT
========================================

Direct connection to Google Gemini.

Type /help for commands.
Type /reset to start a new conversation.
Type /exit to return to the GABO console.
""")

    while True:

        try:
            user_input = input("You: ").strip()

        except KeyboardInterrupt:
            print("\nLeaving Gemini chat.")
            return

        if not user_input:
            continue

        # --------------------------------
        # Gemini chat commands
        # --------------------------------

        if user_input == "/exit":
            print("Leaving Gemini chat.\n")
            return

        if user_input == "/reset":
            try:
                from provider_gemini import reset_chat

                reset_chat()

                print("Gemini conversation reset.\n")

            except Exception as e:
                print(f"Reset failed: {e}\n")

            continue

        if user_input == "/help":
            print("""
GEMINI CHAT COMMANDS
--------------------

/reset
    Start a new Gemini conversation.

/help
    Show these commands.

/exit
    Return to the GABO console.
""")
            continue

        # --------------------------------
        # Send to Gemini
        # --------------------------------

        try:

            print("\nGemini: ", end="", flush=True)

            response = gemini_chat(
                user_input
            )

            print(response)
            print()

        except Exception as e:

            print()
            print(f"GEMINI ERROR: {e}")
            print()



# ============================================================
# GROQ PROVIDED GCHAT
# ============================================================


def groq_chat_mode():
    print("""
========================================
            GABO GROQ CHAT
========================================

Direct connection to Groq.

Type /help for commands.
Type /reset to start a new conversation.
Type /exit to return to the GABO console.
""")

    while True:
        try:
            user_input = input("You: ").strip()

        except KeyboardInterrupt:
            print("\nLeaving Groq chat.")
            return

        if not user_input:
            continue

        if user_input == "/exit":
            print("Leaving Groq chat.\n")
            return

        if user_input == "/reset":
            try:
                from provider_groq import reset_chat

                reset_chat()

                print("Groq conversation reset.\n")

            except Exception as e:
                print(f"Reset failed: {e}\n")

            continue

        if user_input == "/help":
            print("""
GROQ CHAT COMMANDS
------------------
/reset
    Start a new Groq conversation.

/help
    Show these commands.

/exit
    Return to the GABO console.
""")
            continue

        try:
            print("\nGroq: ", end="", flush=True)

            response = groq_chat(user_input)

            print(response)
            print()

        except Exception as e:
            print()
            print(f"GROQ ERROR: {e}")
            print()


# ============================================================
# CONTROL COMMAND PROCESSOR
# ============================================================

def process_command(command):

    global VOICE_RUNNING

    command = command.strip()

    if not command:
        return True

    # -------------------------
    # Chat
    # -------------------------

    if command == "chat":
        chat_mode()
        return True

    # -------------------------
    # G Chat
    # -------------------------

    if command == "gchat":
        gemini_chat_mode()
        return True

    # -------------------------
    # GR Chat
    # -------------------------

    if command == "grchat":
        groq_chat_mode()
        return True

    # -------------------------
    # Help
    # -------------------------

    if command == "help":
        show_help()
        return True

    # -------------------------
    # Status
    # -------------------------

    if command == "status":
        show_status()
        return True

    # -------------------------
    # Clear
    # -------------------------

    if command == "clear":
        clear_screen()
        show_banner()
        return True

    # -------------------------
    # Voice
    # -------------------------

    if command == "voice on":
        start_voice()
        return True

    if command == "voice off":
        stop_voice()
        return True

    # -------------------------
    # Exit
    # -------------------------

    if command == "exit":
        print("\nGABO shutting down.")
        return False

    # -------------------------
    # Unknown command
    # -------------------------

    print(
        f"Unknown command: {command}\n"
        "Type 'help' for available commands."
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    show_banner()

    running = True

    while running:

        try:
            command = input("gabo> ")
            running = process_command(command)

        except KeyboardInterrupt:
            print("\n\nGABO shutting down.")
            break

        except EOFError:
            print("\nGABO shutting down.")
            break


if __name__ == "__main__":
    main()