GIVEN:
INTTYPES: Subformula World ;
PREDICATES:
// Vocabulary for describing the formula.
Atom (Subformula)
Falsum (Subformula)
And (Subformula, Subformula, Subformula)
Or (Subformula, Subformula, Subformula)
Not (Subformula, Subformula)
Implication (Subformula,  Subformula,Subformula)
Box (Subformula, Subformula)
Diamond (Subformula, Subformula)
Biconditional (Subformula, Subformula, Subformula)
// Vocabulary for describing the models
TrueAt (Subformula, World)
TrueAtoms (Subformula, World)
FalseAtoms (Subformula, World)
Accessible (World, World)
SameAtom (Subformula, Subformula)
;
FIND :
TrueAt, TrueAtoms, FalseAtoms, Accessible ;
PHASE :
SATISFYING :
// The formula must be true.
TrueAt (1,1);
// The true atoms at a world are the sub-formulas which are atoms,
// and are true at that world.
! s:Subformula w:World : ( TrueAtoms (s,w) <=> ( TrueAt (s,w) & Atom (s) ) );
! s:Subformula w:World : ( FalseAtoms (s,w) <=> ( ~ TrueAt (s,w) & Atom (s) ) );
//! s:Subformula w:World : ( ~ ( TrueAtoms (s,w) & FalseAtoms (s,w) ) );
// Need to make sure that subformulas corresponding to the same atom share the same truth value at the same world
! s1:Subformula s3:Subformula w:World : ( ? s2:Subformula : ( ( Not (s2,s3) & SameAtom (s1, s3) )  => ( TrueAt (s1, w) <=> ~ TrueAt (s3, w) ) ) );
! s1:Subformula s2:Subformula s3:Subformula w:World : ( ( ~ Not (s2,s3) & SameAtom (s1, s3) )  => ( TrueAt (s1, w) <=> TrueAt (s3, w) ) );
// Semantics of Falsum - BROKEN. How can I tell Enfragmo that any subformula labelled 'false' should never be true at any world?!
! s:Subformula w:World : ( (Falsum (s) ) => ( ~ ( TrueAt (s,w) ) ) );
//! s:Subformula w:World : ( (Atom(s) & Falsum (s)) => ( ~ ( TrueAt (s,w) ) & FalseAtoms (s,w) ) );
// Semantics of And
! s1:Subformula s2:Subformula s3:Subformula :
( And (s1,s2,s3) => ( ! w:World : ( TrueAt (s1,w) <=> ( TrueAt (s2,w) & TrueAt (s3,w) ) ) ) );
// Semantics of Or
! s1:Subformula s2:Subformula s3:Subformula :
( Or (s1,s2,s3) => ( ! w:World : ( TrueAt (s1,w) <=> ( TrueAt (s2,w) | TrueAt (s3,w) ) ) ) );
// Semantics of Not
! s1:Subformula s2:Subformula :
( Not (s1,s2) => ( ! w:World : ( TrueAt (s1,w) <=> ~ TrueAt (s2,w) ) ) );
// Semantics of Implication
! s1:Subformula s2:Subformula s3:Subformula :
( Implication (s1,s2,s3) => ( ! w:World : ( TrueAt (s1,w) <=> ( TrueAt (s2,w) => TrueAt (s3,w) ) ) ) );
// Semantics of Biconditional
! s1:Subformula s2:Subformula s3:Subformula :
( Biconditional (s1,s2,s3) => ( ! w:World : ( TrueAt (s1,w) <=> ( TrueAt (s2,w) <=> TrueAt (s3,w) ) ) ) );
// Semantics of Box
! s1:Subformula s2:Subformula :
( Box (s1,s2) =>
( ! w:World : TrueAt (s1,w) <=> ! w2:World : ( Accessible (w,w2) => TrueAt (s2,w2) ) ) );
// Semantics of Diamond
! s1:Subformula s2:Subformula :
( Diamond (s1,s2) =>
( ! w:World : TrueAt (s1,w) <=> ? w2:World : ( Accessible (w,w2) & TrueAt (s2,w2) ) ) );
// Axiom schema K: ([]phi ^ [](phi -> psi)) -> []psi
// Note that K hold in all Kripke structures without imposing any conditions on accessibility relations.
PRINT :
TrueAt, Accessible;
// Transitive
! w1: World w2: World w3: World: ( Accessible (w1,w2) & Accessible (w2,w3) => Accessible (w1,w3) );
// Euclidean
! w1: World w2: World w3: World: ( Accessible (w1,w2) & Accessible (w1,w3) => Accessible (w2,w3) );
// Symmetric
! w1:World w2:World : ( Accessible (w1, w2) => Accessible (w2,w1) );
// Serial
! w1: World : ? w2: World : ( Accessible (w1,w2) );
// Reflexive
! w1: World : ( Accessible (w1,w1) );
// Anti-symmetric
! w1:World : ? w2:World : ( Accessible (w1, w2) => ~Accessible (w2,w1) );
