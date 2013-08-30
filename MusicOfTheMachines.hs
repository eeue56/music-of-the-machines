module MusicOfTheMachines
where

	generateFrequency :: Double -> Double
	generateFrequency x = 440 * 2 ** (x / 12)


	main = putStrLn $ show $ generateFrequency 0