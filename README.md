# Python static site generator

This guided project is part of the [Boot.dev](www.boot.dev) back-end developer
path. It is intended to be used as a learning resource for myself so that I can
get a better understanding of the inner workings of static website generators by making my own.

Initial start date: 14 April 2026 at day 32 on Boot.dev. Just finished Data Structures and Algorithms course.

## Reflections

### Highlights

- The most satisfying part of this whole project was being able to build
something that I can call my own; something that I've thought about for days on
end, and written by my own hands. 

- For better or worse, the way I programmed
this static site generator differed in significant ways from the solution
files. I can see the trade-offs between complexity and simplicity, and how my
own code can handle unexpected markdown formatting better than the provided solutions,
albeit being a little messier to work with and less performant (I mean, it's
Python, so what else do you expect?).

- I've been using Neovim for the entirety of this back-end development course,
and will continue to do so in the future. It's fantastic to finally be able to
flex my vim motion muscles in a real setting like this project. I'm pushing the
limits of what I already know, given the fact that I've been using Vim for the
past 2 years prior to this course (though not really for coding), and I'm STILL
learning new ways of navigating the IDE, whilst also using new functionalities
that boost my productivity to the max.


### Most challenging moments

- _CH3: Inline, L1: Split delimiter_: I felt a massive difficulty jump from one
chapter to another. No pseudocode was given, and I'm given full reign on the
implementation for a function that is meant to convert TextNodes to HTMLNodes
according to a given formatting delimiter. The approach that I used was far
more complicated than the solution files, but turned out to be more robust as
it is able to handle unclosed delimiters. I took inspirations from how Obsidian
and Discord handles markdown format. However, I was unable to replicate italics
formatting behaviour where closing `_` characters wouldn't format to italics
unless if it's followed by a space. I'm sure there's a good reason for it, but these lessons have already gone on for too long and I'd like to move onto the "Memory Management in C" chapter.

- _Refactoring codebase and test cases_: I discovered that I split utility
functions across multiple files for no good reason. I ended up merging
functions into existing files for better organisation. The biggest refactor was
to the test case files, where I also merged test case files into one, instead
of having them all be separate, with one test file being used to test one
function. It made things pretty confusing, so I decided to follow the solution
files after completing the task as a better model for how I should be writing
test cases; I relied too much on print statements when I should have been
defining new test functions within a Test class.

- Writing documentation: I found it very difficult to explain what a function
does without overcomplicating it. Throughout this project, I tried to maintain
a strict mindset, where I assumed that everything that I've written could be
read by someone one day. It was thus equally important for me to keep a clean
git commit history, and to assume that I'm working in a production environment
as a way to challenge myself. I think it paid off in the end.

