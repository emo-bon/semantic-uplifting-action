import os
from github import Github

def main():
    # Get the GitHub access token from the environment
    git_access_token = os.getenv("GITHUB_TOKEN")
    git_repo = os.getenv("GITHUB_REPOSITORY")

    # Use the access token to create a GitHub client
    g = Github(git_access_token)

    # Get the repository
    repo = g.get_repo(git_repo)

    print("Getting the latest release...")
    print("")
    print("Latest release: {}".format(repo.get_latest_release().title))
    print("")
    print("End of script.")

if __name__ == "__main__":
    main()