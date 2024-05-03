# References
- EWM #
<!-- Links to related issues or pull requests -->

# Description of the changes:
<!-- description here. -->

# Manual test for the reviewer
([instructions to set up the environment](https://github.com/neutrons/RefRed/blob/next/dev-docs/testing.rst#running-manual-tests-in-a-pull-request))

Start RefRed GUI
```bash
(refred-dev)> PYTHONPATH=$(pwd):$PYTHONPATH ./scripts/start_refred.py
```
Or run tests
```bash
(refred-dev)> pytest test/unit/RefRed/test_main.py
```

# Check list for the reviewer
- [ ] I have verified the proposed changes
- [ ] Author included tests for the proposed changes
- [ ] best software practices
    + [ ] clearly named variables (better to be verbose in variable names)
    + [ ] code comments explaining the intent of code blocks
    + [ ] new functions and classes detailed docstrings, parameters documented
- [ ] All tests are passing
- [ ] Documentation is up to date

# Check list for the author
- [ ] I have added tests for my changes
- [ ] I have updated the documentation accordingly
- [ ] I included a link to IBM EWM Story or Defect
