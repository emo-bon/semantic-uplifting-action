import argparse
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from rocrate.rocrate import ROCrate
from sema.bench import Sembench
from sema.commons.aggregator import Aggregator
from sema.ro.getter import ROGetter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("semantic-uplifting-action")

parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true')
args = parser.parse_args()

if args.dev:
    assert Path(".env").exists(), ".env file is missing"
    load_dotenv(override=True)


GITHUB_WORKSPACE = Path(os.getenv("GITHUB_WORKSPACE", "."))
SEMA_WORKSPACE = GITHUB_WORKSPACE / "sema-workspace"
ROCRATE_PROFILE_URI = os.getenv("ROCRATE_PROFILE_URI")
WATER_LOGSHEET_URL = os.getenv("WATER_LOGSHEET_URL")
SEDIMENT_LOGSHEET_URL = os.getenv("SEDIMENT_LOGSHEET_URL")
HARD_LOGSHEET_URL = os.getenv("HARD_LOGSHEET_URL")
RDF_AGGREGATOR_GLOB = os.getenv("RDF_AGGREGATOR_GLOB")
RDF_AGGREGATOR_OUTPUT = os.getenv("RDF_AGGREGATOR_OUTPUT")


def parse_aggregator_globs(glob_str: str | None) -> list[str | dict[str, str]]:
    """Convert comma-separated `pattern:format` or `pattern` strings to list for Aggregator."""
    if not glob_str or not glob_str.strip():
        return ["**/*.ttl"]

    globs: list[str | dict[str, str]] = []
    for part in glob_str.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            g, fmt = part.split(":", 1)
            globs.append({g.strip(): fmt.strip()})
        else:
            globs.append(part)

    return globs if globs else ["**/*.ttl"]


if __name__ == "__main__":
    if not (GITHUB_WORKSPACE / "ro-crate-metadata.json").exists():
        logger.info("Initializing ROCrate metadata in %s...", GITHUB_WORKSPACE)
        crate = ROCrate()
        crate.write(GITHUB_WORKSPACE)

    if not SEMA_WORKSPACE.exists():
        SEMA_WORKSPACE.mkdir(parents=True, exist_ok=True)

    if not any(SEMA_WORKSPACE.iterdir()):
        if ROCRATE_PROFILE_URI:
            logger.info("Fetching profile RO-Crate from %s into %s...", ROCRATE_PROFILE_URI, SEMA_WORKSPACE)
            ROGetter(uri=ROCRATE_PROFILE_URI, output_path=SEMA_WORKSPACE).process()
        else:
            logger.warning("ROCRATE_PROFILE_URI not set; skipping ROGetter.")

    for habitat in ("water", "sediment", "hard"):  # TODO introduce "common" habitat
        if habitat == "common" or (os.getenv(f"{habitat.upper()}_LOGSHEET_URL")):
            config_path = SEMA_WORKSPACE / f"sema_bench_{habitat}.yaml"
            logger.info("Running Sembench for %s (%s)...", habitat, config_path)
            sb = Sembench(
                locations={
                    "observatory-profile": str(SEMA_WORKSPACE),
                    "observatory-crate": str(GITHUB_WORKSPACE),
                },
                sembench_config_path=str(config_path),
                fail_fast=True,
            )

            sb.process()

    globs = parse_aggregator_globs(RDF_AGGREGATOR_GLOB)
    output_path = GITHUB_WORKSPACE / (RDF_AGGREGATOR_OUTPUT or "all-triples.ttl")
    logger.info("Aggregating RDF triples matching %s into %s...", globs, output_path)
    Aggregator(
        input_path=GITHUB_WORKSPACE,
        globs=globs,
        output_path=output_path,
        output_format="text/turtle",
    ).process()
    logger.info("Aggregation completed successfully.")
