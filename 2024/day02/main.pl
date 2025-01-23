:- use_module(library(pio)).

lines([L|Ls1]) --> line(L), "\n", lines(Ls1).
lines([L]) --> line(L).
lines([]) --> [].

line(L) --> [C], { char_code(Char, C) }, { C \= 10 }, line(L1), { L = [Char|L1] }.
line([]) --> [].

parse_line([],[0]).
parse_line(List, ParsedList) :- 
    append(Init, [' '], List),
    parse_line(Init, ParsedList1),
    append(ParsedList1, [0], ParsedList),
    !.
parse_line(List, ParsedList) :- 
    append(Init, [Last], List),
    parse_line(Init, Parsed1),
    append(InitP, [LastP], Parsed1),
    char_code(Last, Code),
    NewLastP is LastP*10+Code-48,
    append(InitP,[NewLastP],ParsedList), !.

parse([],[]).
parse([H|T], [Parsed|ParsedT]) :- parse(T,ParsedT), parse_line(H,Parsed).

diff_within_range(X, Y) :-
    AbsDiff is abs(X - Y),  
    AbsDiff > 0,            
    AbsDiff < 4. 

check_report_helper([_],_).
check_report_helper([H1,H2|T], IsIncreasing) :- 
    (H1 < H2 -> IsIncreasing = true ; IsIncreasing = false), 
    diff_within_range(H1,H2), 
    check_report_helper([H2|T], IsIncreasing).


check_report([H1,H2|T]) :- (H1 < H2 -> Order = true ; Order = false), check_report_helper([H1,H2|T], Order).

check_reports([],0).
check_reports([H|T],X):-
    check_report(H),
    check_reports(T,X1),
    X is X1+1,
    !.
check_reports([_|T],X) :- check_reports(T,X).


check_report_with_mistake_helper([_,_],_).
check_report_with_mistake_helper([H1,H2|T], IsIncreasing) :-
     (H1 < H2 -> IsIncreasing = true ; IsIncreasing = false), 
    diff_within_range(H1,H2), 
    check_report_with_mistake_helper([H2|T], IsIncreasing),
    !.
check_report_with_mistake_helper([H1,_|T], IsIncreasing) :-
    check_report_helper([H1|T], IsIncreasing), !.
check_report_with_mistake_helper([H1,_,H3|T], IsIncreasing) :-
    check_report_helper([H1,H3|T], IsIncreasing), !.

check_report_with_mistake([H1,H2|T]) :- (H1 < H2 -> Order = true ; Order = false), check_report_with_mistake_helper([H1,H2|T], Order), !.
check_report_with_mistake([_,H2,H3|T]) :- (H2 < H3 -> Order = true ; Order = false), check_report_helper([H2,H3|T], Order), !.
check_report_with_mistake([H1,_,H3|T]) :- (H1 < H3 -> Order = true ; Order = false), check_report_helper([H1,H3|T], Order), !.


check_reports_with_mistake([],0).
check_reports_with_mistake([H|T],X):-
    check_report_with_mistake(H),
    writeln(H),
    check_reports_with_mistake(T,X1),
    X is X1+1,
    !.
check_reports_with_mistake([_|T],X) :- check_reports_with_mistake(T,X).


main :- phrase_from_file(lines(Lines), 'test.txt'), 
    parse(Lines, Parsed),
    writeln(Parsed),
    check_reports(Parsed, NumberOfOk),
    writeln(NumberOfOk),
    check_reports_with_mistake(Parsed, NumberOfOk2),
    writeln(NumberOfOk2).
