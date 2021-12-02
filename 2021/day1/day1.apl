⍝ x ← ⎕
⍝ Idk how to read input so this line is copypasta
x ← a←⍎¨⊃⎕NGET 'input.dat' 1
⍝ Dunno if the input thing even works...
inc ← {+/(¯1↓⍵)<(1↓⍵)}
win ← {(¯2↓⍵)+(¯1↓1↓⍵)+(2↓⍵)}
inc x
inc win x
