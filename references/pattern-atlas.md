# Pattern Atlas

Use this file when the target already resembles a recurring pattern and you want the shortest proven first move.

## Pattern A: The endpoint on the page is fake

Symptoms:

- page code hooks `/api/match/...`
- wire uses `/api/question/...` or another path
- browser request succeeds but replaying the visible path fails

Action:

- trust the network path
- trace request initiators
- document the decoy path
- code against the live path only

## Pattern B: The business param is a decoy

Symptoms:

- page code builds `token`
- wire sends `m`, `f`, or another field
- request wrapper mutates data before send

Action:

- reverse the wrapper first
- diff business-layer params against final payload
- rebuild the wrapper logic, not the decoy field

## Pattern C: Standard helper is patched

Symptoms:

- `md5`, `btoa`, `atob`, `sha1`, or similar names exist
- local reproduction with standard libraries does not match browser output

Action:

- freeze fixed test vectors
- port the exact helper implementation
- verify helper outputs before using them in requests

## Pattern D: First response is not data, but bootstrap

Symptoms:

- first request returns JS, `Set-Cookie`, offset scripts, or challenge tokens
- first request returns non-final HTML such as `412` plus inline bootstrap state and one or more linked challenge assets
- replay works only after the bootstrap response is processed
- the same document URL returns the real HTML only on a later pass after challenge state is rebuilt

Action:

- treat bootstrap as part of the protocol contract
- test whether the challenged document route itself is the real business path
- execute or emulate it locally
- carry resulting cookies or globals into the next request
- validate replay with semantic anchors, not status alone

## Pattern E: Only one page breaks

Symptoms:

- pages 1 to 4 work
- page 5 fails or returns hints, strings, or anti-bot signals

Action:

- diff headers and cookies by page
- test page-specific `User-Agent`, referer, or ordering rules
- encode the exception narrowly

## Pattern F: Answer or data is account-bound

Symptoms:

- page text mentions `sessionid`
- different accounts produce different sums or answers
- submit works only with the same session that collected the data

Action:

- make `sessionid` explicit in the collector
- keep fetch and submit under the same account
- verify with the same session before blaming signer logic

## Pattern G: Tiny side assets carry the whole signer

Symptoms:

- `.wasm`, `/offset`, challenge JS, or font files appear trivial
- main bundle is noisy but side asset changes output decisively

Action:

- inspect side assets early
- instantiate WASM locally
- execute bootstrap JS locally
- decode fonts locally

## Pattern H: Dynamic fonts hide the payload

Symptoms:

- numeric values appear as glyphs or meaningless text
- response includes font URLs or embedded font data

Action:

- fetch the font asset
- derive the codepoint-to-digit map
- decode the payload locally

## Pattern I: One-shot verifier, captcha, or click challenge

Symptoms:

- next request only works after a verification step
- no meaningful JS signer exists for the business API

Action:

- treat the verifier output as the real dynamic parameter
- solve and replay the verifier in protocol form
- do not simulate clicks in the final solution

## Pattern J: Response data is encoded, compressed, or split

Symptoms:

- HTTP status is normal but payload looks like gibberish, digit soup, escaped code, glyphs, or binary
- business data only appears after a decode helper, font map, protobuf parser, or compression layer
- the response body shape changes after a local decode step, not after another request

Action:

- freeze the raw payload first
- trace the first consumer of the raw payload
- identify decode order, keys, maps, or parsers
- rebuild the decoder locally
- validate local decode on the exact captured payload before scaling

## Pattern K: Transport is GraphQL, WebSocket, or a binary envelope

Symptoms:

- the URL stays stable but `operationName`, frame type, or binary opcode changes
- request bodies carry nested `variables`, message IDs, or channel names
- the real contract is in the envelope structure, not just one visible param

Action:

- document the transport kind explicitly
- freeze one known-good message or body sample
- separate envelope fields from business fields
- identify which fields are signed, sequenced, or server-assigned
- replay one stable message locally before attempting full stream collection

## Pattern L: Public page still hides a bootstrap envelope

Symptoms:

- the page or homepage is publicly visible
- one early endpoint returns a public key, config blob, nonce seed, or short string instead of business data
- the real business request posts a wrapper such as `{"param":"..."}` rather than the visible form fields
- compact JSON, a digest, a timestamp, and encryption or encoding are applied in a specific order
- list APIs work, but detail or submit APIs may still be permission-gated

Action:

- hit the real entry route once and capture the cookies that scope the public session
- freeze one bootstrap response and one successful business request
- prove the envelope build order exactly: raw payload, compact serialization, sign input, timestamp or nonce injection, final wrapper object, encryption or encoding, and outer transport field name
- verify long-message chunking rules when RSA or similar block ciphers wrap the payload
- make category, mode, and page parameters explicit instead of trusting UI defaults or empty values
- document list access and detail access separately so a public list is not mistaken for full public data access

## Pattern M: Stateful WebSocket session with encrypted business frames

Symptoms:

- the target stays mostly idle until login, pairing, or a short warm-up exchange completes
- one or more early messages carry a ref, public key, client ID, secret seed, or challenge blob
- later frames are binary or protobuf and stay unreadable until session keys or counters are derived
- the stream dies unless auth, ack, heartbeat, reconnect, or message-tag rules are preserved
- media metadata is visible, but media download or decryption needs separate derivation from message payloads

Action:

- freeze one full successful transcript: bootstrap, login or pairing, auth ack, heartbeat, and one business frame
- separate frame families before reading payload semantics: bootstrap, auth, keepalive, business, receipt, media
- recover the exact key schedule or session-secret update path before blaming protobuf or compression
- document message tags, counters, and replay boundaries explicitly
- prove one stable local session first, then add stream collection, reconnect, or media handling

## Pattern N: Challenge-generated state gates a shared envelope family

Symptoms:

- entry HTML and challenge JS must run first before business replay stabilizes
- a derived cookie, storage item, or preflight token binds session, page challenge, and environment model
- the business route depends on several coordinated fields at once, such as cookie, URL query, header token, and encoded body
- URL query, body, response, and sometimes cookie look like variants of one packet family rather than unrelated formats
- packet framing includes field prefixes, version markers, checksum bytes, custom alphabets, dynamic prefixes, or state-derived slices in addition to the inner cipher
- a preflight token request returns the same encoded family and seeds a later header or request field

Action:

- freeze one fresh two-stage trace: entry HTML, challenge JS, derived cookie or storage state, preflight token request and response, and one business request and response
- separate the problem into proofs: environment model, state transition, packet framing, key normalization, inner cipher, and business plaintext
- map the shared envelope family once across URL, body, response, and cookie, then record which fields are exact siblings and which are field-specific variants
- prove whether business plaintext alone is sufficient or whether current state bytes are also required to build later fields
- keep validation checkpoints explicit: cookie shape or length, token shape or length, checksum success, decoded prefix length, and expected JSON anchor or schema fields
- deliver the final collector as an explicit staged pipeline such as `entry -> local challenge/bootstrap -> token preflight -> business request -> local response decode`

## Pattern O: Pagination route pivots mid-sequence

Symptoms:

- early pages replay through one clean URL family, but later page numbers 404 or return the wrong content
- the visible pager looks uniform, but late-page links point to a different endpoint family such as `/ui`, Ajax, or a hidden template route
- guessing page numbers from the first-page URL works briefly and then collapses
- the real next page is stored in inline handlers, hidden templates, or pager metadata rather than a plain `href`

Action:

- treat pagination as part of the protocol contract, not filename arithmetic
- capture the cutoff page where the route family changes
- extract next-page targets from the live pager or raw source rather than extrapolating one URL pattern
- keep the collector logic route-aware so early and late pages can coexist without browser fallback

## Pattern P: Parsed attributes lie about replay-critical routes

Symptoms:

- inline handlers or metadata attributes carry query strings, `&`, entity-like text, or custom delimiters
- the parsed DOM value no longer matches the source bytes
- replay built from `onclick`, `tagname`, or similar DOM attributes fails, while the raw HTML snippet points to the correct route
- prettifying or reparsing the page changes the route or parameter names

Action:

- preserve the raw tag snippet before parsing or beautifying it
- compare raw source, DOM-decoded value, and wire behavior on the same page
- extract replay-critical route data from raw HTML when entity decoding or repair logic mutates it
- normalize entity handling explicitly instead of trusting parser defaults

## Pattern Q: Transport pre-gate blocks the clean baseline

Symptoms:

- standard HTTP clients die at H2 reset, TLS EOF, handshake timeout, or early disconnect before meaningful application data appears
- the same route behaves differently across UA families, ALPN, or HTTP versions
- mobile or app UA, impersonated TLS, or HTTP/1.1 passes while default desktop or stdlib traffic fails
- a sibling auth, identity, or business route bypasses a challenged landing route

Action:

- separate transport admission from signer, cookie, or payload logic
- map a narrow matrix of route, client stack, UA family, and HTTP version before loading giant bundles
- keep any passing transport profile scoped only to the blocked route family that needs it
- continue application-layer reversing only after one clean admitted baseline exists

## Pattern R: Challenge runtime already knows the answer

Symptoms:

- a bootstrap or challenge script exposes a getter after init, or self-issues XHR or fetch with the decisive wrapped payload
- later timer callbacks throw, but a usable artifact already exists before full DOM parity
- blocking `vm` execution deadlocks while DOM or script execution preserves timers or request hooks
- full VM understanding is expensive, but one outgoing payload, cookie, or header set is enough to continue

Action:

- classify the artifact path first: exposed getter, intercepted egress, or alternate-route bypass
- preserve scheduler semantics and intercept the nearest stable boundary
- stub only the minimal success response the runtime expects after local interception
- if runtime egress already exposes the authoritative outbound `Cookie` header, harvest that exact header before over-reversing individual cookie writers
- hand the harvested artifact back to Python for the real HTTP replay, and retry with fresh bootstrap when challenge bundles are version-randomized
