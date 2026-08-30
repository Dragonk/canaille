import re
from pathlib import Path


WORKFLOW_PATH = Path(".github/workflows/publish-ghcr.yml")
REPAIR_WORKFLOW_PATH = Path(".github/workflows/repair-ghcr-latest.yml")


def test_publish_workflow_preserves_releases_and_serializes_latest_updates():
    workflow = WORKFLOW_PATH.read_text()

    assert re.search(
        r"concurrency:\n"
        r"  group: publish-kmms-canaille-\$\{\{ github\.repository \}\}-"
        r"\$\{\{ github\.ref_name \}\}\n"
        r"  cancel-in-progress: false",
        workflow,
    )
    assert re.search(
        r"  publish:\n"
        r"    name: Publish immutable GHCR image\n"
        r"    runs-on: ubuntu-24.04\n"
        r"    outputs:\n"
        r"      image: \$\{\{ steps\.release\.outputs\.image \}\}",
        workflow,
    )
    assert re.search(
        r"  update-latest:\n"
        r"(?:(?!^  [a-z]).)*?"
        r"    needs: publish\n"
        r"(?:(?!^  [a-z]).)*?"
        r"    concurrency:\n"
        r"      group: publish-kmms-canaille-latest-\$\{\{ github\.repository \}\}\n"
        r"      cancel-in-progress: false",
        workflow,
        flags=re.DOTALL | re.MULTILINE,
    )
    assert "IMAGE: ${{ needs.publish.outputs.image }}" in workflow
    assert "git fetch --force --tags origin" in workflow
    assert "docker buildx imagetools create" in workflow


def test_latest_repair_workflow_repoints_an_existing_release_image():
    workflow = REPAIR_WORKFLOW_PATH.read_text()

    assert "workflow_dispatch:" in workflow
    assert "release_tag:" in workflow
    assert "ref: ${{ inputs.release_tag }}" in workflow
    assert "docker manifest inspect \"$IMAGE\"" in workflow
    assert 'release_sha="$(git rev-list -n 1 "$RELEASE_TAG")"' in workflow
    assert "git merge-base --is-ancestor \"$release_sha\" origin/main" in workflow
    assert "docker buildx imagetools create" in workflow
