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

This is one of the 'simulate a path' problems. Rather than handling clunky tuples or building a vector class, we will use complex numbers to track both position and heading. Complex numbers are actually 2-dimensional vectors, with the added benefit that multiplying the heading by `1j` effectively makes a left turn (and by `-1j` makes a right turn). It's easy to read the data, using row and column indices to represent the position of obstacles and the robot.

We will use the negative of the row, and then add the total number of rows so that the imaginary parts grow upwards in the map. Otherwise, the turning does not behave as expected.

Finally, we build a function to chech whether a position is within bounds, performing an enclosure of the values for the number of rows and columns; this is easier to pass aorund, and avoids the need to rewrite the checks in different places.

### Part 1

To keep track of the positions in the path we use a set. The code has been updated for Part 2, so it doesn't show it finally; the `defaultdict(set)` works as well, as we keep the non-duplicated positions as keys (the values keep track of the headings while in the position, which is relevant for Part 2).

Most of the `trace_path` function was added after the fact. At each step we just need to see what would happen taking one step in the direction of heading; if there's an obstacle, turn, otherwise actually take the step, then repeat until the robot is out of bounds. It would look like this:

```python3
def trace_path(obstacles, in_bounds, start, heading=1j):
    path = defaultdict(set)
    pos = start

    while True:
        new_pos = pos + heading  # tentative new step
        if not in_bounds(new_pos):  # next step takes us out of bounds, it's the end of the path
            break
        if new_pos in obstacles:  # there is an obstacle ahead
            heading *= -1j  # turn right
        else:  # next step is feasible
            pos = new_pos  # take the step
        path[pos].add(heading)  # in either case, update the path with the new pos and heading

    return path
```

To get the answer we just look at the length of the path.

### Part 2

Next, we need to find where to set up a new obstacle so that the robot is thrown into a loop. The brute-force approach is to check every possible position and trace the path to see if it geenrates the loop. A little more smartly, we can check only positions along the original path, as other positions won't change the route. That's still a large number of checks, each with a potentially long path until the loop (or lack thereof) is discovered.

We can take one more step checking recursively, dynamic programming-style, as we go along the original path. Everytime we would take a step ahead we ask a hypothetical *what if there were an obstacle just ahead and I had to turn?*. This hypothetical uses exactly the same path-following logic, so we can solve it with a recursive call; to provide both answers that we need (the path for the outer call, whether there is a loop for the inner call), we now return two values. Likewise, we need additional input arguments: the path so far (which we copy, we don't want to overwrite that), the new position for the obstacle if it's the what-if scenario (`new_loop`), and how many new obstacles can be added, which will be 1 or 0.

The code is actually very similar to the simpler version of Part 1, with some reordering, and adding the recursive call for the hypothetical.

There is a subtle bug that crept in (it's already fixed) and took some time to find: because we reuse the `pos` variable first to copy the path prefix and then to continue the path, the initial position is undefined if not reset to `start` explicitly. This would not happen with a normal dictionary as (in modern Python) they are ordered; but apparently `defaultdict` is not.



## Day 7

Today's task is to find what operations, if any, can be inserted between numbers to reach a predefined result.

### Part 1

We can add and multiply. Operations are applied from left to right, so no need to write out the equations and figure out precedence. It's like a reduce or fold operation, only we need to decide each operation. Wich means that a recursive search should be straightforward:

1.  Base case: if there is only one number, that's the only possible result, so we just return whether it matches the target
2.  Loop through the operators: take out the two first numbers, and put the result of applying the operation to them in their place; can we get to the target in this reduced problem?
3.  As soon as one of the operators returns that it works, we can say that it's possible; if they all fail, it is not.

There is one more little improvement we can make: all operators result in larger values than any of their arguments, so if the first number grows beyond the target we can prune that brach of the search immediately and save computation. This comes between steps 1. and 2.

### Part 2

A third option appears now: a concatenation operator. This still behaves like addition and multiplication, in the sense that it is always increasing, so we can apply exactly the same logic, only with one more operator in the loop of operators, with a newly defined `concat` function as the third operator.



## Day 8

Yet another case of elements positioned in a grid. This time we will use (row, column) tuples, as we will be accessing the components frequently, so the complex number option is less useful this time. Otherwise, it's the same sparse representation, using a dictionary keyed by the frequency, and with the position as the value.

Don't forget to also return the number of rows and columns to be able to check bounds later.

### Part 1

Finding the antinodes is easy: it's basically calculating the vector from one antenna to another: `d = a2 - a1`, and then the antinodes are at `a1 - d` and `a2 + d`. In the code:

*   We do this separately for rows and columns, so `d` turns into its two components `rowdiff` and `coldiff`.
*   For each frequency, we select the first antenna by looping over the antennas except the last one, and the second by iterating over those after the current one in the outer loop. This covers all pairs, as we are doing both directions of the antinodes.
*   For each antinode that we determine, we add it to the set of antinodes, which takes care of potential overlaps.

The length of the antinodes set is the number of unique antinode locations, and the answer that we look for.

### Part 2

This is the same as Part 1, just repeating the addition (or substraction) of `d` until getting out of bounds.

For clarity, we retain the same structure as before, but take the calculation of the antinodes corresponding to a pair of antennas out into a `line` function. This function just calculates the step, equivalent to `d` before, now called `slope`, and applies it iteratively in both directions until the grid runs out. It returns the set of antinodes, which is added (union-ed?) to the global set of antinodes.



## Day 9

It's clear that representing the whole memory explicitly is not the way to go so we will define data structures for files and gaps:

*   Each file is a dictionary with fields for `id`, `pos` (position), and `size`. We will keep them ordered in a list, to begin with.
*   Gaps are similar to files, but there is no `id` field. We will use a deque to keep the gaps, as we will need to process them left-to-right (i.e. FIFO).

Reading the data and translating it into these formats is not complex, it just requires some care to alternate between files and gaps, keeping track of the file ids, and skipping 0-sized gaps.

The calculation of the file checksums is also straightforward, given the data structure:

```python3
sum(pos * file['id'] for pos in range(file['pos'], file['pos'] + file['size']))
```

### Part 1

The first compression strategy moves files from the back of the memory, inserting them into the gaps from left to right, and splitting as necessary to leave no gaps. So we just simulate this:

1. We take a file from the back, popping it from the list
2. We take the first gap from the gap queue
3. We insert the whole file or as much of it as fits in the gap
4. We retain the file or gap that is not exhausted, and take the next one of the other
5. Repeat until we reach a gap that is beyond the file that we are moving: everything after the current file must already be moved, so only free space remains there.

Keeping the list of files updated with the positions of the files that are moved is not trivial, and our data structure does not provide affordances for tracking fragments. However, neither of this is a problem.

First, we do not need to keep the list ordered, as long as we correctly update the `pos` field of the files; the checksum will use that value, so the position in the list is irrelevant, except for extracting the files in order from the back. This means that we can just use an auxiliary list, and just join them together at the end.

Second, we do not need to do anything with the files as a whole. If both the `id` and `pos` are correct, it does not matter whther its a whole file, a fragment, or which particular fragment. The checksum will still be correct.

### Part 2

The second strategy tries to avoid fragmentation by moving whole files again starting from the back to the first gap that is large enough. This means that the gaps need to be updated as the files are moved, because the next file will start again from the beginning.

The new procedure works similarly to the first one:

1. We process files from the back towards the front
2. For each file, we check the gaps in order until we reach a gap position beyond the file position
3. For each gap, we check if the file size fits in the gap. If so, we update the position of the file, and the position and size of the gap (the file *eats* the beginning of the gap); this has the side effect of setting the position of the file ahead of the gap, so in the next iteration of the loop it will trigger the break and move on to process the next file.

There are a couple of possible optimizations here, but they were not needed, so it made no sense to add the additional complexity:

*   If a file fits into a gap exactly, the gap becomes size 0; this works out, but ideally this 0-sized gap should be removed.
*   There is probably a smarter stop condition that does not necessarily run through all files, but the meagre potential gains do not justify thinking it through.

As before, the position of the files in the file list is irrelevant, so we do not move them around, just update the `pos` field as needed. This also allows the loop to be a simple `for`.



## Day 10

The relevant features in today's puzzle are the trails, not the heightmap itself. We will still build the heightmap as we read the data, but just as a buffer. We will build three artifacts:

1. A heightmap, as a dictionary of (row, column) and height pairs, as we go through the input file.
2. If the height is 0, we add the (row, column) location to the set of trailheads
3. A graph of trails. This is a directed graph, as we only want ascending steps. To avoid multiple passes, we only consider for each position the positions to the left and above and check both directions (from the current node to the neighbour, or from the neighbour to the current node). It's easy to see that this looks at all possible pairs (and a few impossible ones above the first row and to the left of the first column). Also, as we are checking the height in the heightmap, just seeing if it's there works as well as checking bounds, and can be done on the go, as we build them.

### Part 1

We need to follow all the possible trails and see how many positions of height 9 can be reached. The easy way is to enumarate all reachable nodes from each trailhead, and see if their height is 9 (this is what `score` does).

The `visit` function is like finding the connected components of the graph, but we are only interested in the component of a specific trailhead at a time. We start with just the trailhead in a queue, and an empty set of visited nodes. Until we empty the queue, we take one node from it, yield it as a reachable node, mark it visited, and add its unvisited neighbours to the queue.

### Part 2

The `rating` is more complex than the `score`. We need to check all unique paths, but those paths may not just partially overlap, but they may brach apart and later reunite (if they never reunited, there would be a single way to get to each peak, and `rating` would be the same as `score`).

Luckily, this is easy to solve through recursion. And the recursion corresponds to each step of a trail, so there is no danger of the recursion depth going beyond 10.

When we start at the trailhead, the rating is the sum of the ratings of each possible next step; each of those steps branches into one unique path (but it has to be followed to see if it reaches a peak). We can calculate the rating of each of the next steps in the same way, and with each recursion level we will be one level higher. There are two base cases: if at some point there are no possible steps before reaching the peak, then the rating is 0; if we reach a peak the rating is 1 (we reach it through one specific path).

Since we are only interested in the rating, this is quite neat. If we needed the paths, they can be built through the recursion, adding a few lines of code and some *noise* to the solution.



## Day 11

Not a lot to discuss on the data structures for this one. We will just process the numbers one by one, since we can easily observe that whta happens to each is independent from the others; which means that we don't even need to put them together into a list or something like that.

### Part 1

This part can be directly simulated, the branching does not get out of hand either in terms of space or number of operations. This won't be the case for the second part, but at this steage we still don't know which way it will go (it could well just complicate the blinking rules).

The simulation version is very similar to the final version: we just write the rules for one step and apply it recursively:

```python3
def blink(stone, times):
    if times == 0:
        return (stone,)

    if stone == 0:
        return blink(1, times - 1)

    stone_str = str(stone)
    stone_len = len(stone_str)
    if stone_len % 2 == 0:
        midpoint = stone_len // 2
        stone1, stone2 = (int(stone_str[:midpoint]), int(stone_str[midpoint:]))
        return (**blink(stone1, times - 1), **blink(stone2, times - 1))
    return blink(stone * 2024, times - 1)
```
For the base case, when we have zero applications left (`times == 0`), just return the stone as a 1-tuple; return values need to be sequences because the stones can *multiply* in one step, so we will need to collect them.

If we have more transformations to make, we do one step, and recurse with one less time to apply. We go in order through the rules:

1.  If the stone is 0, change it to 1 and recurse.
2.  If it has an even number of digits, we create two separate stones, one from each half, recurse for each of them, and group the results.
3.  If nothing else applies, multiply by 2024 and recurse.

### Part 2

With the deeper recursion we run into two problems: running time, and the size of the line of stones. The size part can be dealt with by just working with the length of the line, rather than the individual values. For the running time, we will use memoization: there will be repetition of values so we can just reuse previously calculated values.

We rename our function to `blink_len` to reflect the new focus, and adjust the return values: If `times` is zero (the base case), just return one, the stone remains as is. For the other cases, the only non-trivial part is that the grouping of a splitting stone now becomes adding the lengths of each new stone, calculated through the recursion.

For the memoization we just wrap the funciton with a decorator that caches the result of every call to the function, and uses the cache if available.



## Day 12

Another 2-dimensional grid, another graph-based solution. In this case we are not following paths, but working with regions. We will connect nighbours in the same region: as we itereate through the rows and columns of the input, we create a node for each `(row, col)` pair, and edges between it and each of its neighbours that belong to the same region. We will use the same trick we used before of only looking at the neighbours that were visited before in the iteration, to avoid a double pass.

As a helper to building the graph, we will have a map that indicates the region (the associated letter) for each node. We will return that, too, in case it's useful (spoiler alert: it's not).

With the graph, we can easily separate the regions as the connected components in the graph.

### Part 1

The area of a region is straightforward to calculate with our representation: count the number of nodes.

The perimeter is also easy: Each node contributes one unit for each neighbour that is not in the same region, or in other words, 4 minus the number of neighbours. Sum over the nodes.

### Part 2

The new parimeter calculation gets tricky. We will need to actually trace the perimeter, counting how many time we change side. We also need to account for the possible interior gaps, which are slightly different. We will treat them separately, although it should be possible to abstract the difference into a function, parametrizing to what side of the heading the *outside* is. We will discuss the outer bound in detail, and then gloss over the inner bounds, which follow the same rationale.

We first filter out the edge nodes: those with fewer than 4 neighbours; we create a set of them to track when we are done tracing all the boundaries; we use (node, normal) pairs because some nodes, those in corners, will have more than one side to count, so we record also the *missing* neighbours; i.e. the normal points to the outside of the region. We also start a `sides` counter.

We move to the leftmost node in the topmost edge. This is necessarily the outer edge, and easy to calculate: it's the minimum of the edge nodes (considering that tuple inequality is lexicographic and that our nodes are defined as `(row, col)` tuples). We start moving rightwards (we'll go clockwise), with our normal vector pointing up (outside). The loop body counts one side, and runs along it until the next turn. We repeat this until we get back to the start node, but are heading up: that's when we have closed the boundary.

We can keep moving along an edge (and removing the node, heading pairs from the remaining set) as long as the next step in that direction is still within the region (that's a right turn), and the outside neighbour of the next step is not within the region (that's a left turn).

If we reached a right turn, it's done in place: just adjust the heading and normal. If it's a left turn, we need to move one step ahead and one to the left (the direction of the normal), as well as changing the heading and normal. Note that this is different form [a jump to the left and then a step to the right](https://www.youtube.com/watch?v=YC1E8yVJIS4).

For the inner gaps, the normal is to the right of the heading (we are still going clockwise), and the checks for right and left turns are exchanged (now turning right requires the extra steps, and left turns are done in-place). Also, when we close one region we will not end in the same position as we started (it would be a right turn).

We keep counting the inner gaps by taking the minimum remaining node, which is the top-left node of one of the remaining gaps. When we run out of remaining nodes, we are done.


## Day 13

This is a mathematical puzzle; once we notice that everything becomes extremely simple. Especially since none of the machines have collinear buttons (I checked), so asking for the minimum cost is a red herring: there is only one possible combination of the two buttons that will retrieve the prize. Let's define some nomenclature for a machine:

*   Button `A` is pushed $a$ times, and each time it moves the claw machine by $(x_a, y_a)$.
*   Button `A` is pushed $b$ times, and each time it moves the claw machine by $(x_b, y_b)$.
*   The prize is located at $(x_p, y_p)$.

We then have a double condition to meet to reach the prize:

```math
\begin{cases}
  a x_a + b x_b &= x_p\\
  a y_a + b y_b &= y_p.
\end{cases}
```

If we multiply the first equation by $\frac{y_a}{x_a}$ and subtract it from the second, we get:

```math
\begin{align}
  b (y_b - \frac{x_b}{x_a}y_a) &= y_p - \frac{x_p}{x_a} y_a \\
  b (x_a y_b - x_a y_b) &= x_a y_p - x_p y_a\\
  b &= \frac{x_a y_p - x_p y_a}{x_a y_b - x_a y_b}.
\end{align}
```

We can then calculate $a$ directly from the first equation, using the value of $b$:

```math
a = \frac{x_p - b x_b}{x_a}.
```

### Part 1

We will start with a class for a Machine, that takes the buttons and prize position. This could be a function, but it helps with passing around all the data easily. Building the machines is easy, just a little parsing of the specification.

In the `win` method, we just use the equations we derived above to calculate `a` and `b`, or rather their integer part; we're not interested in fractional pushes. We then check if using this numbers of pushes will actually get the prize, and return the cost if so. Otherwise we return `None`, meaning that it's not possible to win in that machine.

### Part 2

It seems that we were expected to solve the first part through search and now try to find out the mathematical solution. Since we started with the math, we just need to add the `offset` option in the initialization of the `Machine` class, and we're done.



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


