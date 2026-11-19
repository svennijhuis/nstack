# Refactor

Structure changes, behaviour does not. **The pin is the contract.** The ticket is done when the code is deeper and easier to read, and nothing a caller sees changed.

1. Read.
2. Pin the behaviour through the interface the callers use: a characterization test or an old-against-new comparison. A typecheck or a lint is not a pin. Run it before you change anything.
3. Name the shape the code is missing, and the target shape. Say the call. Code where its meaning belongs, the deletion test, no seam the spec did not name. Keep boring code that is already clear.
4. Subtract before you add: delete dead code, collapse wrappers with one caller.
5. Move in small steps, each with the pin green. Move every caller and delete the old shape in the same change. Commit as `refactor:`.
6. Prove nothing changed on the real thing: run the old and the new code on the same inputs and compare.
7. Is the code easier to read than before? No: revert, and say why.
8. Review with fresh eyes.
9. Fix.
10. Finish.

**Reply:** the shape before and after, the pin and whether it passed unchanged, the old-against-new proof, why it reads easier. A pinning test you had to change pinned the inside, not the behaviour: say which.
