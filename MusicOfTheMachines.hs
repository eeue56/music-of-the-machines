module MusicOfTheMachines
where

    generateFrequency :: Double -> Double
    generateFrequency x = 440 * 2 ** (x / 12)

    envelope :: Double -> Int -> Double -> Int -> Double
    envelope maxVolume iterations currentVolume currentStep
        | currentStep <= forth = currentVolume + volumeIncrease
        | currentStep >= forth * (2.0 / 3) = currentVolume + (volumeIncrease / 2)
        | currentStep >= forth * (5 / 3) = currentVolume - (volumeIncrease / 1.5)
        | currentVolume < 0 = forth / 4
        | otherwise = currentVolume - (volumeIncrease / forth)
        where
            forth = quot iterations 4
            lastS
            volumeIncrease = maxVolume / forth


    main = do 
        let test = envelope 32000 100
        putStrLn $ show $ test 1000 10