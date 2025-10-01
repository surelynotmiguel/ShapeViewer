# This is the main file that runs the program. It imports the Program class from src/Program.py and runs the run method.

from src.Program import Program

if __name__ == "__main__":
    print("Running HyperPolygon...\n")

    print("Instructions:")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("1. Press 'W', 'A', 'S', 'D', 'Space' and 'Left Shift' to move the camera.")
    print("2. Press 'R' to change the shape.")
    print("3. Press 'Right Click' to switch between 3D and 4D.")
    print("4. Press 'I' to show/hide program information.")
    print("5. Press 'F' to toggle fullscreen.")
    print("6. Press 'ESC' to unlock the mouse.")
    print("7. Move the mouse to look around.")
    print("8. Press 'X' to exit the program.")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

    Program.run()

