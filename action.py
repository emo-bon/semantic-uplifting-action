import json
from pathlib import Path
from pysembench import Sembench

if __name__ == "__main__":
    GITHUB_WORKSPACE = Path("/github/workspace")
    SEMBENCH_KWARGS = Path("~sembench_kwargs.json")

    with open(GITHUB_WORKSPACE / SEMBENCH_KWARGS) as f:
        kwargs = json.load(f)

    sb = Sembench(
        locations={
            "home": kwargs["SEMBENCH_DATA_LOCATION"],
            "input": kwargs["INPUT_DATA_LOCATION"],
        },
        sembench_config_path = kwargs["SEMBENCH_CONFIG_PATH"],
    )

    sb.process()
