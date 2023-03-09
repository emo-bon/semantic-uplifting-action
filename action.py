import json
from pathlib import Path
from pysembench.core import Sembench

if __name__ == "__main__":
    GITHUB_WORKSPACE = Path("/github/workspace")
    SEMBENCH_KWARGS = Path("~sembench_kwargs.json")

    with open(GITHUB_WORKSPACE / SEMBENCH_KWARGS) as f:
        kwargs = json.load(f)

    sb = Sembench(
        input_data_location = kwargs["INPUT_DATA_LOCATION"],
        sembench_data_location = kwargs["SEMBENCH_DATA_LOCATION"],
        sembench_config_path = kwargs["SEMBENCH_CONFIG_PATH"],
    )

    sb.process(force=True)
