import time

import numpy as np


def huffmanCompression(seqErrorImages):
    encodedSeqErrorImages = []
    codeBooks = []
    counter = 1
    for image in seqErrorImages:
        print(f'\nEncoding frame {counter} of {len(seqErrorImages)}')
        counter += 1
        N = image.size  # The number of symbols
        symbols = np.unique(image, return_counts=True)  # Find the unique symbols and their counts

        # Transpose the array to have the symbols in the first column and their counts in the second
        tempSymbols = np.array(symbols).T.tolist()

        # Initialize the probability list with 2s (2 is used to indicate that the symbol is not found in the image).
        # Each index of the list corresponds to a symbol.
        probList = [2 for _ in range(256)]

        # Fill the probability list with the probabilities of each symbol
        for symbol in tempSymbols:
            probList[symbol[0]] = symbol[1] / N
        # probList = [x[1] / N for x in tempSymbols]

        # Create the Huffman codebook for the current image and append it to the codeBooks list
        codeBook = createCodeBook(probList, 256)
        encodedImage = ''
        start = time.time()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                encodedImage += codeBook[image[i][j]]
        end = time.time()
        print(f'Encoding took {end - start} seconds')
        encodedSeqErrorImages.append(encodedImage)
        codeBooks.append(codeBook)
    return encodedSeqErrorImages, codeBooks


def createCodeBook(probList, size):
    def findMin():
        nonlocal foundInStartingProbList_1, foundInStartingProbList_2, whoAmI  # nonlocal is used to access variables
        # from the outer scope
        minProb = min(probList)
        minIdx = probList.index(minProb)
        if minIdx < size:
            probList[minIdx] = 2  # Set the minimum probability to 2 so that it is not found again
            if whoAmI == 1:
                foundInStartingProbList_1 = True
            else:  # whoAmI == 2
                foundInStartingProbList_2 = True
        else:
            probList.pop(minIdx)
        return minProb, minIdx

    codeBook = ['' for _ in range(len(probList))]
    sumDict = {}

    # min1 and min2 are the two smallest probabilities (min1 < min2)
    # min1 -> 0
    # min2 -> 1

    while probList[-1] != 1:
        if len(probList) == size + 1 and probList.count(2) == size:
            break  # End of the algorithm

        # Find the two smallest probabilities
        foundInStartingProbList_1 = False
        foundInStartingProbList_2 = False
        whoAmI = 1
        minProb_1, minIdx_1 = findMin()
        whoAmI = 2
        minProb_2, minIdx_2 = findMin()

        prob_1_found = False
        prob_2_found = False
        symbolsOfProb_1 = None
        symbolsOfProb_2 = None

        if not (foundInStartingProbList_1 and foundInStartingProbList_2):
            for symbols, prob in sumDict.items():
                if prob_1_found and prob_2_found:
                    break
                if not foundInStartingProbList_1 and not prob_1_found and minProb_1 == prob:
                    prob_1_found = True
                    symbolsOfProb_1 = symbols
                    continue
                elif not foundInStartingProbList_2 and not prob_2_found and minProb_2 == prob:
                    prob_2_found = True
                    symbolsOfProb_2 = symbols
                    continue

        newProb = minProb_1 + minProb_2

        # Fill the codeBook
        if prob_1_found and prob_2_found:
            sumDict.pop(symbolsOfProb_1)
            sumDict.pop(symbolsOfProb_2)
            key = symbolsOfProb_1 + '|' + symbolsOfProb_2
            sumDict[key] = newProb
            probList.append(newProb)
            for symbol in symbolsOfProb_1.split('|'):
                codeBook[int(symbol)] += '0'
            for symbol in symbolsOfProb_2.split('|'):
                codeBook[int(symbol)] += '1'
        elif prob_1_found:
            sumDict.pop(symbolsOfProb_1)
            key = symbolsOfProb_1 + '|' + str(minIdx_2)
            sumDict[key] = newProb
            probList.append(newProb)
            for symbol in symbolsOfProb_1.split('|'):
                codeBook[int(symbol)] += '0'
            codeBook[minIdx_2] += '1'
        elif prob_2_found:
            sumDict.pop(symbolsOfProb_2)
            key = symbolsOfProb_2 + '|' + str(minIdx_1)
            sumDict[key] = newProb
            probList.append(newProb)
            codeBook[minIdx_1] += '0'
            for symbol in symbolsOfProb_2.split('|'):
                codeBook[int(symbol)] += '1'
        else:
            key = str(minIdx_1) + '|' + str(minIdx_2)
            sumDict[key] = newProb
            probList.append(newProb)
            codeBook[minIdx_1] += '0'
            codeBook[minIdx_2] += '1'
    return codeBook


def huffmanDecompression(encodedSeqErrorImages, codeBooks, height, width):
    decodedSeqErrorImage = []
    for image in encodedSeqErrorImages:
        # Decode the image and append it to the list of decoded images
        decodedSeqErrorImage.append(huffmanDecode(image, height, width))


def huffmanDecode(image, height, width):
    decodedErrorImage = np.zeros((height, width), dtype=np.uint8)
    counter = 0
    bitString = ''
    pass
