#!/usr/bin/env -S python3 -B

# NOTE: If you are using an alpine docker image
# such as pyaction-lite, the -S option above won't
# work. The above line works fine on other linux distributions
# such as debian, etc, so the above line will work fine
# if you use pyaction:4.0.0 or higher as your base docker image.
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