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

It's easy to see that robots are (individually) fully predictable at any timestep $t$, from the initial position $p(0)$ and the speed $v$:

```math
p(t) = p(0) + vt.
```

This assumes a vector approach, and that we have a slightly redefined multiplication that applies modulo the width/height for the x/y components, respectively, to account for the wrapping (teleportation).

We will use two simple classes to manage all of this, and make the rest of the code more intelligible: `Vector` and `Robot`. Building the `Robot`s from the input requires some parsing, but is straightforward.

### Part 1

Since our definition of the `Robot`s already allows to foresee their position at the target time direclty, only calculating the quadrant is left to do. We will just add 1 if the position is to the right of the middle and 2 if it's below the middle; this is equivalent to using a 2-bit bitmask, and will return a value between 0 and 3. If the robot happens to be on one of the middle lines, we just return `None`, as it belongs into no quadrant.

After that, it's only a matter of counting and multiplying the counts.

### Part 2

We will go for the visual approach in this case. So our first step is to be able to `show` the situation at a given time step. We can start by showing a series of situations, e.g. 100 at a time (aesier to do by redirecting output to a file and using a text editor to scroll), and taking a quick look; mostly the patterns will be basically noise, but some level of structure emerges occasionally.

After only a few of these we see a pattern: Every 101 steps, there is some accumulation of the robots towards the vertical centerline, and some horizontal stretches that seem to suggest lines. From here on, we can advance much faster, just generating those times with steps of 101. Only a few more batches until we see a clear depiction of a christmass tree. We take note of the timestep and that's our answer.



## Day 15

We will keep track of the different types of objects in different ways, always sparse. First, we will use our classical complex representation of the coordinates; this time, as there are no rotations involved, we don't care that increasing the imaginary part goes down. The representation of the different elements:

*   The robot is just its position, nothing else is really needed.
*   Walls are a set of positions so we can easily check for collisions.
*   The boxes will need to model some behaviour, so we will build a class to represent them. We will store them in a dictionary with the box's position as the key.

When moving on to Part 2, and widening the boxes, these definitions need some tweaking: each horizontal step actually becomes two. This does not affect to the definition of the robot, since it is located on the first of the two spaces; and we can build the boxes in the same way as before, assuming that their location is given by their leftmost position. For the walls we just generate both positions to include in the set.

Finally, calculating the *gps* coordinates of each box is trivial.

When reading the description for Part 1, keep in mind that the initial code was much simpler, and it was generalized to wider boxes after the fact.

### Part 1

Mostly standard fare: follow the sequence of moves, check if the new position is feasible; if so, take that step (and move boxes if appropriate), otherwise ignore it.

Checking feasibility has three parts:

1.  If the new step is a wall, it's not feasible.
2.  If the new step is a box, then it's feasible if the box can move in that direction.
3.  If it's neither, then it's feasible.

The second option is the only one with any meat to it. The box can move following exactly the same rules as the robot, so it reduces to a recursive call in case the next move of the box goes into another box; sooner or later the next move of the box will either be a wall (no move possible), or a gap (and so move); in either case, the result propagates back through the chain of calls, up to the robot, and everyone moves or not according to this.

At this stage, the boxes move directly when checking if they can move (if the result is positive), and the move has to be integrated into the dictionary keys as well so that the boxes can be found in the right place (we integrate this in the class itself to avoid potential issues with forgetting to update fro mthe outside). Moving just before returning from the recursive call ensures that every box has a clear spot for its move and that no box is written out of the dictionary (this is a nice touch, but since every box rewrites itself into the right position in the dictionary it would work out in any order; the recursive stack holds the set of boxes to update).

### Part 2

Changing the width of the boxes has little effect on the creation of the different objects (as discussed above), and the horizontal movement (just need to check two steps ahead instead of one for walls or boxes, and it introduces a little asymmetry for the robot: boxes are one step away to the right, but two steps away to the left). Just for fun, we will mostly make this general for any width; this is already Part 2, so we don't expect any more extensions, but this way we can re-solve Part 1 with the same code.

We have gone over the changes in horizontal movement already, but vertical movement is more complex. First, the robot now has to check the position right above/below it as before, but also the one to the left of that, because a box there extends into its path. In general, this extends to `width - 1` steps to the left (the one that is removed is the one right above/below the robot).

Moving the boxes is the real doozy. We will build a `show` function just to be able to check that everything works as expected, and debug behaviour; also, we can create a few test scenarios to try to catch edge cases, and there are a few that can bite us.

Since a box can now push two other boxes, and this can extend, a new situation appears: a box may be able to move, but not do so because another box in this *tree* is blocked. The simplest case is that the robot pushes a box, which in turn pushes two others, one free to move, one set against a wall: nothing moves.

This changes one big thing about our previous approach: we acn no longer move as soon as we check for feasibility; feasible movement in one branch of the tree no longer ensures that everything will move. So we will separate checking, which only validates whether it's possible, and actually moving (assuming that the check has been made). Both still rely on recursively calling the next box(es), if any.

All that's left is to make a few adjustments to ensure that we properly check which boxes are affected by a move with the new width. There are now multiple positions for a box to be affected: from a box shifted to the left so that its rightmost bit is above/below the current box's leftmost bit, to a box shifted to the right so that its leftmost bit is above/below the current box's rightmost bit. That's a `[-(width - 1), width)` range for the offset; note that it's closed to the left and open to the right (which neatly maps to the beheviour of Python's `range`).

So that's it, right? Well, no. There is a subtle problem that is causing incorrect movements in some situations. If we go beyond the simplest tree of boxes pushing other boxes, and reach a third level (think one box, pushing two other, which in turn push another three, one of which is in contact with both the boxes in the previous levels). The recursive calls to check feasibility still work OK in this situation, but the calls to move actually update its position twice, so it moves further than it should.

The solution is to only make the recursive call to move if the boxes are still in contact; the depth-first design ensures that all boxes in a lower level have moved before a box in the upper level does, so only the first of potentially several paths that reach a given box will actually cause a move. That's the role of `Box._touches()`. Also, the order of movement now is relevant, as opposed to the situation in Part 1: we need the boxes further down the tree to move before, so that when a second box tries to move them again, they are no longer in contact with it, and that push is lost as expected.



## Day 16

This is all about the representation. With the right choice, finding the solutions is largely trivial (using preexisting algorithms).

We will represent this as a (directed) graph. But instead of one node for each position, we will use four, one for each heading. Nodes for each heading only communicate with their neighbour node in that direction (if it's not a wall) with a cost of one step of movement, and with some of the other headings for the same position with a cost of one turn; to be precise, each heading communicates with the other two that can be reached by a 90-degree turn.

We also keep track of thek start and end nodes. For the start we have a heading, so it maps directly to one of our nodes. For the end, the heading is not relevant. We will just remove the cost for turning at the end node and arbitrarily select one heading for the target, it makes no difference which. Alternatively we could add a final node (no heading associated to it), and link the four nodes corresponding to the end position at no cost.

### Part 1

Trivial call to `shortest_path_length`, once the graph is built.

### Part 2

The second part just requires enumerating all the shortest paths (we have a standard algorithm for that), and checking the size of their union.



## Day 17

We need a computer following the given specifications. It's not difficult, and there are not *tricks* to implementing it; we will handle combo arguments with a method to take care of the calculations, and some repetitive operations (e.g. the several division operators that only differ in the target register) are generalized. Also, the operations have been implemented mostly as bitwise operations and shifts for efficiency: dividing by `2^n` is equivalent to shifting right `n` bits, modulo 8 is equivalent to an `and` with the mask `b111`, which is 7 in decimal.

A few other practical choices:

*   Since the opcodes are given numerically, we keep the operations in a list and access it by index, which makes calling an operation the quite readable `self.ops[opcode]`.
*   Each operation immediately increments the instruction pointer; since the adjustments done by `jnz` are absolute, there is no impact there, and we can avoid needing to update it in every operation, which is a recipe for an infinite loop (just need to forget it in one operation, and we're stuck there).
*   To make everything as general as possible, `out` is just another operator, which does nothing, but returns the output value; other operators perform their operation, but do not return anything. The computer outputs any operation result, which corresponds to the `out` operations, but can easily change in the future.
*   Since we will need to look into the inner workings, we will have a debug flag to print every operation with its argument and every output operation.

### Part 1

Let's just use the `Computer` to run the code and collect the output.

### Part 2

Let's find a quine for this machine!

First, we will need to understand what the program is doing; brute force will not cut it here. We will build a reverse engineering system that transforms the code into something more interpretable, like `pseudocode`. We just do one pass over the code and provide a more human-friendly version of the operation and argument. The argument takes the form `literal | combo`, and the description of the operation indicates which to use:

```
bst: b <- combo & 7   --   4 | a
bxl: b <- b xor arg   --   3 | 3
cdv: c <- a >> combo   --   5 | b
adv: a <- a >> combo   --   3 | 3
bxc: b <- b xor c   --   1 | 1
bxl: b <- b xor arg   --   5 | b
out: output combo   --   5 | b
jnz: if a == 0 nop else ip <- arg   --   0 | 0
```

We can see it's a single loop that we can rewrite (moving the shifting of `a` for clarity) as:

```python3
while a:  # until all bits have been used up
    b = a & 7  # b <- the last 3 bits of a
    b ^= 3
    c = a >> b
    b ^= c
    b ^= 5
    # output the value of (b & 7) now
    a >>= 3  # shift a 3 bits to the right ==> discard the three bits used for b
```

In other words, take the last 3 bits of `a`, do some operations with them, return the result, discard thos bits; repeat until all of `a` is used up. There is a little additional complexity in that one of the operations involves using `a` (shifted by `b` to the right), so the higher bits are relevant, which means that we can't just solve each 3-bit piece independently.

But now we have a clear target: we want to find the value of `a` that when applying this procedure returns the code in order, so we know what the value of (the last 3 bits of) `b` should be at the end of each iteration, and how many iterations we need. We can build `a` from the least significant bits up, or from the most significant bits down. Since the higher bits are needed to do the calculations in each iteration of the loop (but not the lower ones), we will chose the latter; otherwise we will be setting constraints on the higher bits that are a bit of a nightmare to keep track of.

We will need to do a recursive search; the need to use the higher bits of `a` means that there may be some values that match at one stage, but result invalid later on as we add more bits. We will keep track of the position in the output, to know our target for `b` at each step, but also to ensure that the first three bits are not all zero, as that would cause an early termination and the last value (at least) would not be generated.

At each step, we shift `a` 3 bits to the left, try out all the values from 0 to 7 (skipping 0 for the highest 3 bits) to see if any generate the desired output. Those who don't are dead ends in the tree search, those who do get to search deeper. If we reach the last value to generate and succesfully generate it (that's at index 0, so if we enter a call with index -1), we have our result.

Just to be extra sure, we rerun the code in a `Computer` with `a` initially set to this value and check that we indeed get back the code as output.



## Day 18

Another easy one when cast into a graph. In this case we just generate a graph with nodes at each position and communicated with their horizontal and vertical neighbours, using the usual 'only look at nodes already passed in the loop' trick.

### Part 1

For the given number of time steps, get the coordinates of the *falling byte*, and remove it from the graph, together with the edges that connected to it. With the resulting graph, calculate the shortest path length from start to end.

### Part 2

This time let's go step by step, and after every removal just check if there exists a path from start to end. We are using a pre-existing algorithm, but it would be as easy as building the connected component of the start, breaking early (returning `True`) if the end node is reached at any point, or returning `False` if the component is done without it.

We just look at the coordinates of the last step, which caused the block, and return that.



## Day 19

We go back to recursive search. In this case, generating longer patterns (targets) from smaller building blocks (patterns). We will create a `PatternMatcher` class to do the heavy lifitng. We will discuss here the data structures, and leave the methods that do the search for each part.

We will build a kind of prefix tree, by keeping the available patterns in a dictionary with pattern length as key and the set of patterns of that length as value. This will make it easy to iterate through paterns up to a specific lenght (useful for the last additions) and to handle the adjustment of the target for the recursion. As we add patterns, we will keep track of the maximum length of the patterns, for looping.

### Part 1

Can we build a given target? It's the classic look for all paterns that match the begining of the target, recurse to check if what remains of the target can be built. When the target becomes the empty string, the answer is yes; if at some point we have no match, the answer is no.

The `match` method finds all matching patterns by taking the start of the target for length 1, 2, ... until either the maximum pattern length or the target length (whichever is lesser), and checking if that sequence is in the available patterns of the corresponding length, and if so yielding it.

Checking if a target is possible is just a matter of recursing this matching procedure. Expecting the usual, we will build directly a cached version. We always call `can_build`, wihch in turn calls `_can_build` in case of a cache miss to actually do the calculation. `_can_build` recurses into `can_build` to take advantage of the cache. It appears that there is no base case for this recursion, but it is actually integarted by initializing the cache with the answer to the base case when the target is the empty string.

### Part 2

This is a little different: we need to find all possible ways, instead of just one. The logic behind it is exactly the same, only we don't immediately stop as soon as one way is found, and we don't return just `True` or `False`, but the count of feasible solutions, which is the sum of the ways in which the rest of the target can be build after removing each matching pattern in this step.

As before, we memoize this function, and initialize the cache with the result for the base case of the recursion: there is 1 way to build the empty string.



## Day 20

This one looks very much like some others where we turned to graphs, but it is not really a good fit in this case: there is a single path, and the kind of questions don't really match graph theory algorithms.

So we will record the start and end positions, the one existing path, and the distances from each position in the path to the end. Once we have all the nodes, it's easy to build the path: from the start, take the only feasible neighbour; move there, and get the only feasible neighbour (that isn't visited yet, no turning back). We can just follow this procedure and represent the path as a dictionary of predecessor--succesor pairs. For the distances, also a dictionary, we just build a stack going through the path, and then count from the end (distance zero), adding one for each step back by popping the stack.

### Part 1

In the end, the question boils down to: in how many ways can you gain more than 100 steps by crrossing a wall? We can easily calculate all the cheats for each step in the path, by looking at all the positions at a distance of two steps (a single step cannot cross a wall, so it will only take you at best to the next step in the path, with no actual gain), and calculate the gain for those that are in the path; this is just the distance to the end from the position where we start the cheat (what it would take following the original path) minus the distance to the end from the new point in the path where we rejoin it plus 2, to count the time of the cheat (the new distance from the point where the cheat starts).

### Part 2

Now cheats can be longer, but the reasoning is exactly the same, only instead of distance 2, it's up to distance 20. Since we need to add the cheat distance when determining the time saved, we actually need to do it for distances 2, 3, ..., 20. As soon as there are a few steps, enumerating all possible paths explodes, but we don't need to do it, because a cheat is defined by the start and end points, so only that is needed. Basically, we need to iterate over the distance, find the boundary of the (norm-1) ball for that distance, and check which of those rejoin the path, and give positive savings---specifically over the limit set for counting.

In reality, we will take a couple of shortcuts. Instead of building each ball boundary, we will generate the whole 20-radius ball at once, which is simpler to do, and for each position that matches the path we can calculate the length of the cheat as the distance between the cheat's start and end (since a cheat is defined by those two points, we assume that the (one of the) fastest route(s) between them is taken). This is what the `deltas` function does; it could be run just one and stored into a list or tuple for reuse each time, if we want to optimize it further. We avoid the positions at distances 0 and 1, as they can't provide an advantage in any case.



## Day 21

This is inception with robots. It can be hard to keep track of which level you're at when deciding what the next move is.

We will represent the keypads by the (complex) position of the buttons. In wither case, we will set the 'A' button at position 0, which has the nice perk of making -2 the gap in the keyboard that has to be avoided.

When building a sequence of moves, we will move horizontally first if going left, and vertically first if going right; if doing this would take us to the gap, we invert it. My first though was to always use the inversion, which guarantees never passing over the gap, but it results in longer sequences. I didn't think it fully through, since I saw the heuristic in Reddit, and it solved the problem (the test was working with the other option!).

### Part 1

It's easy to translate the sequence of buttons into a sequence of moves. The numerical keyboard only appears at first, so it's the source of the first translation, but others are always directional keyboards, so the logic is always the same (i.e. the target of the translation is the directional keyboard); and the complex representation of the keyboards makes the translation work the same in both cases.

In this first part, it's straightforward to just do the translations sequentially and build the sequence explicitly. It's always important to keep track of the previous button, as the movements to reach the new target are different depending on where we were before. But in the end it's a matter of iterating over the sequence, applying `translate` to each move (source and destination keys, starting from 'A' before the first button) to get the next level sequence; then process that sequence again (and a third time).

### Part 2

We could, in theory, repeat the same process as in Part 1, only 26 times; but that grows too large and too computationally intensive. So we need to think more carefully.

The main insight here is that, because everytime we need to push 'A' to validate, every move is independent of the rest of the sequence. And with so few buttons, only a limited number of moves exist: 20. There are also a limited number of keyboard depths, so to speak. We can memoize based on the move and the number of keyboard indirections to be made; it's a complex web of recursion, but it works out.

So we `process` each code as a sequence, calculating the lenght of each move defined by the sequence and the number of indirection steps; this is `calculate_len`, the cached result, and it recursively calls `process` to get the legth of the next level of indirection for the `translate`d move. Since we already have a `cached` decorator and the requests to `translate` a given move will repeat often (there are only a handful of movements after all), we can also memoize it.



## Day 22

Let's build a PRNG.

### Part 1

This part is straightforward: just a loop, where each step applies the operations that are indicated. We can make them a little more effective observing that all the multiplying and dividing is by powers of two, so we can just shift accordingly. We could go one step further if we wanted further optimization, notice that 16,777,216 is $2^{24}$, so the modulo operation can be substituted by and-ing with 16,777,215.

### Part 2

To find the best sequence efficiently, we can first evaluate what sequences actually appear in the price streams, and what is the value they provide. For each monkey, we can go through the stream, recording the sequence of the last four diferences, and at each step recoding the sequnce and the number of bananas it yields; if the sequence is already recorded, we just ignore it, as selecting that sequence means that this point in the stream is not reached (it would have stopped at the first accurrence).

We can then merge the results from all the streams: add together the results for each sequence.

Finally, we select the sequence with the most bananas.

This approach just goes once through each stream, once through each seqeunce-to-bananas dictionary to do the merge, and once more through the merged dictionary to get the maximum. Going brute-force, would mean instead going though all possible 4-sequences (roughly, 160,000), and for each going through each stream to find the yield in bananas, possibly until the end if the sequence does not occur.


## Day 23

This is begging for a graph representation: the input is exactly the list of edges.

### Part 1

The question can be simplified to: find all cliques of size 3 in the graph. We will do it manually, just for fun. And since it's just for fun, and fast enough, we won't try to optimize: we'll keep track of the cliques we find in a set, and let that deal with duplicates that will appear.

We just look at each node. We get its neighbours, and for each neighbour we get *its* neighbours, let's call these the second-order neighbours. For each neighbour, we get a 3-clique for each second-order neighbour which is also a first-order neighbour. We build the corresponding clique as a `frozenset` so we can add it to our clique set. We could also use tuples, but that would require normalizing the order of the nodes in the clique (e.g. sorted alphabetically).

For the final answer, we only need to count, filtering by the condition of containing a node starting with 't'.

### Part 2

We could build on the previous step to grow the largest clique, but that would soon become too slow without properly adjusting the algorithm. Instead, we take advantage of the functionality of `networkx` and just `enumerate_all_cliques`; we discard all by the last, which is the largest, and the one we are interested in. Sort and join.



## Day 24

We know from the beginning that it's going to be a circuit built with logic gates, so we will design sround that. First we get the values input into the wires, and store that as a dictionary. The gates we will also gather into a dictionary with the output (which will also identify the gate) as the key, and a tuple (operation, input1, input2) as the value.

### Part 1

We need to simualte the logic see the values of the nodes starting with 'z'. We can evaluate a wire recursively: if we know the value (in the values dictionary), that's it; if not, get the values of the inputs to the gate, perform the operation, and store the result in values. This will populate all the values needed to calculate the requested nodes.

We use a shift-then-or loop to build the resulting number from the gate values.

### Part 2

We will resot once more to a visual approach in this case. We can build a graphviz diagram representing the circuit. The `flowchart` function generates the code for that. We can see the result in this [image](puzzle24.png), which is too large to usefully inline.

A quick review of the chart shows a repeating structure that adds each binary digit and propagates the carryover. A more in-depth analysis finds the blocks where the structure is not the right one. For some it's quite obvious, as the 'wires' change shape because of the misconnection; in other cases is more subtle, as it's only the labelling of the outputs (e.g. the carryover is fed to the output 'zxx' and the output is propagated to the next block as if it were the carryover).

With the offending wires identified in this way, the solution is hardcoded.


## Day 25

We will make it easy to check if a key fits in a lock. For locks, we will enconde the size of each gap, while for the keys we will encode the size of the tooth. Then each will be represented by a 5-tuple, not unlike the representation used in the description of the puzzle, but with the nice property that a `key` fits in a `lock` if `all(k <= l for k, l in zip(key, lock))`.

To build the representation, we use a list of lists, that will work as a matrix; for each line, we append 1 or 0, depending on the character and what we are counting (different for keys and locks). This builds the matrix-like representation as it is drawn, with each tooth or gap as a column, so we transpose the matrix (that's the effect of `zip(*matrix)`) and add along the rows.

### Part 1

No fancy algorithm today: loop over the combinations of keys and locks, and count how many fit.

### Part 2

As usual, Part 2 is a XMAS gift!
