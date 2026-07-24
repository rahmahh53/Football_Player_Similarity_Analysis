from pathlib import Path
import yaml


def load_config(config_path="config.yaml"):
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)  # loads the yaml file and converts it into a dictionary

    return config


if __name__ == "__main__":
    config = load_config()

    print("Project name:", config["project"]["name"])
    print("Project version:", config["project"]["version"])
    print("Raw data directory:", config["paths"]["raw_data_dir"])
    print("Processed data directory:", config["paths"]["processed_data_dir"])
    print("Database name:", config["database"]["database_name"])
