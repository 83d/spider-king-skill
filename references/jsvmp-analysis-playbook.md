# JSVMP Analysis Playbook

Use this file when the target wraps logic inside a custom VM or bytecode interpreter.

## Recognition signals

- opcode arrays
- dispatch loops switching on byte values
- tiny VM runtime with a large encoded program
- helpers hidden behind interpreter calls instead of direct JavaScript

## Working method

1. locate the VM entry point
2. identify what inputs go into the VM and what outputs come out
3. test the smallest closer-to-browser local execution path before full VM recovery; a real embedded engine or host runtime may execute the VM with far less work than devirtualization
4. avoid full VM recovery unless the protocol truly depends on it
5. prefer isolating the one helper output needed for the request
6. move to local execution or helper wrapping before attempting full devirtualization

## Common traps

- trying to devirtualize the whole VM when only one result matters
- missing side inputs passed into the VM entry point
- treating failure under Node, jsdom, or a thin shim as proof the VM cannot run locally at all

## Delivery rule

If a tiny helper wrapper around the VM output is enough for protocol replay, use that instead of heroic full recovery.
