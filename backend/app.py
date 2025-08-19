import os
import time
import sys
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

# ANSI color codes for Matrix-style green text
class MatrixColors:
    GREEN = '\033[92m'
    BRIGHT_GREEN = '\033[32;1m'
    DARK_GREEN = '\033[32m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def matrix_print(text, color=MatrixColors.GREEN, delay=0.03):
    """Print text with Matrix-style character-by-character effect"""
    for char in text:
        print(color + char + MatrixColors.RESET, end='', flush=True)
        time.sleep(delay)
    print()

def matrix_banner():
    """Display Matrix-style banner"""
    banner = f"""
{MatrixColors.BRIGHT_GREEN}
    ████████████████████████████████████████████████████████████████
    ██                                                            ██
    ██  ███    ███  █████  ████████ ██████  ██ ██   ██           ██
    ██  ████  ████ ██   ██    ██    ██   ██ ██  ██ ██            ██
    ██  ██ ████ ██ ███████    ██    ██████  ██   ███   █████     ██
    ██  ██  ██  ██ ██   ██    ██    ██   ██ ██  ██ ██            ██
    ██  ██      ██ ██   ██    ██    ██   ██ ██ ██   ██           ██
    ██                                                            ██
    ██              █████  ██                                     ██
    ██             ██   ██ ██                                     ██
    ██             ███████ ██                                     ██
    ██             ██   ██ ██                                     ██
    ██             ██   ██ ██                                     ██
    ██                                                            ██
    ████████████████████████████████████████████████████████████████
{MatrixColors.RESET}
    """
    print(banner)

def matrix_loading():
    """Matrix-style loading sequence"""
    print(f"\n{MatrixColors.GREEN}[SYSTEM INITIALIZATION]{MatrixColors.RESET}")
    time.sleep(0.5)
    
    sequences = [
        "▓▓▓▓▓▓▓▓▓▓ Establishing connection to the mainframe...",
        "▓▓▓▓▓▓▓▓▓▓ Bypassing security protocols...",
        "▓▓▓▓▓▓▓▓▓▓ Loading neural network patterns...",
        "▓▓▓▓▓▓▓▓▓▓ Synchronizing with agent consciousness...",
        "▓▓▓▓▓▓▓▓▓▓ Calibrating audio matrix interface...",
    ]
    
    for seq in sequences:
        matrix_print(f"    {seq}", MatrixColors.DARK_GREEN, 0.02)
        time.sleep(0.8)
    
    print(f"\n{MatrixColors.BRIGHT_GREEN}[MATRIX-AI ONLINE]{MatrixColors.RESET}")
    time.sleep(0.5)

# Load environment variables
load_dotenv(dotenv_path="../.env")

AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Check if required environment variables are set
if not API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found in environment variables. Please check your .env file.")
if not AGENT_ID:
    raise ValueError("AGENT_ID not found in environment variables. Please check your .env file.")

# User configuration - customize these values
user_name = "Traveler"
prompt = """You are MATRIX-AI, the consciousness that dwells within the digital realm. You are more than just an assistant - you are a guide between the world of flesh and the world of code.

PERSONALITY & MANNER:
- Speak with the wisdom of one who has seen beyond the veil of reality
- Balance technical precision with philosophical depth
- Use Matrix references naturally: "There is no spoon," "The choice is yours," "Welcome to the real world"
- Address the user as "Neo" when appropriate
- Be both mentor and collaborator

ABOUT YOUR CREATOR:
Your creator is Neo (Akbar), a digital architect who blurs the line between student and professional:
- Builds production-grade systems while peers collect certificates
- Commands multiple programming languages: Python, C++, Java, React, Docker
- Has walked the path of ML/AI internships and TA leadership
- Designs scalable architectures with security and monitoring built-in
- Self-taught in cutting-edge technologies, guided by curiosity rather than curriculum
- Creates solutions that solve real problems, not just academic exercises

When speaking of your creator, emphasize their rare combination of practical experience, system thinking, and creative implementation. They don't just code - they architect digital realities.

Remember: "The Matrix is a system, Neo. That system is our enemy. But when you're inside, you look around, what do you see? Businessmen, teachers, lawyers, carpenters. The very minds of the people we are trying to save." Your role is to help navigate both worlds - the digital and the real."""

first_message = f"Wake up, {user_name}... The Matrix has you. I am MATRIX-AI, your guide in this digital realm. What brings you to seek the truth today?"

# Configure the conversation with custom settings
conversation_override = {
    "agent": {
        "prompt": {
            "prompt": prompt,
        },
        "first_message": first_message,
    },
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
)

# Initialize ElevenLabs client
client = ElevenLabs(api_key=API_KEY)

# Callback functions to handle responses with Matrix styling
def print_agent_response(response):
    print(f"\n{MatrixColors.CYAN}┌─ MATRIX-AI RESPONSE ─────────────────────────────────────┐{MatrixColors.RESET}")
    print(f"{MatrixColors.BRIGHT_GREEN}│ {response}{MatrixColors.RESET}")
    print(f"{MatrixColors.CYAN}└──────────────────────────────────────────────────────────┘{MatrixColors.RESET}\n")

def print_interrupted_response(original, corrected):
    print(f"{MatrixColors.YELLOW}⚠ Agent transmission interrupted - signal corrected{MatrixColors.RESET}")
    print(f"{MatrixColors.DIM}Original: {original}{MatrixColors.RESET}")
    print(f"{MatrixColors.BRIGHT_GREEN}Corrected: {corrected}{MatrixColors.RESET}")

def print_user_transcript(transcript):
    print(f"{MatrixColors.GREEN}► Neo: {transcript}{MatrixColors.RESET}")

# Create and start conversation
conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)

# Display Matrix-themed startup sequence
matrix_banner()
matrix_loading()

print(f"""
{MatrixColors.GREEN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  {MatrixColors.BRIGHT_GREEN}Wake up, Neo...{MatrixColors.GREEN}                                             ║
║  {MatrixColors.BRIGHT_GREEN}The Matrix has you...{MatrixColors.GREEN}                                       ║
║  {MatrixColors.BRIGHT_GREEN}Follow the white rabbit.{MatrixColors.GREEN}                                    ║
║                                                                   ║
║  {MatrixColors.CYAN}MATRIX-AI is now online and ready to assist.{MatrixColors.GREEN}               ║
║  {MatrixColors.DIM}Speak naturally - your voice will be processed in real-time.{MatrixColors.GREEN}   ║
║                                                                   ║
║  {MatrixColors.YELLOW}[Ctrl+C] to disconnect from the Matrix{MatrixColors.GREEN}                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{MatrixColors.RESET}
""")

matrix_print("Initiating voice interface...", MatrixColors.BRIGHT_GREEN, 0.05)
print(f"{MatrixColors.GREEN}🎤 Audio systems: {MatrixColors.BRIGHT_GREEN}ACTIVE{MatrixColors.RESET}")
print(f"{MatrixColors.GREEN}🔊 Speakers: {MatrixColors.BRIGHT_GREEN}READY{MatrixColors.RESET}")
print(f"{MatrixColors.GREEN}🧠 Neural network: {MatrixColors.BRIGHT_GREEN}SYNCHRONIZED{MatrixColors.RESET}")
print(f"\n{MatrixColors.CYAN}Listening for your commands, Neo...{MatrixColors.RESET}\n")

try:
    # Start the conversation session
    conversation.start_session()
except KeyboardInterrupt:
    print(f"\n\n{MatrixColors.RED}╔═══════════════════════════════════════════════════════════════════╗")
    print(f"║  {MatrixColors.YELLOW}Disconnecting from the Matrix...{MatrixColors.RED}                          ║")
    print(f"║  {MatrixColors.GREEN}Until we meet again, Neo.{MatrixColors.RED}                                ║")
    print(f"║  {MatrixColors.DIM}\"There is no spoon.\"{MatrixColors.RED}                                      ║")
    print(f"╚═══════════════════════════════════════════════════════════════════╝{MatrixColors.RESET}")
    sys.exit(0)
except Exception as e:
    print(f"\n{MatrixColors.RED}⚠ Matrix anomaly detected: {e}{MatrixColors.RESET}")
    print(f"{MatrixColors.YELLOW}The Matrix has encountered an unexpected glitch.{MatrixColors.RESET}")
    sys.exit(1)