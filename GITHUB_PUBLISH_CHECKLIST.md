# Manual GitHub publish checklist

## Before the first commit

- [ ] Open the extracted public release folder in VS Code and initialize Git in that folder.
- [ ] Run the README test, demo and reproduction commands. On the reference runtime compare both result hashes.
- [ ] Review VS Code's staged files or run `git diff --cached --name-only`. Include `.gitignore`, `.gitattributes`, and `results/public_v1.json`. Check that local outputs, private inputs, reviewer material, credentials and settings stay outside the commit.
- [ ] Confirm the public statement of AI assistance and the fixture-only scope. Check the H1 failure, H2 effect size and uncertainty against the frozen evidence.
- [ ] Decide licensing separately. The release files contain no license grant.

## When ready to publish

- [ ] Commit the reviewed files, create the intended GitHub repository and push manually from VS Code.
- [ ] Verify that GitHub renders the README, all documentation opens, and the original evidence hash survives a clean checkout.
- [ ] Confirm that the description accurately identifies a deterministic public synthetic experiment. Pending validations include independent authorship and adjudication, protocol freeze, protected evaluation and actual-model feasibility.
