import json
from pathlib import Path
from pysembench.core import Sembench, locations_from_environ

if __name__ == "__main__":
    GITHUB_WORKSPACE = Path("/github/workspace")
    SEMBENCH_KWARGS = Path("~sembench_kwargs.json")

    with open(GITHUB_WORKSPACE / SEMBENCH_KWARGS) as f:
        kwargs = json.load(f)

    sb = Sembench(
        # TODO consider switching to the more flexible pattern scheme
        # for env variables --> SEMBENCH_HOME_PATH, SEMBENCH_INPUT_PATH 
        # then following line can become locations=locations_from_environ()
        locations=dict(
            home=kwargs["SEMBENCH_DATA_LOCATION"],
            input=kwargs["INPUT_DATA_LOCATION"],
        ),
        sembench_config_path = kwargs["SEMBENCH_CONFIG_PATH"],
    )

    sb.process()
