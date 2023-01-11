import os

def main():
    # Get the GitHub access token from the environment
    git_access_token = os.getenv("GITHUB_TOKEN")
    git_repo = os.getenv("GITHUB_REPOSITORY")

    # Print the token
    print("GitHub access token: " + git_access_token)
    print("GitHub repository: " + git_repo)
    print("End of script.")

if __name__ == "__main__":
    main()