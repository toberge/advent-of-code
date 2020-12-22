import Data.List

solve xs' = ones * threes
    where xs = 0 : sort xs' -- remember the outlet!
          diffs = zipWith (-) (tail xs) xs
          ones = length (filter (== 1) diffs) 
          threes = 1 + length (filter (== 3) diffs) -- one extra to the device

main = interact $ show . solve . map read . words
