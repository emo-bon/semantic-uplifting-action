import json
import yaml
from pathlib import Path
from sema.bench import Sembench

GITHUB_WORKSPACE = Path("/github/workspace")
SEMBENCH_KWARGS = Path("~sembench_kwargs.json")

with open(GITHUB_WORKSPACE / SEMBENCH_KWARGS) as f:
    kwargs = json.load(f)

INPUT_DATA_LOCATION = kwargs["INPUT_DATA_LOCATION"]
SEMBENCH_DATA_LOCATION = kwargs["SEMBENCH_DATA_LOCATION"]
SEMBENCH_CONFIG_PATH = kwargs["SEMBENCH_CONFIG_PATH"]

def splice_sembench_config(ignore_task_prefix):
    """This function is a hack to circumvent the problem that a YAML file can't be parsed without resolving the !tags.
    """
    with open(SEMBENCH_CONFIG_PATH, "r") as f:
        config = f.readlines()

    spliced_config = []
    skipping = False
    for line in config:
        if line.startswith(ignore_task_prefix):
            skipping = True
        elif line.startswith(" ") and skipping:
            pass
        elif line.startswith(" ") and not skipping:
            spliced_config.append(line)
        else:
            skipping = False
            spliced_config.append(line)

    with open(SEMBENCH_CONFIG_PATH, "w") as f:
        f.writelines(spliced_config)

wp = yaml.load(open(GITHUB_WORKSPACE / "config/workflow_properties.yml"), Loader=yaml.BaseLoader)

if wp["water"] == "nan":
    splice_sembench_config("water")
if wp["sediment"] == "nan":
    splice_sembench_config("sediment")

sb = Sembench(
    locations={
        "home": SEMBENCH_DATA_LOCATION,
        "input": INPUT_DATA_LOCATION,
    },
    sembench_config_path = SEMBENCH_CONFIG_PATH,
    fail_fast=True,
)

sb.process()
