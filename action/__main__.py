import argparse
import glob
import os
import requests
import shutil
import zipfile
from dotenv import load_dotenv
from pathlib import Path
from rdflib import Graph
from rocrate.rocrate import ROCrate
from sema.bench import Sembench

parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true')
args = parser.parse_args()

if args.dev:
    assert Path(".env").exists(), ".env file is missing"
    load_dotenv(override=True)


GITHUB_WORKSPACE = Path(os.getenv("GITHUB_WORKSPACE"))
SEMA_WORKSPACE = GITHUB_WORKSPACE / "sema-workspace"
ROCRATE_PROFILE_URI = os.getenv("ROCRATE_PROFILE_URI")
WATER_LOGSHEET_URL = os.getenv("WATER_LOGSHEET_URL")
SEDIMENT_LOGSHEET_URL = os.getenv("SEDIMENT_LOGSHEET_URL")
HARD_LOGSHEET_URL = os.getenv("HARD_LOGSHEET_URL")
RDF_AGGREGATOR_GLOB = os.getenv("RDF_AGGREGATOR_GLOB")


def clone_profile_crate_repo():
    profile_crate_metadata = requests.get(f"{ROCRATE_PROFILE_URI}/ro-crate-metadata.json").json()
    download_url = None
    for node in profile_crate_metadata.get("@graph", [{}]):
        if node.get("@id", "") == "./":
            download_url = node.get("downloadUrl")
    assert download_url
    zipball = requests.get(download_url)
    with open(SEMA_WORKSPACE / "zipball.zip", "wb") as f:
        f.write(zipball.content)
    with zipfile.ZipFile(SEMA_WORKSPACE / "zipball.zip", 'r') as f:
        f.extractall(SEMA_WORKSPACE / "zipball")
    for path in glob.glob(str(SEMA_WORKSPACE / "zipball" / "*" / "*")):
        shutil.move(path, SEMA_WORKSPACE)
    os.remove(SEMA_WORKSPACE / "zipball.zip")
    shutil.rmtree(SEMA_WORKSPACE / "zipball")


class Aggregator:
    def __init__(self):
        self.globs = {k.strip(): v.strip() for k, v in (i.strip().split(":") for i in RDF_AGGREGATOR_GLOB.split(","))}
        self.graph = Graph()

    def aggregate(self):
        for glb, fmt in self.globs.items():
            for p in GITHUB_WORKSPACE.rglob(glb):
                if p.is_file():
                    try:
                        self.graph.parse(p, format=fmt)
                    except Exception as e:
                        print(f"failed to parse {p}: {e}")

        self.graph.serialize(GITHUB_WORKSPACE / "all-triples.ttl", format="ttl")


if __name__ == "__main__":
    if not (GITHUB_WORKSPACE / "ro-crate-metadata.json").exists():
        crate = ROCrate()
        crate.write(GITHUB_WORKSPACE)

    if not SEMA_WORKSPACE.exists(): 
        SEMA_WORKSPACE.mkdir(parents=True, exist_ok=True)

    if not any(SEMA_WORKSPACE.iterdir()):
        clone_profile_crate_repo()
    
    for habitat in ("water", "sediment", "hard"): # TODO introduce "common" habitat
        if habitat == "common" or (os.getenv(f"{habitat.upper()}_LOGSHEET_URL")):
            sb = Sembench(
                locations={
                    "observatory-profile": str(SEMA_WORKSPACE),
                    "observatory-crate": str(GITHUB_WORKSPACE),
                },
                sembench_config_path = str(SEMA_WORKSPACE / f"sema_bench_{habitat}.yaml"),
                fail_fast=True,
            )

            sb.process()

    Aggregator().aggregate()
