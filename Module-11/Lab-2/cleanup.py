"""
Cleanup Script for Lab-2: Delete ALL Agent Engine Resources
Removes reasoning engines, staging buckets, and container images
"""

import subprocess
import vertexai
from vertexai import agent_engines

PROJECT_ID = ""
LOCATION = ""

vertexai.init(project=PROJECT_ID, location=LOCATION)

print(f"Project:  {PROJECT_ID}")
print(f"Region:   {LOCATION}")
print()

# ============================================
# STEP 1: Delete all Reasoning Engine deployments
# ============================================
print("=" * 50)
print("STEP 1: Reasoning Engine Deployments")
print("=" * 50)

engines = agent_engines.list()

if not engines:
    print("  No deployments found.")
else:
    for e in engines:
        print(f"  Deleting {e.display_name} ({e.resource_name})...")
        agent_engines.delete(e.resource_name, force=True)
        print(f"  Deleted.")

print()

# ============================================
# STEP 2: Delete staging buckets created by
#          Agent Engine
# ============================================
print("=" * 50)
print("STEP 2: Cloud Storage Staging Buckets")
print("=" * 50)

# Agent Engine creates buckets matching these patterns
bucket_patterns = [
    f"gs://{PROJECT_ID}-reasoning-engine",
    f"gs://{PROJECT_ID}_cloudbuild",
]

# Also find any buckets with "reasoning" or "agent" in the name
result = subprocess.run(
    ["gsutil", "ls", f"-p", PROJECT_ID],
    capture_output=True, text=True
)

if result.returncode == 0:
    all_buckets = result.stdout.strip().split("\n")
    agent_buckets = [
        b for b in all_buckets
        if any(keyword in b.lower() for keyword in ["reasoning", "agent-engine", "cloudbuild"])
    ]

    if not agent_buckets:
        print("  No staging buckets found.")
    else:
        for bucket in agent_buckets:
            print(f"  Deleting {bucket} ...")
            subprocess.run(
                ["gsutil", "-m", "rm", "-r", bucket],
                capture_output=True, text=True
            )
            print(f"  Deleted.")
else:
    print("  Could not list buckets. Skipping.")

print()

# ============================================
# STEP 3: Delete Artifact Registry images
#          created during deployment
# ============================================
print("=" * 50)
print("STEP 3: Artifact Registry Images")
print("=" * 50)

# List all repositories in the region
result = subprocess.run(
    [
        "gcloud", "artifacts", "repositories", "list",
        f"--project={PROJECT_ID}",
        f"--location={LOCATION}",
        "--format=value(name)"
    ],
    capture_output=True, text=True
)

if result.returncode == 0 and result.stdout.strip():
    repos = result.stdout.strip().split("\n")
    for repo in repos:
        repo_name = repo.strip()
        if not repo_name:
            continue
        repo_path = f"{LOCATION}-docker.pkg.dev/{PROJECT_ID}/{repo_name}"
        print(f"  Checking repository: {repo_name}")

        # List images in this repo
        img_result = subprocess.run(
            [
                "gcloud", "artifacts", "docker", "images", "list",
                repo_path,
                f"--project={PROJECT_ID}",
                "--format=value(IMAGE)"
            ],
            capture_output=True, text=True
        )

        if img_result.returncode == 0 and img_result.stdout.strip():
            images = img_result.stdout.strip().split("\n")
            for image in images:
                image = image.strip()
                if image:
                    print(f"    Deleting image: {image}")
                    subprocess.run(
                        [
                            "gcloud", "artifacts", "docker", "images", "delete",
                            image, "--quiet", "--delete-tags"
                        ],
                        capture_output=True, text=True
                    )

            # Delete the repository itself
            print(f"  Deleting repository: {repo_name}")
            subprocess.run(
                [
                    "gcloud", "artifacts", "repositories", "delete",
                    repo_name,
                    f"--location={LOCATION}",
                    f"--project={PROJECT_ID}",
                    "--quiet"
                ],
                capture_output=True, text=True
            )
            print(f"  Deleted.")
        else:
            print(f"    No images found.")
else:
    print("  No Artifact Registry repositories found.")

print()

# ============================================
# STEP 4: Verify everything is cleaned up
# ============================================
print("=" * 50)
print("VERIFICATION")
print("=" * 50)

remaining = agent_engines.list()
if not remaining:
    print("  Reasoning Engines: None remaining")
else:
    print("  Reasoning Engines still active:")
    for e in remaining:
        print(f"    {e.display_name} - {e.resource_name}")

print()
print("Cleanup complete!")