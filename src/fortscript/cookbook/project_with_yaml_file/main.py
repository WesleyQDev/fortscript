import os

from fortscript import FortScript

# Path to our English configuration file
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config.yaml")

# Initialize FortScript using the external YAML file
# This is ideal for users who want to change settings without touching Python code
app = FortScript(config_path=config_path)


def main():
    print("--- [bold magenta]FortScript: Content Creator Case[/bold magenta] ---")
    print(f"Loading external configuration from: {config_path}")
    print("Scenario: Managing streaming overlays that pause during resource-intensive gameplay.")
    app.run()


if __name__ == "__main__":
    main()
