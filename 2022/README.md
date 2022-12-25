# Advent of Code 2022

Python files read from `stdin` and can be run like this:

```sh
python part_one.py < input.dat
```

Solutions written in Haskell and other languages might have a different method of receiving a file – typically as an argument or through `stdin`.

## Scoreboard

✔ : Finished on time  
🆗 : Finished, but a little late  
⭐ : Free star

Delta: Time between finishing part 1 and 2  
Late: The day I finished the task, if it wasn't the day the task was given  
Time: Execution time, measured with `time`

Languages: Python (🐍), Haskell (λ), C++ (➕)

| Puzzle | Part 1 | Part 2 | Delta | Late   | Time   | Language | Comment                                                               |
| ------ | ------ | ------ | ----: | ------ | -----: | -------- | --------------------------------------------------------------------- |
| Day 1  | ✔      | ✔      | 01:52 |        | 26 ms  | 🐍       |                                                                       |
| Day 2  | ✔      | ✔      | 06:33 |        | 62 ms  | 🐍       |                                                                       |
| Day 3  | ✔      | ✔      | 07:49 |        | 55 ms  | 🐍       |                                                                       |
| Day 4  | ✔      | ✔      | 03:36 |        | 30 ms  | 🐍       |                                                                       |
| Day 5  | ✔      | ✔      | 01:00 |        | 24 ms  | 🐍       |                                                                       |
| Day 6  | ✔      | ✔      | 07:02 |        | 27 ms  | 🐍       | Spent less than 7 minutes on part 2, but had to postpone answer input |
| Day 7  | ✔      | ✔      | 08:58 |        | 37 ms  | 🐍       |                                                                       |
| Day 8  | 🆗     | 🆗     | 58:35 | Day 9  | 141 ms | 🐍       | Spent too much time doing dynamic programming when brute force worked |
| Day 9  | ✔      | ✔      | 12:38 |        | 239 ms | 🐍       |                                                                       |
| Day 10 | ✔      | ✔      | 16:58 |        | 58 ms  | 🐍       |                                                                       |
| Day 11 | ✔      | ✔      | 08:14 |        | 4.2 s  | 🐍       |                                                                       |
| Day 12 | ✔      | ✔      | 07:27 |        | 857 ms | 🐍       |                                                                       |
| Day 13 | ✔      | ✔      | 11:43 |        | 44 ms  | 🐍       | Abused generators, eval(), exceptions and sorting                     |
| Day 14 | ✔      | ✔      | 48:18 |        | 2.9 s  | 🐍       | Bus ride interrupted this time smh                                    |
| Day 15 | ✔      |        |       |        |        |          |                                                                       |
| Day 16 |        |        |       |        |        |          |                                                                       |
| Day 17 |        |        |       |        |        |          |                                                                       |
| Day 18 | ✔      | ✔      | 34:06 |        | 155 ms | 🐍       |                                                                       |
| Day 19 |        |        |       |        |        |          |                                                                       |
| Day 20 |        |        |       |        |        |          |                                                                       |
| Day 21 | ✔      | ✔      | 57:02 |        | 79 ms  | 🐍       | Dinner break. Had to redo as tree.                                    |
| Day 22 |        |        |       |        |        |          |                                                                       |
| Day 23 | ✔      | ✔      | 01:48 |        | 48.8 s | 🐍       | This year's game of life variant. Wrote elegant but slow code 🙃      |
| Day 24 |        |        |       |        |        |          |                                                                       |
| Day 25 | ✔      |        | -     |        | 57 ms  | 🐍       |                                                                       |

(Table generated with this macro: `'mhye<c-a><c-o>vepbhj`)

Current total: Around **57.791** seconds  
Goal: Less than **30** seconds (**needs some optimization**)

(Estimates summed with [sum.sh](sum.sh) which uses [sum.awk](../2020/sum.awk) from 2020)
