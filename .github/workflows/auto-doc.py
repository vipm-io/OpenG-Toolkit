from __future__ import annotations
import os
import json
from pathlib import Path
from typing import Self
from dataclasses import dataclass

import xmltodict
from pydantic import BaseModel, Field

LV_VERSION = "20.0"

# get this scripts folder
script_folder = Path(__file__).parent
project_folder = script_folder.parent.parent


all_contributorsrc = project_folder / ".all-contributorsrc"

ascii_checkmark = "  ✅"
ascii_cross = "  ❌"
ascii_warning = "  ❗"

README_CONTRIBUTORS_SECTION = """
## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

"""


class ReadmeContext(BaseModel):
    package_display_name: str
    package_name: str
    package_description: str
    github_project_name: str
    github_project_owner: str


README_STRUCTURE = """
# {package_display_name}

## Installation

## How to Contribute

## Contributors

"""


README_TITLE_SECTION = """

# {package_display_name} ![image](source/images/icon.png)

[![Image](https://www.vipm.io/package/{package_name}/badge.svg?metric=installs)](https://www.vipm.io/package/{package_name}/) [![Image](https://www.vipm.io/package/{package_name}/badge.svg?metric=stars)](https://www.vipm.io/package/{package_name}/)
[![ci-checks](https://github.com/{github_project_owner}/{github_project_name}/actions/workflows/ci.yml/badge.svg)](https://github.com/{github_project_owner}/{github_project_name}/actions/workflows/ci.yml)
[![All Contributors](https://img.shields.io/github/all-contributors/{github_project_owner}/{github_project_name}?color=ee8449&style=flat-square)](#contributors)

![image](source/images/icon.png)

{package_description}

![image](source/images/functions_palette.png)

"""


def render_template(ctx: BaseModel, template: str):
    rendered = template.format(**ctx.dict()).strip()
    return "\n" + rendered + "\n"


README_INSTALLATION_SECTION = """

## Installation

[Install the {package_display_name} with VIPM](https://www.vipm.io/package/{package_name}/) (a.k.a {package_name})

"""

README_HOW_TO_CONTRIBUTE_SECTION = """

## How to Contribute

Take a look at the [Help Wanted](https://github.com/{github_project_owner}/{github_project_name}/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) issues list. If it's your first contribution or you're not extremely familiar with this library, you might want to look at the [Good First Issues](https://github.com/{github_project_owner}/{github_project_name}/issues?q=is%3Aissue+is%3Aopen+label%3Agood-first-issue) list.  If you see an issue that looks like one you can complete, add a comment to the issue stating you'd like to work on it, and a maintainer will follow up and "assigned" to you. You then create a branch and then submit your contribution in the form of a [Pull Requests](https://github.com/{github_project_owner}/{github_project_name}/pulls).

"""


@dataclass
class OpenGProject:
    package_name: str


@dataclass
class GitHubProject:
    project_owner: str
    project_name: str

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

    return GitHubProject(project_owner=github_owner, project_name=github_project)


def create_all_contributorsrc(file_path, gh: GitHubProject):
    content = {
        "projectName": f"{gh.project_name}",
        "projectOwner": f"{gh.project_owner}",
    }
    with open(file_path, "w") as file:
        file.write(json.dumps(content, indent=4))


def get_xml_tag_value(xml_string, xml_tag):
    return xml_string.split(f"<{xml_tag}>")[1].split(f"</{xml_tag}>")[0].strip()


def get_package_name(vipb_file):
    vipb_string = vipb_file.read_text()
    xml_tag = "Package_File_Name"
    package_file_name = get_xml_tag_value(vipb_string, xml_tag)
    return package_file_name


def get_package_display_name(vipb_file):
    vipb_string = vipb_file.read_text()
    xml_tag = "Product_Name"
    package_display_name = get_xml_tag_value(vipb_string, xml_tag)
    return package_display_name


def main():
    ##########################################################################################
    # Setup
    ##########################################################################################

    print("\nChecking project docs...\n")

    ##########################################################################################
    # Reading git origin url
    ##########################################################################################
    git_origin_url = os.popen("git config --get remote.origin.url").read().strip()
    print(f"{ascii_checkmark} git_origin_url: {git_origin_url}")

    # Checking if project is hosted on GitHub...
    try:
        gh = GitHubProject.from_url(git_origin_url)
        print(
            f"{ascii_checkmark} GitHub project found: {gh.project_owner}/{gh.project_name}"
        )
    except ValueError:
        print(f"c{git_origin_url} does not appear to be a github project. Exiting...")
        return

    ##########################################################################################
    # Check VI Package Info
    ##########################################################################################

    vipb_file = project_folder / "source" / ".vipb"
    vipb_string = vipb_file.read_text()

    vipb_dict = xmltodict.parse(vipb_string)

    # print(json.dumps(vipb_dict, indent=4))

    if not vipb_file.exists():
        print(f"{ascii_cross} .vipb file not found in project source folder")
        raise FileNotFoundError(".vipb file not found in project source folder")

    # sub-dictionaries
    vipb_settings = vipb_dict["VI_Package_Builder_Settings"]
    vipb_library_settings = vipb_settings["Library_General_Settings"]
    vipb_advanced_settings = vipb_settings["Advanced_Settings"]
    vipb_description = vipb_advanced_settings["Description"]

    # values
    package_name = vipb_library_settings["Package_File_Name"]
    package_display_name = vipb_library_settings["Product_Name"]
    package_description = vipb_description["Description"]

    print(f"{ascii_checkmark} Package name: {package_name}")
    print(f"{ascii_checkmark} Display name: {package_display_name}")
    print(f"{ascii_checkmark} Description: {package_description}")

    readme_ctx = ReadmeContext(
        package_display_name=package_display_name,
        package_name=package_name,
        package_description=package_description,
        github_project_name=gh.project_name,
        github_project_owner=gh.project_owner,
    )

    ##########################################################################################
    # Checking for .all-contributorsrc file
    ##########################################################################################
    if all_contributorsrc.exists():
        print(f"{ascii_checkmark} .all-contributorsrc file found in project root.")
    else:
        print(
            f"{ascii_warning} .all-contributorsrc file not found in project root. Creating one..."
        )
        create_all_contributorsrc(file_path=all_contributorsrc, gh=gh)

    ##########################################################################################
    # Checking README.md exists
    ##########################################################################################
    readme = project_folder / "README.md"
    if not readme.exists():
        print(f"{ascii_warning} README.md not found in project root. Creating one...")
        # write an empty file
        with open(readme, "w") as file:
            file.write(render_template(readme_ctx, README_TITLE_SECTION).lstrip())
            file.write(render_template(readme_ctx, README_INSTALLATION_SECTION))
            file.write(render_template(readme_ctx, README_HOW_TO_CONTRIBUTE_SECTION))

    ##########################################################################################
    # Checking README.md for `## Contributors` section
    ##########################################################################################
    readme = project_folder / "README.md"
    if not readme.exists():
        print(f"{ascii_warning} README.md not found in project root")
        return
    with open(readme, "r") as file:
        readme_content = file.read()
        has_contributors_section = "## Contributors" in readme_content
        if has_contributors_section:
            print(f"{ascii_checkmark} README.md has a `## Contributors` section")
        else:
            print(
                f"{ascii_warning} README.md does not have a `## Contributors` section. Adding one..."
            )

            with open(readme, "a") as file:
                file.write(README_CONTRIBUTORS_SECTION)

    ##########################################################################################
    # Check for .lvversion file
    ##########################################################################################

    dot_lvversion = project_folder / ".lvversion"
    if not dot_lvversion.exists():
        print(
            f"{ascii_warning} .lvversion file not found in project root. Creating one..."
        )
        with open(dot_lvversion, "w") as file:
            file.write(LV_VERSION)
        print(f"{ascii_checkmark} .lvversion file created and set to '{LV_VERSION}'.")

    ##########################################################################################
    # Cleanup
    ##########################################################################################

    print("\nProject docs check complete!")


if __name__ == "__main__":
    main()
