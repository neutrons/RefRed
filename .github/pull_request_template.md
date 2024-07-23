## Description of work:

Check all that apply:
- [ ] added [release notes](https://github.com/neutrons/RefRed/blob/next/docs/release_notes.rst) (if not, provide an explanation in the work description)
- [ ] updated documentation
- [ ] Source added/refactored
- [ ] Added unit tests
- [ ] Added integration tests
- [ ] Verified that tests requiring the /SNS and /HFIR filesystems pass without fail

**References:**
- Links to IBM EWM items:
- Links to related issues or pull requests:


# Manual test for the reviewer
([instructions to set up the environment](https://github.com/neutrons/RefRed/blob/next/docs/developer/testing.rst#running-manual-tests-in-a-pull-request))

Start RefRed GUI
```bash
(refred-dev)> PYTHONPATH=$(pwd):$PYTHONPATH ./scripts/start_refred.py
```
Or run tests
```bash
(refred-dev)> pytest test/unit/RefRed/test_main.py
```

# Check list for the reviewer
- [ ] [release notes](https://github.com/neutrons/RefRed/blob/next/docs/release_notes.rst) updated, or an explanation is provided as to why release notes are unnecessary
- [ ] best software practices
    + [ ] clearly named variables (better to be verbose in variable names)
    + [ ] code comments explaining the intent of code blocks
- [ ] All the tests are passing
- [ ] The documentation is up to date
- [ ] code comments added when explaining intent
