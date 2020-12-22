import Data.List

-- In the style of this:
-- https://www.youtube.com/watch?v=LjrCckaHjB0
-- with an infinite, recursive list
--
-- if combs is combs when taking n adapters:
-- combs[n] = (for 1..3: combs[n-i] if xs[j] - xs[j-i] <= 3)
--
-- This solution is slower than the Python solution (140 vs 20 ms)
-- because of the use of takeWhile and dropWhile or my equivalent function

takeWhileAfter _ [] = []
takeWhileAfterDrop pred (x:xs)
    | pred x    = takeWhile pred (x:xs)
    | otherwise = takeWhileAfterDrop pred xs

solve xs' = combs !! (length xs - 1)
    where xs'' = 0 : sort xs'
          xs   = xs'' ++ [last xs'' + 3]
          combs = 1 : map (\x ->
              sum
              $ map snd
              $ takeWhileAfterDrop (\(y, _) -> y < x && x - y <= 3)
              $ zip xs combs)
            (tail xs)

main = interact $ show . solve . map read . words
