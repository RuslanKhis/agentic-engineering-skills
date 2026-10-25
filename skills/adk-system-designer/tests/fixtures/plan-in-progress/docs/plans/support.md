# Plan

```yaml
- goal: G01
  phase: 1
  type: implementation
  total: 2-3
  owner: Ana
  blocked_by: []
  contracts: [C1, C2]
  security: [SB01]
- goal: G02
  phase: 1
  type: implementation
  total: 2-4
  owner: Ana
  blocked_by: [G01]
  contracts: [C3]
- goal: G03
  phase: 1
  type: implementation
  total: 1-2
  owner: Ana
  blocked_by: [G01]
  contracts: [C5]
- goal: G04
  phase: 1
  type: journey
  total: 1-2
  owner: Ana
  blocked_by: [G02, G03]
  contracts: [C1, C2, C3, C5]
- goal: G05
  phase: 1
  type: presentation
  total: 2-3
  owner: Ana
  blocked_by: [G04, D3]
```
