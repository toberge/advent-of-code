import Data.List.Split
 
-- Extended Euclidean algorithm
innerInv :: Integer -> Integer -> (Integer, Integer, Integer)
innerInv a 0 = (1, 0, a)
innerInv a b = (t, s - q * t, r')
  where (q, r) = divMod a b
        (s, t, r') = innerInv b r

-- Modular inverse of a mod b
-- (using Maybe might be better, but in this simple case I'll error out)
inv :: Integer -> Integer -> Integer
inv a b
  | r == 1    = t
  | otherwise = error "Whoops, no such moular inverse"
  where (t, _, r) = innerInv a b


-- I don't wanna come up with a better name rn, ok?
makeBusThing :: (Integer, Integer) -> String -> (Integer, Integer)
makeBusThing (_ ,offset) str = (num, succ offset) where
    num = if str == "x" then -1 else read str

splitInput :: String -> [(Integer, Integer)]
splitInput = filter (\(x,_) -> x /= -1)
    . scanl makeBusThing (-1, -1)
    . splitOn ","


-- From https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
chinesify :: Integer -> (Integer, Integer) -> Integer
chinesify n (m, offset) = ((m-offset) * b * b') `mod` n where
    b = n `div` m
    b' = inv b m

solve :: [(Integer, Integer)] -> Integer
solve xs = (sum $ map (chinesify n) xs) `mod` n where
    n = product $ map fst xs


main = interact $ show . solve . splitInput . head . tail . words
