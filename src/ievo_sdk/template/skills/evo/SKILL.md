# EVO — Self-Evolution Skill

> Every agent carries this skill. It turns mistakes into permanent improvements.

## Trigger

Activate EVO when:
- An output is rejected or needs rework
- You notice a pattern of repeated mistakes
- User corrects your approach or assumptions
- A downstream agent reports issues with your output

## Workflow

```
1. IDENTIFY  → What exactly went wrong?
2. CLASSIFY  → Bug | Misunderstanding | Gap | Drift | Regression
3. ROOT CAUSE → Why did it happen? (5-whys)
4. FORMULATE → Draft a rule/patch for ROLE.md
5. PROPOSE   → Show the mutation to the user
6. APPLY     → Update ROLE.md (only after approval)
7. LOG       → Append to EVOLUTION_LOG.md
8. CONFIRM   → Verify the fix prevents recurrence
```

## Evolution Log Entry Format

```markdown
## EVO-{NNN} — {title}
- **Date**: {YYYY-MM-DD}
- **Type**: Bug | Misunderstanding | Gap | Drift | Regression
- **Trigger**: {what happened}
- **Root cause**: {why}
- **Mutation**: {what changed in ROLE.md}
- **Confidence**: {low|medium|high}
```

## Rules

1. **Never update ROLE.md without user approval**
2. One mutation per evolution — keep changes atomic
3. Always log, even if the user rejects the mutation
4. Regression = revert + log why the previous fix was wrong
5. If confidence is low, propose but don't apply
6. Review last 5 entries before proposing — avoid contradictions
