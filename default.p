% Clean data from a list by removing duplicates and sorting

% Remove duplicates from a list
remove_duplicates([], []).
remove_duplicates([H|T], Result) :-
    member(H, T), % If H is in the tail
    remove_duplicates(T, Result). % Skip H
remove_duplicates([H|T], [H|Result]) :-
    \+ member(H, T), % If H is not in the tail
    remove_duplicates(T, Result).

% Merge two sorted lists into one sorted list
merge([], L, L).
merge(L, [], L).
merge([H1|T1], [H2|T2], [H1|Merged]) :-
    H1 =< H2,
    merge(T1, [H2|T2], Merged).
merge([H1|T1], [H2|T2], [H2|Merged]) :-
    H1 > H2,
    merge([H1|T1], T2, Merged).

% Split a list into two halves
split_list([], [], []).
split_list([H], [H], []).
split_list([H1,H2|T], [H1|L1], [H2|L2]) :-
    split_list(T, L1, L2).

% Merge sort algorithm
merge_sort([], []).
merge_sort([H], [H]).
merge_sort(List, Sorted) :-
    List = [_,_|_], % Ensure the list has at least two elements
    split_list(List, L1, L2),
    merge_sort(L1, Sorted1),
    merge_sort(L2, Sorted2),
    merge(Sorted1, Sorted2, Sorted).

% Clean data by removing duplicates and sorting
clean_data(Unclean, Clean) :-
    remove_duplicates(Unclean, NoDuplicates),
    merge_sort(NoDuplicates, Clean).

% Test queries
% ?- clean_data([3, 1, 2, 2, 3, 4, 1], Clean).
% Clean = [1, 2, 3, 4].
% ?- clean_data([7, 3, 9, 3, 5, 9, 1], Clean).
% Clean = [1, 3, 5, 7, 9].
