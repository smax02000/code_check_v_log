import os
import requests

def fetch_pr_metadata():
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")
    print(f"token: {token}")
    print(f"repo: {repo}")
    print(f"pr-number: {pr_number}")
    
    if not all([token, repo, pr_number]):
        print("❌ Missing required environment variables.")
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    pr_url = f"https://github.apps.gevernova.net/api/v3/repos/{repo}/pulls/{pr_number}"
    response = requests.get(pr_url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch PR details: {response.status_code}")
        return None

    data = response.json()
    return {
        "PR Number": pr_number,
        "Title": data.get("title"),
        "Author": data.get("user", {}).get("login"),
        "Created At": data.get("created_at"),
        "Merged At": data.get("merged_at"),
        "URL": data.get("html_url")
    }

def show_metadata(pr_info):
    if pr_info:
        print(f"\n--- 📝 Pull Request #{pr_info['PR Number']} ---")
        for key, value in pr_info.items():
            print(f"{key}: {value}")
        print("✅ PR metadata displayed above.")

if __name__ == "__main__":
    pr_info = fetch_pr_metadata()
    show_metadata(pr_info)
