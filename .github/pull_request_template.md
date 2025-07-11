## Description of work:

Check all that apply:

- [ ] Source added/refactored
- [ ] Added unit tests
- [ ] Added integration tests
- [ ] Verified that tests requiring the /SNS and /HFIR filesystems pass without fail
- [ ] updated documentation and checked that it looks correct in the [pull request preview](https://docs.readthedocs.com/platform/stable/pull-requests.html)

**References:**

- Links to IBM EWM items:
- Links to related issues or pull requests:

# Manual test for the reviewer

([instructions to set up the environment](https://github.com/neutrons/RefRed/blob/next/docs/developer/testing.rst#running-manual-tests-in-a-pull-request))

Start RefRed GUI

```bash
(refred)
$ PYTHONPATH=$(pwd):$PYTHONPATH ./scripts/start_refred.py
```

Or run tests

```bash
$ pixi run test
```

# Check list for the reviewer

- [ ] best software practices
  - [ ] clearly named variables (better to be verbose in variable names)
  - [ ] code comments explaining the intent of code blocks
- [ ] All the tests are passing
- [ ] The documentation is up to date and looks correct in the [pull request preview](https://docs.readthedocs.com/platform/stable/pull-requests.html)
- [ ] code comments added when explaining intent
