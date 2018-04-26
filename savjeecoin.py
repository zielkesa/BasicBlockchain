# A python implementation of a simple crypto currency

import hashlib
import time

class Transaction:
    def __init__(self, fromAddress, toAddress, amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount

    def to_string(self):
        theString = self.fromAddress + self.toAddress + str(self.amount)
        return theString

class Block:
    def __init__(self, timestamp, transactions, previousHash = ''):
        self.nounce = 0
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.hash = self.calculateHash()

    def calculateHash(self):
        transStr = ''
        for i in self.transactions:
            transStr = transStr + i.to_string()
        hString = self.previousHash + str(self.timestamp) + \
                  transStr + str(self.nounce)
        return hashlib.sha256(hString.encode('utf-8')).hexdigest()

    def to_string(self):
        aString = 'Block: {0}\nTimeStamp: {1}\nData: {2}\nPreviousHash: {3}\nHash: {4}\n'.format(str(self.index), str(self.timestamp), self.data, self.previousHash, self.hash) 
        return aString

    def mine_block(self, difficulty):
        while int(self.hash[0:difficulty], 16) != 0:
            self.nounce = self.nounce + 1
            self.hash = self.calculateHash()

class Blockchain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.difficulty = 2
        self.pendingTransactions = []
        self.miningReward = 100

    def createGenesisBlock(self):
        return Block(time.time(), 
            [Transaction('Genesis', 'Genesis', 0)])

    def getLatestBlock(self):
        return self.chain[-1]

    def minePendingTransactions(self, miningRewardAddress):
        newBlock = Block(time.time(), 
                         self.pendingTransactions, 
                         self.getLatestBlock().hash)
        newBlock.mine_block(self.difficulty)

        print('Block successfully mined!')
        self.chain.append(newBlock)

        self.pendingTransactions = [
            Transaction('Satoshi', miningRewardAddress, self.miningReward)]

    def createTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    def getBalanceOfAddress(self, address):
        balance = 0
        for block in self.chain:
            for trans in block.transactions:
                if trans.fromAddress == address:
                    balance -= trans.amount
                elif trans.toAddress == address:
                    balance += trans.amount
        return balance

    def to_string(self):
        aString = ''
        for i in self.chain:
            aString = aString + i.to_string()
        return aString

    def isChainValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i-1]
            if(currentBlock.hash != currentBlock.calculateHash()):
                return False
            if currentBlock.previousHash != previousBlock.hash:
                return False
        return True

#https://www.youtube.com/watch?v=fRV6cGXVQ4I

savjeeCoin = Blockchain()
savjeeCoin.createTransaction(Transaction('address1', 'address2', 100))
savjeeCoin.createTransaction(Transaction('address2', 'address1', 50))
print('starting miner...')
savjeeCoin.minePendingTransactions('Stephens-address')
print('Balance of address2 is: ' + 
    str(savjeeCoin.getBalanceOfAddress('address2')))

