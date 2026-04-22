"""
Entry point for the Garden App
"""

from advisor import GardenCLI


def main():
    cli = GardenCLI()
    cli.run()


if __name__ == "__main__":
    main()