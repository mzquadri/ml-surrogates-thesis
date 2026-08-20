"""Validate canonical thesis, corrigendum, and aggregate evidence contracts."""

import hashlib
import json
import py_compile
import re
import subprocess
from pathlib import Path

from evidence_contract import (
    AUDIT_SOURCE_COMMIT,
    LOCAL_TEST_LOADER_BYTES,
    LOCAL_TEST_LOADER_PATH,
    LOCAL_TEST_LOADER_SHA256,
    SOURCE_ARTIFACTS,
    SUBMITTED_ARTIFACT_COMMIT,
    SUBMITTED_DOCUMENT_FILE_COUNT,
    SUBMITTED_DOCUMENT_GIT_TREE,
    SUBMITTED_PDF_BYTES,
    SUBMITTED_PDF_SHA256,
)

REPO = Path(__file__).resolve().parent.parent
SUBMITTED_PDF = REPO / "document/main.pdf"
ANALYSIS_ROOT = REPO / "analysis_outputs"

ANALYSIS_OUTPUT_SHA256 = {
    "THESIS_INTELLIGENCE_REPORT.md": "c59b7c7c7a9179fdcdcd5a2b880dcf2062b9f9c83a7b08a13c6e1b44af5398e8",
    "artifact_manifest.csv": "68368fc523766ac78b3599deaf0f233712a234eb4dae8fa741941ec3ec50cd59",
    "figures/conditional_coverage_by_uncertainty.png": "6aac4e8944f368efeeb501777e74101354307cb2d5c2eed1511506c0335b2bd4",
    "figures/conditional_coverage_by_uncertainty.svg": "498ccf6b124bed4bbc6f1026c42604ab10f520af07c5b34d3992b5d206b0bba1",
    "figures/model_r2_comparison.png": "b410b1aaf582ca58460de4b3ad574e9ab325fab97fcb9bb4f5e539793665f653",
    "figures/model_r2_comparison.svg": "32543f566f9e8900ca82f302f323adac883eaba900c38825045d8858f7d8d1b5",
    "figures/selective_risk_comparison.png": "aa3ba233904c075eadf0c3c68bdf98ed1167eb70e3f80cd92e4f02cd5efbbbc8",
    "figures/selective_risk_comparison.svg": "ba575f469dbddae1ad2e1ee88c0fac4ef842ba38356b05119e163225f95d9822",
    "figures/temperature_reliability_graph20_80.png": "824120fac2f8d21108de18fcff2ab8197d6ea7ec065acbdca636277969aadeb2",
    "figures/temperature_reliability_graph20_80.svg": "7c46c9e3525cfe0c18efc73939e42ea84c02bbea6d85eaefd8a8447990192ad3",
    "figures/uncertainty_error_relationship.png": "8f56efee2ac3a13d86c920b8012a92232b86284d0e424c76ff9ae007740eb7e1",
    "figures/uncertainty_error_relationship.svg": "754a4dfceeecc651c9ea79a5950e4dca91ac6b2c3acf1d05e7af3432fb97bfd7",
    "model_comparison.csv": "af923cf16e9e5c071f9b357d7a946c8ad232f74f3646f19fba8da762cd6cac00",
    "thesis_intelligence.json": "5b5a8b0df4d66a45f8f9958ffb9a8e094932c4e6c34e1ecf5e9f0bb86b8c68ec",
}

LOCAL_PATH_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]|\\\\[^\\\s]+\\[^\\\s]+|"
    r"(?<![:\w])/(?:Users|home|mnt|tmp|var|opt|root|workspace|srv|build|project|app)/",
    re.IGNORECASE,
)
ROW_LEVEL_KEYS = {
    "prediction",
    "predictions",
    "target",
    "targets",
    "uncertainty",
    "uncertainties",
    "observations",
    "points",
    "records",
    "rows",
    "samples",
    "y_pred",
    "y_true",
}

REQUIRED_PATHS = (
    "README.md",
    "CITATION.cff",
    "document/main.pdf",
    "document/main.tex",
    "code/environment-minimal.yml",
    "docs/CORRIGENDUM.md",
    "docs/ARTIFACT_PROVENANCE.md",
    "analysis_outputs/thesis_intelligence.json",
    "analysis_outputs/THESIS_INTELLIGENCE_REPORT.md",
    "analysis_outputs/artifact_manifest.csv",
    "analysis_outputs/model_comparison.csv",
    "dashboard-requirements.txt",
    "requirements-dev.txt",
    "scripts/analysis/generate_thesis_intelligence.py",
    "thesis_dashboard/app.py",
    "thesis_dashboard/analytics.py",
    ".streamlit/config.toml",
)

PYTHON_PATHS = (
    "scripts/analysis/generate_thesis_intelligence.py",
    "thesis_dashboard/app.py",
    "thesis_dashboard/analytics.py",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def validate_submitted_pdf() -> None:
    if SUBMITTED_PDF.stat().st_size != SUBMITTED_PDF_BYTES:
        raise SystemExit("Submitted PDF size changed")
    if sha256(SUBMITTED_PDF) != SUBMITTED_PDF_SHA256:
        raise SystemExit("Submitted PDF hash changed")


def validate_submitted_document_tree() -> None:
    document_root = REPO / "document"
    files = sorted(path for path in document_root.rglob("*") if path.is_file())
    if len(files) != SUBMITTED_DOCUMENT_FILE_COUNT:
        raise SystemExit("Submitted document tree file count changed")

    current_tree = subprocess.run(
        ["git", "rev-parse", "HEAD:document"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    baseline_tree = subprocess.run(
        ["git", "rev-parse", f"{SUBMITTED_ARTIFACT_COMMIT}:document"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if current_tree != SUBMITTED_DOCUMENT_GIT_TREE or baseline_tree != current_tree:
        raise SystemExit("Submitted document Git tree changed")

    baseline = subprocess.run(
        ["git", "diff", "--quiet", SUBMITTED_ARTIFACT_COMMIT, "--", "document"],
        cwd=REPO,
        check=False,
    )
    if baseline.returncode != 0:
        raise SystemExit(
            "Submitted document tree differs from baseline commit "
            f"{SUBMITTED_ARTIFACT_COMMIT} or the baseline is unavailable"
        )


def validate_json_export(value: object, location: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in ROW_LEVEL_KEYS and isinstance(child, list):
                raise SystemExit(f"Aggregate JSON contains a row-level array at {location}.{key}")
            validate_json_export(child, f"{location}.{key}")
    elif isinstance(value, list):
        if len(value) > 100:
            raise SystemExit(f"Aggregate JSON contains an oversized array at {location}")
        for index, child in enumerate(value):
            validate_json_export(child, f"{location}[{index}]")
    elif isinstance(value, str):
        stripped = value.strip()
        if LOCAL_PATH_PATTERN.search(value) or stripped.startswith(("/", "\\\\")):
            raise SystemExit(f"Aggregate JSON contains an absolute local path at {location}")


def validate_analysis_outputs() -> None:
    actual = {
        path.relative_to(ANALYSIS_ROOT).as_posix()
        for path in ANALYSIS_ROOT.rglob("*")
        if path.is_file()
    }
    expected = set(ANALYSIS_OUTPUT_SHA256)
    if actual != expected:
        raise SystemExit(
            "Aggregate output inventory changed: "
            f"missing={sorted(expected - actual)}, unexpected={sorted(actual - expected)}"
        )

    for relative_path, expected_digest in ANALYSIS_OUTPUT_SHA256.items():
        path = ANALYSIS_ROOT / relative_path
        if sha256(path) != expected_digest:
            raise SystemExit(f"Aggregate output hash changed: {relative_path}")
        if path.suffix.lower() in {".csv", ".json", ".md", ".svg"}:
            text = path.read_text(encoding="utf-8")
            if LOCAL_PATH_PATTERN.search(text) or "MohdZaminQuadri" in text:
                raise SystemExit(f"Aggregate output contains a local path: {relative_path}")


def validate_bundle() -> None:
    bundle_path = REPO / "analysis_outputs/thesis_intelligence.json"
    with bundle_path.open(encoding="utf-8") as handle:
        bundle = json.load(handle)

    if bundle.get("schema_version") != "1.0.0":
        raise SystemExit("Unsupported thesis intelligence schema")
    provenance = bundle.get("source_provenance", {})
    if provenance.get("audit_source_commit") != AUDIT_SOURCE_COMMIT:
        raise SystemExit("Aggregate bundle source commit is not locked")

    expected_privacy = {
        "classification": "safe aggregate export",
        "contains_absolute_paths": False,
        "contains_pickle_payloads": False,
        "contains_row_level_records": False,
        "source_data_policy": (
            "local processing only; confidential data junction excluded"
        ),
    }
    if bundle.get("privacy") != expected_privacy:
        raise SystemExit("Aggregate bundle privacy contract is invalid")
    validate_json_export(bundle)

    target = bundle["analyses"]["t8_mc"]["quality"]["targets"]
    if target["count"] != 3_163_500 or target["zero_count"] != 872_540:
        raise SystemExit("Corrected T8 target audit values do not match")

    manifest = bundle["artifact_manifest"]
    source_rows = {row["name"]: row for row in manifest if row["name"] in SOURCE_ARTIFACTS}
    if set(source_rows) != set(SOURCE_ARTIFACTS):
        raise SystemExit("Aggregate manifest source inventory is incomplete")
    for name, (expected_path, expected_bytes, expected_hash) in SOURCE_ARTIFACTS.items():
        row = source_rows[name]
        if row != {
            "name": name,
            "path": expected_path,
            "exists": True,
            "bytes": expected_bytes,
            "sha256": expected_hash,
            "trust_boundary": "tracked audited-source artifact",
        }:
            raise SystemExit(f"Aggregate manifest source contract changed: {name}")

    local_loader_rows = [row for row in manifest if row["name"] == "t8_local_test_loader"]
    expected_local_loader = {
        "name": "t8_local_test_loader",
        "path": LOCAL_TEST_LOADER_PATH,
        "exists": True,
        "bytes": LOCAL_TEST_LOADER_BYTES,
        "sha256": LOCAL_TEST_LOADER_SHA256,
        "trust_boundary": "hash-locked local audited-source pickle artifact; never export",
    }
    if local_loader_rows != [expected_local_loader]:
        raise SystemExit("Aggregate manifest local loader contract changed")

    for artifact in manifest:
        artifact_path = Path(artifact["path"])
        if artifact_path.is_absolute():
            raise SystemExit(f"Manifest path must be relative: {artifact_path}")
        artifact_hash = artifact.get("sha256")
        if artifact_hash is not None:
            if len(artifact_hash) != 64:
                raise SystemExit(f"Invalid manifest hash length: {artifact_path}")
            int(artifact_hash, 16)


def validate_public_docs() -> None:
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    code_readme = (REPO / "code/README.md").read_text(encoding="utf-8")
    public_prose = f"{readme}\n{code_readme}".lower()
    forbidden = ("zero bugs", "0 bugs", "predicted speed change", "predicts speed change")
    if any(value in public_prose for value in forbidden):
        raise SystemExit("Public documentation contains a superseded claim")
    if "872,540 exact zeros out of 3,163,500" not in readme:
        raise SystemExit("README does not state the corrected target-zero result")
    if "https://github.com/mzquadri/ml-surrogates-thesis" not in (
        REPO / "CITATION.cff"
    ).read_text(encoding="utf-8"):
        raise SystemExit("Citation metadata does not use the canonical repository")


def main() -> None:
    missing = [path for path in REQUIRED_PATHS if not (REPO / path).is_file()]
    if missing:
        raise SystemExit("Missing required artifacts:\n- " + "\n- ".join(missing))

    validate_submitted_pdf()
    validate_submitted_document_tree()
    validate_analysis_outputs()
    validate_bundle()
    validate_public_docs()
    for path in PYTHON_PATHS:
        py_compile.compile(str(REPO / path), doraise=True)

    print(
        f"Repository check passed: {len(REQUIRED_PATHS)} required artifacts; "
        "submitted document tree and aggregate evidence contracts verified."
    )


if __name__ == "__main__":
    main()
