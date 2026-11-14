# Sequential LDB2 prefab validation — 2026-11-14

Both readers now enforce the MP2 revision-34 registration rule. A negative ID
owns its buffers without registering a template; an ID equal to the current
template count registers the next template; a smaller nonnegative ID reuses one.
A larger ID raises a sequence error immediately after the ID is read, before
reading the unique-render flag or geometry payload. Reuse keeps the existing
render/collision sharing rules and each instance's bounds.

The Python change is in `max_payne_sdk/max_ldb2.py`. The canonical C++ change
is in the separate workspace project `max payne formats/src/mp2/Ldb2Document.cpp`.
This importer repository does not own that C++ library. Its exact implementation
and test delta is supplied as
[canonical-prefab-sequence.patch](patches/canonical-prefab-sequence.patch), with
[before/after source hashes](patches/canonical-prefab-sequence-pins.json).
The patch also changes the recovery fixture's first template from ID 42 to ID 0.

Apply the patch from the canonical formats checkout, after checking its input
hashes. `--ignore-space-change` allows LF patch context to match CRLF source:

```text
git apply --check --ignore-space-change <path-to-canonical-prefab-sequence.patch>
git apply --ignore-space-change <path-to-canonical-prefab-sequence.patch>
cmake --build build-mp2-current --config Release --target verify_mp2_ldb2 verify_mp2_recovery verify_mp2_dynamic_frames
ctest --test-dir build-mp2-current -C Release -R "^mp2_(ldb2|recovery|dynamic_frames)$" --output-on-failure
```

The workspace copy is already patched. Forward application was checked against
saved original sources, and reverse application was checked against the changed
sources. The patch contains only this task's changes, not the whole untracked
canonical source tree.

## Regression coverage

- First ID 1 or 2147483647, a later ID 2 after template 0, and skipped IDs after
  negative-ID records are rejected with both unique-render flag values.
- Complete malformed buffers are rejected as sequence errors. Python additionally
  checks the cursor on truncated input to show that geometry is not consumed.
- Multiple sequential templates, repeated references, negative IDs between
  templates, registration reset and independent lighting/render flags remain valid.
- The C++ writer's reparse also rejects malformed registration.
- The old Python reader from commit 3157000 accepts all ten complete malformed
  cases; the fixed reader rejects all ten. Compiling the new C++ tests with the
  saved old reader fails with `Skipped prefab ID was not rejected at registration`.

## Verification

The Python suite passes 47 tests and compileall. Python also parses all 56
hash-retained original LDB files (28 MP1 and 28 MP2) with no failures or input
changes. The three focused CTest tests
`mp2_ldb2`, `mp2_recovery` and `mp2_dynamic_frames` pass. The C++ corpus check
reads and writes 28 retained original MP2 files byte for byte and checks an
isolated float edit; original inputs and their test copies retain their hashes.
The test executable reads inputs only and keeps modified bytes in memory.

Corpus receipts are in [prefab-validation.json](prefab-validation.json). Two
previously inventoried MP2 inputs, Upper East Side and Police Station, remain
unlocated by hash and are excluded. No generated level is substituted for them.
These checks establish parser compatibility and byte preservation, not game,
Maya viewport, animation or physics equivalence. No game DLL was changed.
