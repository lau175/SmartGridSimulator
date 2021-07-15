from web3 import Web3
import json


class performTransaction():
    # Connect to Blockchain and prepare contract info.
    def __init__(self):

        ganache_url = "http://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))

        if not self.web3.isConnected():
            print("Connection with blockchain failed.")

        else:
            print("Connected to Blockchain")

        self.abi = json.loads('[{"constant":false,"inputs":[{"name":"payee","type":"address"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"get_meter","outputs":[{"name":"","type":"uint256[20]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newData","type":"uint256[20]"}],"name":"input_meter","outputs":[{"name":"","type":"uint256[20]"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"meter_info","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"payee","type":"address"}],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"deposits","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
        self.bytecode = "608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555061059f806100606000396000f3fe6080604052600436106100555760003560e01c806351cff8d91461005a578063d4b33ea6146100ab578063e5f1a0a8146100fe578063f14c4b3f146101ae578063f340fa01146101fd578063fc7e286d14610241575b600080fd5b34801561006657600080fd5b506100a96004803603602081101561007d57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506102a6565b005b3480156100b757600080fd5b506100c061037a565b6040518082601460200280838360005b838110156100eb5780820151818401526020810190506100d0565b5050505090500191505060405180910390f35b34801561010a57600080fd5b50610170600480360361028081101561012257600080fd5b810190808061028001906014806020026040519081016040528092919082601460200280828437600081840152601f19601f82011690508083019250505050505091929192905050506103c5565b6040518082601460200280838360005b8381101561019b578082015181840152602081019050610180565b5050505090500191505060405180910390f35b3480156101ba57600080fd5b506101e7600480360360208110156101d157600080fd5b8101908080359060200190929190505050610424565b6040518082815260200191505060405180910390f35b61023f6004803603602081101561021357600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff16906020019092919050505061043c565b005b34801561024d57600080fd5b506102906004803603602081101561026457600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506104ca565b6040518082815260200191505060405180910390f35b6000600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205490506000600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055508173ffffffffffffffffffffffffffffffffffffffff166108fc829081150290604051600060405180830381858888f19350505050158015610375573d6000803e3d6000fd5b505050565b6103826104e2565b60026014806020026040519081016040528092919082601480156103bb576020028201915b8154815260200190600101908083116103a7575b5050505050905090565b6103cd6104e2565b8160029060146103de929190610505565b506002601480602002604051908101604052809291908260148015610418576020028201915b815481526020019060010190808311610404575b50505050509050919050565b6002816014811061043157fe5b016000915090505481565b600034905080600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205401600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020819055505050565b60016020528060005260406000206000915090505481565b604051806102800160405280601490602082028038833980820191505090505090565b8260148101928215610534579160200282015b82811115610533578251825591602001919060010190610518565b5b5090506105419190610545565b5090565b61056791905b8082111561056357600081600090555060010161054b565b5090565b9056fea265627a7a723158201ef715fb8084e7ff376a95f9a57bf4fb84a6941ac6fae2d18d8caa4e6701846b64736f6c63430005110032"



    def getaddresses(self, addresses):
        # Get the addresses from Ganache.
        addresses_list = []
        for i in range(len(addresses)):
            addresses_list.append(self.web3.eth.accounts[i])
        return addresses_list
        

    def deploySC(self, people):
        # Deploy smart contract.
        # tx_receipt is list containing integ from zeros to 9
        tx_receipt=[]
        print("Deploy of smart contract.")
        
        
        for buyer in people:
            # Assign addresses to agents.
            self.web3.eth.defaultAccount = buyer

            transactionInst = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode)
             
            tx_hash = transactionInst.constructor().transact()
    
            tx_receipt.append(self.web3.eth.waitForTransactionReceipt(tx_hash))

        return tx_receipt


    def transferFunds(self, tx_receipt, seller, amount):
        self.web3.eth.defaultAccount = tx_receipt['from']
        contract = self.web3.eth.contract(
            address = tx_receipt.contractAddress,
            abi = self.abi
            )

        # Wallet check.
        SC_res = False
        if self.web3.toWei(amount, 'ether') <= self.web3.eth.get_balance(tx_receipt['from']):
            tx_hash = contract.functions.deposit(seller).transact({'value':self.web3.toWei(amount, 'ether')})
            result = contract.functions.withdraw(seller).transact()
            SC_res= True
        else:
            print("Insufficient balance")
            SC_res= False
            
        return SC_res
        


    def updateMeter(self, tx_receipt, values):
        # This function stores and shows the smart meter data.
        # This function is actually never used.
        self.web3.eth.defaultAccount = tx_receipt['from']

        contract = self.web3.eth.contract(
            address = tx_receipt.contractAddress,
            abi = self.abi
            )

        tx_hash_up = contract.functions.input_meter(values).transact()
        check_tx_hash = contract.functions.get_meter().call()