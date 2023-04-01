from config import Config
from runner import Runner


if __name__ == "__main__":
    r = Runner(Config())
    r.run()
    r.end()
