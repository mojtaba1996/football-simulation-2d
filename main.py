import argparse
from config import Config
from runner import Runner


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Football Simulation 2D")
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file')

    args = parser.parse_args()
    config = Config(path=args.config)
    r = Runner(config)
    r.run()
    r.end()
