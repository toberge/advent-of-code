module Main where

parse :: String -> [Int]
parse = map read . words

safeInterval :: (Int, Int) -> Bool
safeInterval (x, y) = diff >= 1 && diff <= 3
    where
        diff = abs $ x - y

safeOrder :: [Int] -> Bool
safeOrder xs = ascending || descending
    where 
        right = tail xs
        left = take (length xs - 1) xs
        ascending = all id $ zipWith (<) left right
        descending = all id $ zipWith (>) left right

safeReport :: [Int] -> Bool
safeReport xs = allSafeInterval && safeOrder xs
    where
        right = tail xs
        left = take (length xs - 1) xs
        allSafeInterval = all safeInterval $ zip left right

reportPermutations :: [Int] -> [[Int]]
reportPermutations haha = go [] [] haha
    where
        go :: [[Int]] -> [Int] -> [Int] -> [[Int]]
        go acc xs (y:ys) = go (acc ++ [(xs ++ ys)]) (xs ++ [y]) ys
        go acc xs [] = acc

-- safePermutations :: [Int] -> Bool
-- safePermutations xs = all id $ sum $ map (toNum . safeReport) $ reportPermutations xs
safePermutations = any id . map safeReport . reportPermutations

toNum :: Bool -> Int
toNum True = 1
toNum False = 0

-- part1 = show . sum . map (num . safeReport . parse) . lines
part1 = show . sum . map (toNum . safeReport . parse) . lines
part2 = show . sum . map (toNum . safePermutations . parse) . lines
-- part2 = show . solve game2 . map parse . lines

main = do
  stuff <- getContents
  putStr "Part 1: "
  putStrLn $ part1 $ stuff
  putStr "Part 2: "
  putStrLn $ part2 $ stuff
