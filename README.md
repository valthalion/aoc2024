# Advent of Code 2024

This repo contains the code solving the puzzles in the [Advent of Code 2024](https://adventofcode.com/2024/). The code is quite terse and unexplained, but details on the reasoning behind the solutions are provided below (usually updated after the fact).

Direct links to each day:

*   [Day 1](#Day-1)
*   [Day 2](#Day-2)
*   [Day 3](#Day-3)
*   [Day 4](#Day-4)
*   [Day 5](#Day-5)
*   [Day 6](#Day-6)
*   [Day 7](#Day-7)
*   [Day 8](#Day-8)
*   [Day 9](#Day-9)
*   [Day 10](#Day-10)
*   [Day 11](#Day-11)
*   [Day 12](#Day-12)
*   [Day 13](#Day-13)
*   [Day 14](#Day-14)
*   [Day 15](#Day-15)
*   [Day 16](#Day-16)
*   [Day 17](#Day-17)
*   [Day 18](#Day-18)
*   [Day 19](#Day-19)
*   [Day 20](#Day-20)
*   [Day 21](#Day-21)
*   [Day 22](#Day-22)
*   [Day 23](#Day-23)
*   [Day 24](#Day-24)
*   [Day 25](#Day-25)



## Day 1

This is a proper warm-up exercise, conceptually very simple.

### Part 1

The task is to compare the numbers in each list, in increasing order in both: straightforward sort each list and add the (absolute) differences.

### Part 2

This part is slightly trickier. We need to calculate a similarity score that depends on how many times each number in the feirst list appears in the second list. To avoid going through the second list again and again, we just pre-count (in linear time) the occurrencies and store them in a dictionary so we can retrieve them easily (and in constant time).



## Day 2

We will be processing the sequences of *levels*, so a list of lists (with the numbers cast to `int`s) is the right data structure: the order is relevant. Other than that, it's only a matter of implementing the safety rules corresponding to each part.

### Part 1

As usual, this is the easy one. We can determine whether a given report is ascending or descending by checking the difference between the first and second element; it may be a fluke, but since any deviation means failure, it works out.

We can use the comparison operators directly to avoid evaluating the difference, but we need to actually calculate it for the condition that it must be (in absolute terms) between one and three; so we don't do it for the performance, but rather for the clarity.

### Part 2

Introducing the flexibility for a bad level makes things more complex. We will look at the differences directly (`diffs`), and we need to check the direction more intelligently: we can take the three first differences and take the most common, but it's even easier to just use the global difference from start to end to mark the direction.

It is not enough, or even necessary, that all but at most one of the differences be valid. Since we can remove one value, that takes away two consecutive differences and oncludes instead their sum (which equals the difference between the elements before and after the one removed).

So we iterate over the differences, and if we find an invalid one we try dropping one of the elements that cause it (on either side). If this is possible, we continue, marking the report as dampened, because this can be done only once. If it is not possible, or if we later find another infeasible difference, the report is not valid.

This prevents the explosion of the naive approach: for each invalid report, try if it becomes valid by removing each of the elements. Updating the validity check to return the index at which it happens, so just two trials are needed (either of the elements involved in the offending difference), means more complex logic, impacting readability.



## Day 3

At first it seems that building an interpreter may be needed, but only regular expressions are required this time. The task is to find a specific type of instruction.

### Part 1

Quite straightforward, find instances of `mul(x,y)`, where `x` and `y` are integers, and just that (any other character invalidates it). The regular expression is quite simple, though it appears a little more complicated because groups are defined to easily access `x` and `y`.

### Part 2

Now there is state in the processor, updated byt the `do()` and `don't()` commands. It's easy to notice that this is sequential, so we just update the regular expression to also capture these commands, and keep track of whether the operations are enabled, skipping the occurrences that appear while disabled.


## Day 4

Now we're cooking. Find words mixed in a table. We will save the table in dictionary format indexed by (row, col) pairs. Why not a list of lists? the double brackets are more unconfortable to type, and since we will be operating on the indices, passing them around together is easier.

### Part 1

We are looking for `XMAS` in any direction (including diagonals and reversed). The easiest way: just stop at the `X`s, and check each of the 8 possible directions to see if it is the right string. We could do it step by step and abort at the first mismatch, but with just four characters that's overkill.

We will build a helper function to generate the sequences of indices for each *word* at a given position (i.e. at each `X`). Importantly, we need to keep track of index bounds to avoid errors when looking up the words. With that, just check and count.

### Part 2

Now we're looking for an X-like pattern with two `MAS` lines. This results in a number of possible combinations, depending on the directions.

Instead of trying to enumerate all of them, we can notice that this means that we are looking for `A`s, which have two `M`s and two `S`s as their four diagonal neighbours. Also, we need to avoid a pattern that results from crossing `MAM` and `SAS`; we seem to be in no better position than before, except that giving it some thought reveals that just checking that one of the lines has different letters on each end is enough.

We build a helper as before, to get the four relevant neighbours; this time we do not care about bounds, instead default to an empty string in case of a key miss when looking up in the table.

We ignore the order, by sorting so we know which string to expect, and if we have the right four characters, we check the ends of one of the lines. Check and count as before.



## Day 5

The data representation in this case is a dictionary, which represents the precedence rules of the pages. For each page (key), we get a set of the pages that have to go before it. This makes it easy to check compliance as we advance along a sequence of pages.

Each manual is just a list of the page numbers, in order (of publication, not sorted).

### Part 1

At this stage, we just check for the right order.

First, we filter the global rules to keep only the ones that are relevant, i.e. those that refer to the pages involved in the particular manual.

With that, we go page by page in order, keeping track of them in a helper set (`seen`) to make efficient comparisons with the rules. If there are predecessors indicated in the rules for the page, we check that they are a subset of the seen pages. Any failure means the manual is ivalid.

### Part 2

Now we get to reorder the invalid manuals. Evidently, trying every permutation and checking is not a great idea (factorial complexity is even worse than exponential). Instead we will rebuild each manual in linear time by applying the rules.

We start by filtering the rules as before. Then we take the pages ignoring their current order, are set up a stack (even if we call it queue) to build the new order. We also keep track of the pages that are already added.

We take one arbitrary page and push it into the stack. Then we recursively apply the following procedure, until we exhaust the stack:

*   Peek at the top element in the stack
*   If there are no predecessors indicated by the rules, or they are satisfied by the pages that are already added, pop the page and add it.
*   Otherwise, push the unsatisfied dependencies to the stack

We add all unsatisfied dependencies, which may already be in the stack somewhere; this means that when we peek into the stack, if we see a page that has already been added we just discard it.

This procedure ensures that the pages are added in order consistent with the rules, as a page is never added unless all its dependencies have been added before.

Depending on the structure of the rules and the first page selected there may remain additional pages when the stack empties. In that case, just take any of the remaining pages and put it in the stack. Repeat until all pages are gone.


## Day 6

### Part 1



### Part 2




## Day 7

### Part 1



### Part 2




## Day 8

### Part 1



### Part 2




## Day 9

### Part 1



### Part 2




## Day 10

### Part 1



### Part 2




## Day 11

### Part 1



### Part 2




## Day 12

### Part 1



### Part 2




## Day 13

### Part 1



### Part 2




## Day 14

### Part 1



### Part 2




## Day 15

### Part 1



### Part 2




## Day 16

### Part 1



### Part 2




## Day 17

### Part 1



### Part 2




## Day 18

### Part 1



### Part 2




## Day 19

### Part 1



### Part 2




## Day 20

### Part 1



### Part 2




## Day 21

### Part 1



### Part 2




## Day 22

### Part 1



### Part 2




## Day 23

### Part 1



### Part 2




## Day 24

### Part 1



### Part 2




## Day 25

### Part 1



### Part 2


