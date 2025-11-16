Some days ago I finally finished coding the first stable version of the interpreter for  [Stackade](https://github.com/RubenSab/Stackade), my programming language.

Getting tired of testing solutions for increasingly complex and language-specific problems, a rather "simple" problem (or so I thought), of a more abstract nature, piqued my interest.

# A simple problem

The most natural structure you can work with in Stackade is the **Stack**, which is basically a **pile of elements**, nothing more.

From now on, picture it as a **string** like "cba", where "c" is the downmost element and "a" is the upmost, going left to right.

First things first, I wanted to know whether it was possible to start with the string "ab" and end with "abab" using some **sequence** made only by these three **rules**:

- `dup`: duplicates the last character, so "ab" becomes "abb";
- `swap`: swaps the last character and the one before it, so "ab" becomes "ba";
- `rot`: swaps the last character with the third to last, so "abcd" becomes "adcb";

How hard could that be? I thought that two or three steps could make for it, but when trying my hand, I got a solution double as long:

1. **ab** -> ba (swap)
2. ba -> baa (dup)
3. baa -> aab (rot)
4. aab -> aabb (dup)
5. aabb -> abba (rot)
6. abba -> **abab** (swap)

My concern is not finding *a* solution for this particular problem or a family of slightly different ones; I'm interested in finding *the* more efficient solution and demonstrating it, for *any* instance of this kind of problems.

From an even broader perspective, maybe every simple enough problem definable with a "**state**" to **reach** from a **starting one**, plus a **set of rules** to transition from a state to another, can be solved in the **same way**.

# The generic problem is a logic labyrinth

As stated above, every problem compatible with our idea of solution have common features, strikingly similar to the structure of a **labyrinth**:

- a set of states (the *labyrinth*), all with the same features, for example being a string of four characters at most;
- an **initial** state (the *entrance*);
- a "**solved**" state (the *exit door*);
- a set of **rules** to **transition** (the *corridors*) from a state to another. Note that some transitions (the *walls*) could be **impossible** to make. Think about the "ab" -> "abab" example: we could not have applied `rot` to "ab", because it's only two characters long.

Unsurprisingly, the simplest problem solvable with the system we are building is finding the shortest exit path of a labyrinth, provided that the map was properly encoded as a network of nodes, because there's no computation of next states involved, only the traversal of already existing ones.

# Coding it

*Object Oriented Programming* is the perfect fit for this project, because states can be build as **objects** storing particular data while sharing the same generic blueprint specified in their **class**.
On the other hand, **rules** can be implemented as **methods** that compute the produced state and connect it to the previous one, growing the network.