import System.Environment
import qualified Data.Map as M
import Data.Maybe (fromMaybe)

data Count = Count Int Int

readLines = do
    args <- getArgs
    stuff <- readFile $ if null args then "example.dat" else head args
    return $ lines stuff

checksum :: [String] -> Int
checksum =
    count 0 0 where
        count :: Int -> Int -> [String] -> Int
        count twos threes [] = twos * threes
        count twos threes (x:xs) = 2
        -- ehehehe I am not used to Haskell anymore

main = do
    ids <- readLines
    putStrLn "Part One: Checksum"
    print $ checksum ids
    putStrLn "Part Two: First to appear twice"
