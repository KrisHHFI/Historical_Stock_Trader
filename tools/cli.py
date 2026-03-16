import sys
from cmd_create_new import cmd_create_new
from cmd_create_refine import cmd_create_refine

COMMANDS = {
    "help":          "Show this help page.",
    "create new": "Generate a new trading algorithm and set it as the active strategy.",
    "refine":      "Run the ML parameter optimizer to tune the active algorithm.",
}


def print_help() -> None:
    print("Usage: trader <command>")
    print()
    print("Available commands:")
    for cmd, description in COMMANDS.items():
        print(f"  {cmd:<20} {description}")
    print()


if __name__ == "__main__":
    args = sys.argv[1:]
    command = " ".join(args).strip().lower()

    if command == "create new":
        cmd_create_new()
    elif command == "refine":
        cmd_create_refine()
    else:
        print_help()

