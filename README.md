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

**A Speech Recognition**

GABO currently uses **faster-whisper** for speech-to-text.

The project is designed to work with lightweight Whisper models so that speech recognition can run on relatively modest hardware.

**B Wake Word Detection**

Wake-word detection is handled with **OpenWakeWord**.

The system can detect supported wake phrases and activate GABO when the assistant is addressed.

**C Language Model**

GABO supports local LLM inference through Ollama.

The development setup currently uses a lightweight model suitable for running on consumer hardware.

Cloud-based models can also be integrated when additional capability is useful.

**D Text-to-Speech**

GABO uses Piper for local text-to-speech.

The current voice is based on:

en_US-lessac-medium
Hardware

The project is being developed with relatively modest hardware in mind.

A major goal is to keep the assistant lightweight enough to run locally rather than requiring a powerful GPU or permanent cloud connection.

# **Example Commands**

The eventual goal is for commands such as:

"GABO, perform a security check."

"GABO, set the bulb to 30 lumens."

"GABO, probe for temperature."

to trigger actual tools or hardware actions.

At the moment, many of these capabilities are still experimental.

## **Project Structure**
GABO/
├── main.py
├── audio-stt.py
├── test_stt.py
├── test-tts.py
├── GABO.spec
├── .gitignore
└── ...

The project structure is still evolving as GABO's architecture develops.

## **Installation**
**Requirements**
Windows
Python 3.12+
Git
A working microphone
Speakers or headphones
Ollama for local LLM support
Python dependencies listed by the project
Clone the repository
git clone https://github.com/shutdown-f/GABO.git
cd GABO
Create a virtual environment
python -m venv .venv

**Activate it:**

.venv\Scripts\Activate.ps1

Then install the required Python packages.

Dependency installation and configuration are still being standardized, so expect some manual setup during the current development stage.

## **Development**

GABO is currently a personal experimental project.

The architecture, models, voice pipeline, command system, and hardware interfaces are expected to change considerably as development continues.

The current priority is getting the core assistant loop reliable:

Wake → Listen → Understand → Think → Respond → Speak

After that, the plan is to expand GABO's ability to interact with the world through tools and hardware.

## **Roadmap**

Voice

Wake-word detection

Speech-to-text

Text-to-speech

Improve conversational latency

More natural voice

Better interruption handling

Intelligence

Local LLM experimentation

Cloud LLM experimentation

Persistent memory

Tool calling

Better command routing

Context-aware responses

Tools & Automation

System controls

Smart-home control

Sensor integration

Security checks

Custom command system

Hardware

Camera / computer vision

Environmental sensors

Robotics integration

Physical GABO interface

## **Philosophy**

GABO is intended to be a useful assistant, not a digital companion.

The goal is practical interaction: give it a command, let it figure out what needs to happen, and have it do the job.

Ideally, the assistant should feel less like a chatbot and more like a capable piece of software that happens to have a voice.

GABO is a work in progress.

Built experimentally, one subsystem at a time.
