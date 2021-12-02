import System.Environment
import qualified Data.Set as S
import Data.Maybe (fromMaybe)

parseInt :: String -> Int
parseInt = read . filter (/= '+')

readLines = do
    args <- getArgs
    stuff <- readFile $ if null args then "example.dat" else head args
    return $ map parseInt $ lines stuff

parseInput lines = do
    return $ map parseInt lines

secondInstance :: [Int] -> Maybe Int
secondInstance =
    find S.empty where
        find :: S.Set Int -> [Int] -> Maybe Int
        find _ [] = Nothing
        find found (x:xs)
          | S.member x found = Just x
          | otherwise        = find (S.insert x found) xs

main = do
    nums <- readLines
    putStrLn "Part One: Result"
    print $ sum nums
    putStrLn "Part Two: First to appear twice"
    print $ fromMaybe (-1) $ secondInstance $ scanl1 (+) $ cycle nums
