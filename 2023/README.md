# Advent of Code 2023

Python and Haskell solutions read from `stdin` and can be run like this:

```sh
python solution.py < input.dat
ghc Solution.hs && ./Solution < input.dat
```

Solutions written in other languages usually read from `stdin`, but might have a different method of receiving a file.

## Scoreboard

✔ : Finished on time  
🆗 : Finished, but a little late  
⭐ : Free star  
Delta: Time between finishing part 1 and 2  
Late: The day I finished the task, if it wasn't the day the task was given  
Time: Execution time, measured with `time`

Languages: Python (🐍), Haskell (λ), C++ (➕), Bourne Shell (🐚)

| Puzzle | Part 1 | Part 2 | Delta   | Late   | Time   | Language | Comment                              |
| ------ | ------ | ------ | ------: | ------ | -----: | -------- | ------------------------------------ |
| Day 1  | ✔      | ✔      | 1:03:54 |        | 16 ms  | 🐚       | All the sed                          |
| Day 2  | ✔      | ✔      | 05:01   |        | 8 ms   | λ        | Haskelled                            |
| Day 3  | ✔      | 🆗     | 1 day   | Day 4  | 367 ms | 🐍       | Off-by-one lead to too few gears     |
| Day 4  | ✔      | ✔      | 39:32   |        | 6.45 s | 🐍       | Part 2 solved in a hilarious way     |
| Day 5  | ✔      | 🆗     | 4 days  | Day 9  | 71 ms  | 🐍       | Bugs + too little time = postponed   |
| Day 6  | ✔      | ✔      | 00:16   |        | 21 ms  | 🐍       | This day is O(1)                     |
| Day 7  | ✔      | ✔      | 37:38   |        | 2.02 s | 🐍       | Pattern matching woohoo!             |
| Day 8  | ✔      | ✔      | 1:23:54 |        | 49 ms  | 🐍       | gcd ftw                              |
| Day 9  | ✔      | ✔      | 00:07   |        | 67 ms  | 🐍       | Why was this so simple?              |
| Day 10 | ✔      | ✔      | 02:02   |        | 664 ms | 🐍       | Upscaled for ez squeeze              |
| Day 11 |        |        |         |        |        |          |                                      |
| Day 12 |        |        |         |        |        |          |                                      |
| Day 13 |        |        |         |        |        |          |                                      |
| Day 14 |        |        |         |        |        |          |                                      |
| Day 15 |        |        |         |        |        |          |                                      |
| Day 16 |        |        |         |        |        |          |                                      |
| Day 17 |        |        |         |        |        |          |                                      |
| Day 18 |        |        |         |        |        |          |                                      |
| Day 19 |        |        |         |        |        |          |                                      |
| Day 20 |        |        |         |        |        |          |                                      |
| Day 21 |        |        |         |        |        |          |                                      |
| Day 22 |        |        |         |        |        |          |                                      |
| Day 23 |        |        |         |        |        |          |                                      |
| Day 24 |        |        |         |        |        |          |                                      |
| Day 25 |        |        |         |        |        |          |                                      |

(Table generated with this macro: `'mhye<c-a><c-o>vepbhj`)

Current total: Around **9.169** seconds  
Goal: Less than **30** seconds

(Estimates summed with [sum.sh](sum.sh) which uses [sum.awk](../2020/sum.awk) from 2020)
