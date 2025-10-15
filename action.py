import glob
import os
import shutil
import zipfile
import requests
from pathlib import Path
from rocrate.rocrate import ROCrate, ContextEntity
import json
import yaml
from pathlib import Path
from sema.bench import Sembench

GITHUB_WORKSPACE = Path("/github/workspace")
SEMBENCH_WORKSPACE = GITHUB_WORKSPACE / "~sembench_data_cache"
PROFILE = os.getenv("PROFILE")

def instantiate_rocrate():
    crate = ROCrate()
    context_entity = crate.add(
        ContextEntity(
            crate,
            identifier=PROFILE,
            properties={
                "@type": "CreativeWork",
                "name": "<name>",
                "version": "<version>"
            },
        )
    )
    crate.root_dataset["conformsTo"] = context_entity
    crate.write(GITHUB_WORKSPACE)


def clone_profile_crate_repo():
    data_crate = ROCrate(GITHUB_WORKSPACE)
    profile_uri = data_crate.root_dataset["conformsTo"]["@id"]
    profile_crate = ROCrate()
    profile_crate_metadata = requests.get(f"{profile_uri}/ro-crate-metadata.json").json()
    for i in profile_crate_metadata.get("@graph", []):
        profile_crate.add_or_update_jsonld(i)
    zipball = requests.get(profile_crate.root_dataset["downloadUrl"])
    with open("zipball.zip", "wb") as f:
        f.write(zipball.content)
    with zipfile.ZipFile("zipball.zip", 'r') as f:
        f.extractall("zipball")
    for path in glob.glob("zipball/*/*"):
        shutil.move(path, SEMBENCH_WORKSPACE)
    os.remove(GITHUB_WORKSPACE / "zipball.zip")
    shutil.rmtree(GITHUB_WORKSPACE / "zipball")

def splice_sembench_config(ignore_task_prefix):
    """This function is a hack to circumvent the problem that a YAML file can't be parsed without resolving the !tags.
    """
    with open(SEMBENCH_WORKSPACE / "sembench.yaml", "r") as f:
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

    with open(SEMBENCH_WORKSPACE / "sembench.yaml", "w") as f:
        f.writelines(spliced_config)

if __name__ == "__main__":
    if not (GITHUB_WORKSPACE / "ro-crate-metadata.json").exists():
        instantiate_rocrate()

    if not SEMBENCH_WORKSPACE.exists(): 
        SEMBENCH_WORKSPACE.mkdir(parents=True, exist_ok=True)
        clone_profile_crate_repo()

    wp = yaml.load(open(GITHUB_WORKSPACE / "config/workflow_properties.yml"), Loader=yaml.BaseLoader)

    if wp["water"] == "nan":
        splice_sembench_config("water")
    if wp["sediment"] == "nan":
        splice_sembench_config("sediment")

    sb = Sembench(
        locations={
            "home": str(SEMBENCH_WORKSPACE),
            "input": str(GITHUB_WORKSPACE),
        },
        sembench_config_path = str(SEMBENCH_WORKSPACE / "sembench.yaml"),
        fail_fast=True,
    )

    sb.process()
