import Data.Map hiding (map, splitAt, null)
import System.Environment

type Command = Int -> State -> State

type Instruction = (String, Int)

--                  ops      ip  acc lastAcc
data State = S [Instruction] Int Int Int
            deriving (Show, Eq)

type StopCondition = State -> Bool

nop :: Command
nop _ (S ops ip acc _) = S ops (ip+1) acc acc

jmp :: Command
jmp arg (S ops ip acc _) = S ops (ip + arg) acc acc

acc :: Command
acc arg (S ops ip acc _) = S ops (ip+1) (acc + arg) acc

commandList = [
    ("nop", nop),
    ("jmp", jmp),
    ("acc", acc)
              ]

commands = fromList commandList

cmd :: State -> State
cmd state@(S ops ip _ _) = (commands ! name) arg state where
    (name, arg) = ops !! ip

run :: StopCondition -> State -> State
run cond state
  | cond state = state
  | otherwise  = run cond $ cmd state

splitInstruction :: String -> Instruction
splitInstruction line = (word, number) where
    ( word, raw ) = splitAt 3 line
    number = read $ map (\c -> if c == '+' then ' ' else c) raw

readInstructions :: [String] -> [Instruction]
readInstructions = map splitInstruction

getAcc (S _ ip acc last) = (ip, acc, last)

partOne (S _ _ acc _) = acc == 5

main = do
    args <- getArgs
    stuff <- readFile $ if null args then "example.dat" else head args
    let instr = readInstructions $ lines stuff
    let state = S instr 0 0 0
    print $ show $ getAcc $ run partOne state
