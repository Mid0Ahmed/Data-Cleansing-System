% Define parent relationships
parent(john, mary).
parent(john, frank).
parent(mary, susan).
parent(mary, george).
parent(frank, anna).
parent(frank, james).

% Define gender relationships
male(john).
male(frank).
male(george).
male(james).
female(mary).
female(susan).
female(anna).

% Define grandparent relationship
grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).

% Define sibling relationship
sibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y),
    X \= Y.

% Define cousin relationship
cousin(X, Y) :-
    parent(A, X),
    parent(B, Y),
    sibling(A, B).

% Queries
% ?- grandparent(john, X).
% ?- sibling(mary, X).
% ?- cousin(susan, X).

% Define a rule to find all ancestors of a person
ancestor(X, Y) :-
    parent(X, Y).
ancestor(X, Y) :-
    parent(X, Z),
    ancestor(Z, Y).

% Define a rule to find all descendants of a person
descendant(X, Y) :-
    parent(Y, X).
descendant(X, Y) :-
    parent(Z, X),
    descendant(Z, Y).

% Queries
% ?- ancestor(john, X).
% ?- descendant(X, john).

% Define a rule to check if someone is an uncle or aunt
uncle_or_aunt(X, Y) :-
    sibling(X, Z),
    parent(Z, Y).

% Queries
% ?- uncle_or_aunt(frank, X).
% ?- uncle_or_aunt(mary, X).
