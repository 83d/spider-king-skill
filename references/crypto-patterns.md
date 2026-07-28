# Crypto Patterns

Use this file when signatures, encryption, or helper outputs look suspicious.

## Standard-looking helpers that are often not standard

- `md5`
- `sha1`
- `btoa`
- `atob`
- `hmac`
- `aes`
- `rsa`

## Fast recognition checklist

- length matches a common digest size
- alphabet matches hex, Base64, URL-safe Base64, or a custom alphabet
- padding matches a standard encoder
- output changes with timestamp, page, or session state
- helper reads DOM, globals, or side-script state
- output is digest plus a short suffix digest, checksum nibble, or version fragment
- a UUID, nonce, or session value looks standard at first glance but contains an inserted fixed-width segment, prefix, or checksum-derived fragment
- the apparent key, iv, seed, or hash source comes from slicing, concatenating, trimming, or decorating a config field instead of using it directly

## Fixed-input validation loop

1. freeze a tiny input such as `"abc"`
2. freeze a live input such as a captured timestamp
3. compare browser output with local output
4. compare intermediate strings, not only final digests

## Cross-runtime porting loop

When porting JS logic to Python or another runtime:

1. freeze the same config blob, timestamp, nonce, UUID source, and fingerprint vector
2. compare normalization outputs first, such as compact JSON, sliced key material, prefixed payloads, or checksum inputs
3. compare the final cookie, token, or sign output only after the intermediate forms match
4. keep one deterministic parity vector before trusting live traffic

## Common failure modes

- standard Base64 library used against a patched alphabet
- standard MD5 used against a custom string-to-word packing step
- URL-encoding mismatch before hashing
- wrong timestamp precision
- hidden page or session state included in the input
- correct hash function applied to the wrong JSON serialization, item order, or compactness rule
- standard UUID or random hex used where the protocol expects a structurally constrained local identifier
- apparent key or iv used directly when the page normalizes it through slice, concat, trim, or wrapper removal first
- recomputing an accepted bundle or version hash from current file bytes when the client actually uses an embedded compatibility id

## Delivery rule

Do not call crypto "done" until fixed-input self-checks are in the collector and any cross-runtime port has at least one deterministic parity vector.
