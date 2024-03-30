# Guide for Upgrading Library Sources for OpenG 6.0 Release

Steps to Upgrade Sources

- [ ] Add `.github/workflows/ci.yml` (copy from OpenG Variant Library) to project (this will help automate and enforce maintenance)
- [ ] Upgrade Sources to LV2020 (CI will fail until this is done)
- [ ] Separate Compiled Code for all files (CI will fail until this is done)
- [ ] Move VIs into a `.lvlib`
- [ ] Update License to mention "Project Contributors (See README.md)"
- [ ] Change .vipb package version to `6.0.0`
- [ ] Update .vipb file with Copyright notice and mention "Project Contributors (See README.md)"
- [ ] Update .vipb file with Author Info (VIPM Community)
- [ ] Create a `LICENSE` file in the root directory (copy from user docs folder)

And, before release:

- [ ] Update .vipb file with release notes

Additional tasks

- [ ] Upgrade unit tests to use Caraya

Auto-doc updates needed:

- [ ] Check for VIs in an `.lvlib` (check for presence of lvlib in correct location)
- [ ] Update .vipb file with Copyright notice (end date and "Project Contributors")
- [ ] Update .vipb file with Author Info (VIPM Community)
