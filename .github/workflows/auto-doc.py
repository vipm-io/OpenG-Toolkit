import os
import json
from pathlib import Path
from typing import Self
from dataclasses import dataclass

# get this scripts folder
script_folder = Path(__file__).parent
project_folder = script_folder.parent.parent


all_contributorsrc = project_folder / ".all-contributorsrc"

ascii_checkmark = "  \u2713"
ascii_cross = "  \u2717"

README_CONTRIBUTORS_SECTION = """
## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

"""


@dataclass
class GitHubProject:
    github_owner: str
    github_project: str


    @classmethod
    def from_url(cls, url: str) -> Self:
        return github_project_from_url(url)


def github_project_from_url(url: str) -> GitHubProject:
    is_github_project = "github.com" in url
    if not is_github_project:
        raise ValueError("This project is not hosted on GitHub")
    
    github_owner = url.split("/")[-2]
    github_project = url.split("/")[-1]
    
    # remove the `.git` extension if present
    github_project = github_project.rstrip(".git")

    return GitHubProject(github_owner=github_owner, github_project=github_project)

def create_all_contributorsrc(file_path, gh_project: GitHubProject):
    content = {
        "projectName": f"{gh_project.github_project}",
        "projectOwner": f"{gh_project.github_owner}",
        }
    with open(file_path, "w") as file:
        file.write(json.dumps(content, indent=4))
    
def main():

    print("\nChecking project docs...")

    print("\nReading git origin url...")
    git_origin_url = os.popen("git config --get remote.origin.url").read().strip()
    print(f"{ascii_checkmark} git_origin_url: {git_origin_url}")

    print("\nChecking if project is hosted on GitHub...")
    try:
        gh_project = GitHubProject.from_url(git_origin_url)
        print(f"{ascii_checkmark} GitHub project found: {gh_project.github_owner}/{gh_project.github_project}")
    except ValueError:
        print(f"c{git_origin_url} does not appear to be a github project. Exiting...")
        return

    print("\nChecking for .all-contributorsrc file...")
    if all_contributorsrc.exists():
        print(f"{ascii_checkmark} .all-contributorsrc file found in project root.")
    else:
        print(f"{ascii_cross} .all-contributorsrc file not found in project root. Creating one...")
        create_all_contributorsrc(file_path=all_contributorsrc, gh_project=gh_project)

    print("\nChecking README.md for `## Contributors` section...")
    readme = project_folder / "README.md"
    if not readme.exists():
        print(f"{ascii_cross} README.md not found in project root.")
        return
    with open(readme, "r") as file:
        readme_content = file.read()
        has_contributors_section = "## Contributors" in readme_content
        if has_contributors_section:
            print(f"{ascii_checkmark} README.md has a `## Contributors` section.")
        else:
            print(f"{ascii_cross} README.md does not have a `## Contributors` section. Adding one...")
        
            with open(readme, "a") as file:
                file.write(README_CONTRIBUTORS_SECTION)

    print("\nProject docs check complete.")

if __name__ == "__main__":
    main()