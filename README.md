# **GABO**
**GABO** is a private, locally-oriented AI assistant built from scratch with the goal of becoming a fast, voice-controlled personal assistant that will have resemblance with the actual biological lifeform and actual thought process of a human or other low level biological brain.

It is designed to listen for a wake word, understand spoken commands, generate a response, and speak back. The long-term goal is to give GABO access to useful tools, sensors, automation, and eventually physical hardware.

# **Status:** Experimental / In active development

# **Features**

A/ Voice input using speech recognition
B/ Local LLM support through Ollama
C/ Cloud LLM support through external providers
D/ Text-to-speech using Piper
E/ Wake-word detection using OpenWakeWord
F/ Windows-based console interface
G/ Designed for future tools, automation, sensors, and hardware

## Current Architecture

## Current Components

A Speech Recognition

GABO currently uses **faster-whisper** for speech-to-text.

The project is designed to work with lightweight Whisper models so that speech recognition can run on relatively modest hardware.

B Wake Word Detection

Wake-word detection is handled with **OpenWakeWord**.

The system can detect supported wake phrases and activate GABO when the assistant is addressed.

C Language Model

GABO supports local LLM inference through **Ollama**.

The development setup currently uses a lightweight model
