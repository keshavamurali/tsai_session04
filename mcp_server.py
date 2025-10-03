# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
#from pywinauto.application import Application
#import win32gui
#import win32con
import time
import time
import subprocess
from Quartz.CoreGraphics import (
    CGEventCreateMouseEvent, CGEventPost,
    kCGEventLeftMouseDown, kCGEventLeftMouseUp,
    kCGEventMouseMoved, kCGEventLeftMouseDragged,
    kCGMouseButtonLeft
)
import pyautogui
#from win32api import GetSystemMetrics

# instantiate an MCP server client
mcp = FastMCP("Calculator")

kCGHIDEventTap = 0  
paintbrush_opened = False
# -----------------------------
# Quartz helpers
# -----------------------------
def mouse_event(type, x, y):
    event = CGEventCreateMouseEvent(None, type, (x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, event)

def mouse_move(x, y): mouse_event(kCGEventMouseMoved, x, y)
def mouse_down(x, y): mouse_event(kCGEventLeftMouseDown, x, y)
def mouse_up(x, y): mouse_event(kCGEventLeftMouseUp, x, y)
def mouse_drag(x, y): mouse_event(kCGEventLeftMouseDragged, x, y)
def mouse_click(x, y):
    mouse_move(x, y)
    time.sleep(0.05)
    mouse_down(x, y)
    time.sleep(0.05)
    mouse_up(x, y)

def activate_paintbrush():
    """Bring Paintbrush to front (must already be open)"""
    subprocess.run(["osascript", "-e", 'tell application "Paintbrush" to activate'])
    time.sleep(0.5)

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

@mcp.tool()
def draw_rectangle(x1: int, y1: int, x2: int, y2: int) -> dict:
    """Draw a rectangle in Paintbrush from (x1,y1) to (x2,y2)"""
    try:
        activate_paintbrush()
        RECT_TOOL = (80, 253)  # update with actual toolbar coordinates
        mouse_click(*RECT_TOOL)
        time.sleep(0.5)

        mouse_move(x1, y1)
        mouse_down(x1, y1)
        time.sleep(0.1)
        mouse_drag(x2, y2)  # drag directly to bottom-right corner
        time.sleep(0.1)
        mouse_up(x2, y2)
        return {
        "content": [
            TextContent(
                type="text",
                text=f"Rectangle drawn from ({x1},{y1}) to ({x2},{y2})"
            )
        ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }

@mcp.tool()
def add_text_in_rectangle(x1: int, y1: int, text: str) -> dict:
    """Add text in Paintbrush in a rectangle with top left corner at (x1, y1)"""
    try:
        activate_paintbrush()
        TEXT_TOOL = (107, 285)      # Text tool icon coords
        PLACE_BUTTON = (835, 553)   # Place button coords (update to your screen)
        
        # Activate Paintbrush
        subprocess.run(["osascript", "-e", 'tell application "Paintbrush" to activate'])
        time.sleep(0.5)

        # Step 1: select text tool
        mouse_click(*TEXT_TOOL)
        time.sleep(0.3)

        # Step 2: click anywhere to create text box
        mouse_click(x1+10, y1+10)  # offset slightly to avoid collision with rectangle
        time.sleep(0.3)

        # Step 3: type text
        pyautogui.typewrite(text, interval=0.05)
        time.sleep(0.2)

        # Step 4: click the "Place" button
        mouse_click(*PLACE_BUTTON)
        time.sleep(0.2)

        # Step 5: click inside rectangle to insert text
        mouse_click(x1+40, y1+40)
        time.sleep(0.2)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text:'{text}' added successfully"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }



@mcp.tool()
async def open_paintbrush() -> dict:
    """Open Paintbrush app"""
    try:
        global paintbrush_opened
        subprocess.Popen(["open", "-a", "Paintbrush"])
        time.sleep(2)
        pyautogui.press("enter")  # dismiss popup
        time.sleep(1)
        paintbrush_opened = True
        activate_paintbrush()
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Paintbrush opened successfully and maximized"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Paintbrush: {str(e)}"
                )
            ]
        }
# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        print("RUNNING IN DEV MODE")
        mcp.run()  # Run without transport for dev server
    else:
        print("RUNNING IN PRODUCTION MODE")
        mcp.run(transport="stdio")  # Run with stdio for direct execution
