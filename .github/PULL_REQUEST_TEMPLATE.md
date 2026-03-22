## Summary

- What changed?
- Why was it needed?

## Checklist

- [ ] Change is for authorized, defensive use only
- [ ] README or docs updated if behavior changed
- [ ] Tests added or updated where relevant
- [ ] `python -m unittest -q tests/test_nosey.py` passes
- [ ] `python NetNosey --help` works
- [ ] `python WebNosey --help` works

## Validation

Describe what you ran locally:

```bash
python -m unittest -q tests/test_nosey.py
python NetNosey --help
python WebNosey --help
```

## Notes

Include anything reviewers should pay attention to, such as new plugin behavior, fixture updates, or CI changes.