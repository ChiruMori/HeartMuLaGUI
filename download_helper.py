"""Helper script for downloading HeartMuLa models"""
import sys
from huggingface_hub import snapshot_download

def download_model(repo_id, local_dir):
    """Download a model from Hugging Face"""
    try:
        print(f"Downloading {repo_id} to {local_dir}...")
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        print(f"✓ Successfully downloaded {repo_id}")
        return 0
    except Exception as e:
        print(f"✗ Error downloading {repo_id}: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_helper.py <repo_id> <local_dir>")
        sys.exit(1)
    
    repo_id = sys.argv[1]
    local_dir = sys.argv[2]
    sys.exit(download_model(repo_id, local_dir))
