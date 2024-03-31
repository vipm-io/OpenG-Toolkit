from __future__ import annotations
import os
import json
from pathlib import Path
import re
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
    year: int = 2024


README_STRUCTURE = """
# {package_display_name}

## Installation

## How to Contribute

## Contributors

"""


README_TITLE_SECTION = """

# {package_display_name}

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

Take a look at the [Help Wanted](https://github.com/{github_project_owner}/{github_project_name}/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) issues list. If it's your first contribution or you're not extremely familiar with this library, you might want to look at the [Good First Issues](https://github.com/{github_project_owner}/{github_project_name}/issues?q=is%3Aissue+is%3Aopen+label%3Agood+first+issue) list.  If you see an issue that looks like one you can complete, add a comment to the issue stating you'd like to work on it, and a maintainer will follow up and "assigned" to you. You then create a branch and then submit your contribution in the form of a [Pull Requests](https://github.com/{github_project_owner}/{github_project_name}/pulls).

"""


BSD_LICENSE = """
{package_display_name}

Copyright (c) 2002-{year} Project Contributors (See CONTRIBUTORS.md)

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
  
  * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
  
  * Neither the name of the <organization> nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

    # also check for presense of a file named "LabVIEW 2009" (or similar) in the project root
    # if it exists, then we'll delete it

    labview_version_file_pattern = "LabVIEW [0-9]{4}"
    re.compile(labview_version_file_pattern)
    for file in project_folder.iterdir():
        if re.match(labview_version_file_pattern, file.name):
            print(
                f"{ascii_warning} Found a LabVIEW version file '{file.name}' in project root. Deleting..."
            )
            file.unlink()


    ##########################################################################################
    # Check for source\user docs\License Agreement.txt
    ##########################################################################################
            
    NEW_COPYRIGHT_LINE = f"Copyright 2002-{readme_ctx.year} Project Contributors (See CONTRIBUTORS.md)"
            
    old_license_agreement = project_folder / "source" / "user docs" / "License Agreement.txt"

    if old_license_agreement.exists():
        print(f"{ascii_warning} Found old license agreement file. Moving to new `./LICENSE` location...")
        new_license = project_folder / "LICENSE"
        old_license_agreement.rename(new_license)
        print(f"{ascii_checkmark} Moved old license agreement file to new location: {new_license}")

        # find the line that begins with "Copyright" and update it:
        with open(new_license, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith("Copyright"):
                    print(f"{ascii_warning} Found old copyright line: {line.strip()}")
                    print(f"{ascii_checkmark} Updating to new copyright line: {NEW_COPYRIGHT_LINE.strip()}")
                    lines[i] = NEW_COPYRIGHT_LINE + "\n"
                    break
        with open(new_license, "w") as file:
            file.writelines(lines)


    ##########################################################################################
    # Check for .gitignore file
    ##########################################################################################
    
    GIT_IGNORE = """
# Python Virtual Environment
.venv/

# LabVIEW Local Settings
*.aliases
*.lvlps

# Dragon Meta Folder
.dragon/

# Temp Build Folder
.source/

# Built Package
*.vip
"""

    gitignore = project_folder / ".gitignore"

    if not gitignore.exists():
        print(f"{ascii_warning} .gitignore file not found in project root. Creating one...")
        with open(gitignore, "w") as file:
            file.write(GIT_IGNORE)
        print(f"{ascii_checkmark} .gitignore file created.")


    # ##########################################################################################
    # # Update .vipb file meta info
    # ##########################################################################################
    
    # vipb_file = project_folder / "source" / ".vipb"

    # vipb_changed = False
    # if vipb_file.exists():
    #     vipb_string = vipb_file.read_text()
    #     vipb_dict = xmltodict.parse(vipb_string)
    #     vipb_settings = vipb_dict["VI_Package_Builder_Settings"]
    #     vipb_library_settings = vipb_settings["Library_General_Settings"]
    #     vipb_advanced_settings = vipb_settings["Advanced_Settings"]
    #     vipb_description = vipb_advanced_settings["Description"]
    #     if vipb_description["Copyright"] != NEW_COPYRIGHT_LINE.strip():
    #         vipb_description["Copyright"] = NEW_COPYRIGHT_LINE.strip()
    #         vipb_changed = True
    #     if vipb_description["Packager"] != "VIPM Community":
    #         vipb_description["Packager"] = "VIPM Community"
    #         vipb_changed = True
    #     if vipb_description["URL"] != f"https://www.vipm.io/package/{package_name}":
    #         vipb_description["URL"] = f"https://www.vipm.io/package/{package_name}"
    #         vipb_changed = True
    #     if vipb_library_settings["Company_Name"] != "VIPM Community":
    #         vipb_library_settings["Company_Name"] = "VIPM Community"
    #         vipb_changed = True
    #     if vipb_library_settings["Library_License"] != "BSD-3-clause":
    #         vipb_library_settings["Library_License"] = "BSD-3-clause"
    #         vipb_changed = True
    #     if vipb_library_settings["Package_LabVIEW_Version"] != LV_VERSION:
    #         vipb_library_settings["Package_LabVIEW_Version"] = LV_VERSION
    #         vipb_changed = True
    #     if vipb_advanced_settings["License_Agreement_Filepath"] != "..\\LICENSE":
    #         vipb_advanced_settings["License_Agreement_Filepath"] = "..\\LICENSE"
    #         vipb_changed = True

    # if vipb_changed:
    #     with open(vipb_file, "w") as file:
    #         vipb_string = xmltodict.unparse(vipb_dict, pretty=True)
    #         # convert eols to windows style
    #         vipb_string = vipb_string.replace("\n", "\r\n")
    #         file.write(xmltodict.unparse(vipb_dict, pretty=True))
    #     print(f"{ascii_checkmark} Updated .vipb file with new meta info.")


    ################################################################################################
    # Check if 'dev docs/ToDo.txt' is an empty file and delete it, if so
    ################################################################################################
    
    dev_docs_folder = project_folder / "dev docs"
    todo_file = dev_docs_folder / "ToDo.txt"
    if todo_file.exists():
        if not todo_file.read_text().strip():
            print(f"{ascii_warning} Found empty 'ToDo.txt' file. Deleting...")
            todo_file.unlink()
            print(f"{ascii_checkmark} Deleted empty 'ToDo.txt' file.")

    # check if dev_docs_folder is empty and delete it
    if not list(dev_docs_folder.iterdir()):
        print(f"{ascii_warning} Found empty 'dev docs' folder. Deleting...")
        dev_docs_folder.rmdir()
        print(f"{ascii_checkmark} Deleted empty 'dev docs' folder.")
        

    ##########################################################################################
    # Cleanup
    ##########################################################################################

    print("\nProject docs check complete!")


if __name__ == "__main__":
    main()
