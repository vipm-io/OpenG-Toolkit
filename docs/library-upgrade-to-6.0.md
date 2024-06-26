# Guide for Upgrading Library Sources for OpenG 6.0 Release

## Checklist (Copy everything below into a new issue in the library/project called "6.0 Tasks")

This was copied from [List Template Here](https://github.com/vipm-io/OpenG-Toolkit/blob/main/docs/library-upgrade-to-6.0.md). Please update the template when changes/additions to this list are needed.

Contributor Tasks
- [ ] LabVIEW tasks
  - [ ] Upgrade Sources to LV2020 (CI will fail until this is done)
  - [ ] Separate Compiled Code for all files (CI will fail until this is done)
  - [ ] Move VIs into a `.lvlib`
- [ ] License file
  - [ ] Update License to mention "Project Contributors (See README.md)"
  - [ ] Create a `LICENSE` file in the root directory (copy from user docs folder)
- [ ] VIPB Settings
  - [ ] Change .vipb package version to `6.0.0`
  - [ ] Update .vipb file with Copyright notice and mention "Project Contributors (See README.md)"
  - [ ] Update .vipb file with Author Info (VIPM Community)
  - [ ] Change the .vipb's License Text file to link to the LICENSE in the root folder of project
  - [ ] Update .vipb/.vipc dependencies
    - [ ] From the VI Package Builder, edit the VIPC file to update OpenG Toolkit dependencies to version 6.0
    - [ ] Apply the new configuration, to upgrade all the packages
    - [ ] Re-scan for dependencies to make sure they are updated
    - [ ] Review dependencies to see if they are needed/accurate
- [ ] Unit Tests
  - [ ] Copy over the 'build support' folder from OpenG Variant
  - [ ] Remove the .vit test templates
  - [ ] Upgrade unit tests to use Caraya (optional, since could be done later)


Admin Tasks (to be done by Maintainer)
- [ ] CI
  - [ ] Enable GitHub Actions for repo
  - [ ] Add `.github/workflows/ci.yml` (copy from OpenG Variant Library) to project (this will help automate and enforce maintenance)
- [ ] Release
  - [ ] Update .vipb file with release notes
  - [ ] Assign all issues and PRs to the milestone
  - [ ] Create a Release with `v6.0.0` tag and name
    - [ ] Generate Release notes
  - [ ] Upload package to vipm.io

## Admin To Do

Auto-doc updates needed for automation/validation (Affects all OpenG Packages)
- [ ] Check for VIs in an `.lvlib` (check for presence of lvlib in correct location)
- [ ] Update .vipb file with Copyright notice (end date and "Project Contributors")
- [ ] Update .vipb file with Author Info (VIPM Community)
