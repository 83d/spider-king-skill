# Verifier Replay Playbook

Use this reference when:

- data requests are gated behind captcha, one-shot verification, or click-order challenges
- there is no meaningful business signer, but requests still fail until a verifier passes
- browser clicks appear to unlock the next request

## Core rule

The verifier output is the real dynamic parameter.

## Working method

1. classify the verifier family before lifting fields:
   - slider, point-click, ordered-click, rotate, or another verifier branch
   - old and new generations of one vendor can still have incompatible fields and proof builders
2. freeze one verifier round end to end:
   - prehandle or load response
   - callback ids or random keys
   - asset URLs and downloaded images
   - verifier token, work factor, or round id
   - final verify request and response
3. determine what output authorizes the next business request
4. split the answer path by verifier type:
   - point-click or ordered-click: prompt extraction, hit localization, proof packaging
   - slider or image-derived: restored-image coordinate, display coordinate, submitted coordinate, behavior trace
5. solve or reconstruct that output locally
6. replay the verifier in protocol form
7. send the business request with the resulting token, cookie, coordinates, or grant

## Common traps

- hunting for a fake business-layer signer while ignoring the verifier
- automating clicks instead of understanding the verifier payload
- treating the verifier as UI-only behavior
- mixing token, images, callbacks, or proof fields across adjacent verifier rounds
- treating prompt OCR or image matching alone as proof of verifier success
- mixing restored-image pixels, rendered UI coordinates, and submitted proof coordinates
- carrying fields from one verifier family or generation into another because the page role looks similar

## Delivery rule

Do not simulate UI interaction in the final solution. Reproduce the verifier as protocol data.
