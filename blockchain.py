import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import hashlib

class Hash:
    
    def toSHA1(text):
        #to_SHA1()
        #a function that takes a string of data as input and returns a hash value of this data in the form of a string (in
        #this case, the SHA1 function with a length of 160 bits is used as a hashing algorithm).
        hash_object = hashlib.sha1(text.encode())
        hex_dig = hash_object.hexdigest()
        print(hex_dig)
        return hex_dig


class Signature:

    def signData(keyPair, msg):
        #signData(self)
        #a function that allows you to generate a signature. private key and the
        #message to be signed as input. It returns an array of bytes which stores the signature data. Depending on the
        #library and approach used, the input and output types may differ.
        # RSA sign the message
        hash = int.from_bytes(hashlib.sha512(msg.encode()).digest(), byteorder='big')
        signature = pow(hash, keyPair.d, keyPair.n)
        print("Signature:", hex(signature))
        return signature

   
    def verifySignature(signature, msg, keyPair):
        #verifySignature()
        #a boolean function that allows you to verify the signature. The function takes the value of a signature, a
        #public key and a message as an input. The output is true/false depending on the result of verification.
        # RSA verify signature
        hash = int.from_bytes(hashlib.sha512(msg.encode()).digest(), byteorder='big')
        hashFromSignature = pow(signature, keyPair.e, keyPair.n)
        print("Signature valid:", hash == hashFromSignature)
        return hash == hashFromSignature

class KeyPair:

    def __init__(self,privateKey,publicKey):
        #privateKey
            #a large natural number required to sign operations.
        #publicKey
            #a point on an elliptic curve (in the case of using signatures on elliptic curves).
        self.privateKey = privateKey
        self.publicKey = publicKey

    def genKeyPair():
        #a function that generates keys, which returns an object of the KeyPair class.
        """keyPair = RSA.generate(bits=1024)
        #print(f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
        #print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})")
        x = KeyPair(keyPair.d,keyPair.e)"""

        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator) #generate public and private keys
        x = KeyPair(key.privateKey,key.publicKey) 
        return x

class Account:

    def __init__(self,wallet,balance):
        #accountID(String)
            #an unique value for identifying an account within the system. It can often be a public key or its hash value.
        #wallet(array)
            #an array that stores KeyPair objects that belong to the same account.
        #balance(int)
            #an integer value representing the number of coins belongs to the account.
        _publicKey = wallet[0].publicKey
        _hash = Hash.toSHA1(p)
        self.accountID = str(_hash)
        self.wallet[0] = wallet
        self.balance = balance

    def genAccount():
        #a function that allows you to create an account. It returns an object of the Account class. The first key pair
        #is generated and assigned to the account.
        key = KeyPair.genKeyPair()
        #key = RSA.generate(bits=1024)
        account = Account(key,0)
        return account

    def addKeyPairToWallet(self, keyPair):
        #a function that allows you to add a new key pair to the wallet and use it in the future to sign operations
        #initiated from this account. It does not return anything.
        self.wallet.push(keyPair)
        
    def updateBalance(self,_balance):
        #a function that allows to update the state of the user's balance. It takes an integer value as input, and does
        #not return anything.
        self.balance += _balance

    def createPaymentOp(self,recipient,amount,index):
        #a function that allows to create a payment operation on behalf of this account to the recipient. Accepts the
        #account object as input to which the payment will be made, the transfer amount and the key index in the
        #wallet.
        #sign = Signature.signData(self.wallet[index],"baba")
        sign = self.signData("baba",index)
        return Operation.createOperation(self,recipient,amount,sign)

    def getBalance(self):
        #a function that allows to get the state of the user's balance. It returns an integer value.
        return self.balance

    def printBalance(self):
        #a function that allows to display the state of the user's balance. It does not return anything.
        print(self.balance)

    def signData(self,msg, index):
        #a function that allows the user to sign random data. It accepts a message and an index of the key pair in the
        #wallet as input. Returns the value of the signature
        keyPair = self.wallet[index]
        hash = int.from_bytes(hashlib.sha512(msg.encode()).digest(), byteorder='big')
        signature = pow(hash, keyPair.d, keyPair.n)
        print("Signature:", hex(signature))
        return signature

class Operation:

    def __init__(self,sender,receiver,amount,signature):
        #sender
            #payment sender's account.
        #receiver
            #payment recipient's account.
        #amount
            #the amount of the transfer.
        #signature
            #signature data generated by the sender of the payment.
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def createOperation(sender,receiver,amount,signature)
        #a function that allows to create an operation with all the necessary details and signature. It accepts the
        #accounts of the sender and recipient of funds, the amount of the transfer and the signature of the mentioned
        #data. Returns an Operation object.
        x = Operation(sender,receiver,amount,signature)
        return x

    def verifyOperation(self)
        #a function that checks the operation. The main checks (relevant for the proposed implementation) include:
        #verification of the transfer amount (that it does not exceed the sender's balance) and signature verification
        #(using the public key of the sender of the payment). Returns true/false depending on the results of checking
        #the operation.
        x = self.sender.balance >= self.amount
        num = len(self.sender.wallet)
        for i in num:
            y = Signature.verifySignature(self.signature,"baba",self.sender.wallet[i])
            if y==True:
                break
            
        
        return x && y 

class Transaction:


    def __init__(self, setOfOperations, nonce):
        #TransactionID (String)
            #a unique identifier of the transaction (a hash value from all other fields of the transaction).
        #setOfOperations (Array list of operations)
            #a set of payment operations confirmed in this transaction.
        #nonce (int)
            #a value to protect duplicate transactions with the same operations.
        num = len(self.setOfOperations)
        cont = ""
        for i in num:
            cont = cont + str(setOfOperations[i].signature)
        Transaction = Hash.toSHA1(cont)

        self.TransactionID = Transaction.toString()
        self.setOfOperations = setOfOperations
        self.nonce = nonce


    def createOperation(_setOfOperations,_nonce):
        #a function that allows to create a transaction with all the necessary details. It accepts a list of operations and
        #nonce as input. It returns a Transaction object.
        x = Transaction(_setOfOperations,_nonce)
        return x

class Block:

    def __init__(self, prevHash, setOfTransactions):
        #blockID (String)
            #an unique block identifier (the hash value from all other data).
        #prevHash (String)
            #an identifier of the previous block (it is needed to ensure history integrity check).
        #setOfTransactions (Array)
            #a list of transactions confirmed in this block.
        num = len(self.setOfTransactions)
        cont = ""
        for i in num:
            cont = cont + str(setOfTransactions[i].TransactionID)
        _blockID = Hash.toSHA1(cont)
        self.blockID = str(_blockID)
        self.prevHash = prevHash
        self.setOfTransactions = setOfTransactions
        

    def createBlock(_setOfTransactions, _prevHash)
        #a function that allows to create a block with all the necessary details. It accepts a list of transactions and the
        #identifier of the previous block as input. The function returns a Block object.
        x = Block(_setOfTransactions, _prevHash)
        return x

class Blockchain:

    def __init__(self, coinDatabase, blockHistory, txDatabase, faucetCoins)
        #coinDatabase(HashMap[Acount,int])
            #a table reflecting the current state of balances in the system. The account identifier is used as the key, the
            #user balance is used as the value.
        #blockHistory(Array list of block)
            #an array storing all the blocks added to the history.
        #txDatabase(Array list of transactions)
            #an array storing all transactions in history. It will be used for faster access when checking the existence of
            #the transaction in the history (protection against duplication).
        #faucetCoins(int)
            #an integer value defining the number of coins available in the faucet for testing.
        #Account | Block | Transaction
        self.coinDatabase = coinDatabase
        self.blockHistory = blockHistory
        self.txDatabase = txDatabase
        self.faucetCoins = faucetCoins

    def initBlockchain():
        #a function that allows to initialize the blockchain. The genesis block is created and added to the history.
        _coinDatabase = {
            _Account:[Account.genAccount(),],
            _Balance:[0,]
        }
        return Blockchain(_coinDatabase,[],[],1000)
    def getTokenFromFaucet(self, _account, _amount):
        #a function that allows you to get test coins from the faucet. Updates the state of the coinDatabase and the
        #balance of the account that was called by the method.
        num = len(self.coinDatabase._Account)
        for i in num:
            if _account == self.coinDatabase._Account[i]:
                break
        self.coinDatabase._Account[i].updateBalance(_amount)
        self.coinDatabase._Balance[i] += _amount 
        self.faucetCoins -= _amount

    def validateBlock(self, _block):
        #a function that allows you to make a check and add a block to the history.
        self.blockHistory.push(_block)
    def showCoinDatabase(self):
        #a function that allows you to get the current state of accounts and balances.
        print(self.coinDatabase)

class Voting:

    def __init__(self, initiator, prop1,prop2,participants,count1,count2,winner):
        #initiator    [Account]      : account which lauch the vote
        #prop1        [String]       : First Proposal
        #prop2        [String]       : Second Proposal
        #participants [Account List] : List of all voters
        #count1       [int]          : Proposal 1 count
        #count2       [int]          : Proposal 2 count
        #winner       [int]          : 1 if (count1>count2) or 2 if(count1<count2)
        self.initiator = initiator
        self.participants = participants
        self.prop1 = prop1
        self.prop2 = prop2
        self.count1 = count1
        self.count2 = count2

    def initVot(account,prop1,prop2):
        x = Voting(account,prop1,prop2,[],0,0,0)
        return x

    def voting(self,prop,_account):
        if prop == prop1:
            self.count1 += 1
        if prop == prop2:
            self.count2 += 1
        self.participants.push(_account)

    def winner(self):
        if self.count1 > self.count2 :
            self.winner = count2

        if self.count1 < self.count2 :
            self.winner = count2