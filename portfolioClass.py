import cmc

class Portfolio:

    def __init__(self, account, portfolio):
        self.account = account
        if type(portfolio) != dict: raise TypeError()
        self.portfolio = {key:float(value) for key, value in portfolio.items()}
        self.dataLoaded = False

    # Clean assets so that accounts with no amount of cryptocurrency (0) are removed
    def cleanAssets(self):
        new = {}

        for asset, value in self.portfolio.items():
            if value != 0:
                new[asset] = value

        self.portfolio = new

    #
    def loadNames(self):
        cmc.loadNames(self.portfolio)

    # Loads real-time prices of coins into given portfolio
    def loadPrices(self):
        prices = cmc.getPrices(self.portfolio)

        i = 0
        for key, value in self.portfolio.items():
            value.append(prices[i])
            i += 1

    # Loads current balance of coins into given portfolio using real-time prices
    def loadBalance(self):
        for key, value in self.portfolio.items():
            value[2] = str(float(value[1]) * float(value[2]))

        self.loadPrices()


    # Calculates total balance of given portfolio
    def totalBalance(self):
        return "$" + str(sum([float(value[2]) for key, value in self.portfolio.items()])) + " USD"

    def loadData(self):
        if self.dataLoaded: return

        self.cleanAssets()
        self.loadNames()
        self.loadPrices()
        self.loadBalance()
        self.sortPortfolio()
        self.dataLoaded = True


    # Requires loadData() to be called. 
    def sortPortfolio(self):
        sortedPortfolio = sorted(self.portfolio.items(), key = lambda coin: float(coin[1][2]), reverse = True)
        sortedPortfolio = dict(sortedPortfolio)
        
        self.portfolio = sortedPortfolio
        
    # Prints assets and all details of portfolio into terminal 
    def showAssets(self):

        if not self.dataLoaded: self.loadData()

        print("\nShowing your assets in " + "\033[4m" + self.account + "\033[0m" + ":\n")

        # Symbol | Name | Amount | Balance | Real-Time Price
        header = f"{'Symbol':<5} | {'Name':<25} | {'Amount':<12} | {'Balance':<11} | {'Real-Time Price':<15}"
        print(header)
        print('-'*90)
        for key, value in self.portfolio.items():
            symbol = key
            name = value[0]
            amount = round(float(value[1]), 5)
            balance = round(float(value[2]), 4)
            price = round(float(value[3]), 4)
            print(f"{symbol:<6} | {name:<25} | {amount:<12} | ${balance:<10} | ${price:<10}")
        print()
        print("Total Balance in " + '\033[4m' + self.account + "\033[0m" + ": " + self.totalBalance() + "\n")


from collections import defaultdict

# Uses OOP Principles like Inheritance and Composition 
class MasterPortfolio(Portfolio):
    
    def __init__(self, accounts):
        if type(accounts) != list or type(accounts[0]) != Portfolio: raise TypeError()

        self.accounts = accounts

        self.exchangeData = defaultdict(list)
        self.balances = defaultdict(float)
        self.generateBalances()

        self.portfolio = dict(self.balances)
        super().__init__("Master", self.portfolio)

    def generateBalances(self):
        for account in self.accounts:
            accountPortfolio = account.portfolio
            for coin in accountPortfolio:
                self.balances[coin] += accountPortfolio[coin]

    def generateExchangeData(self):
        for account in self.accounts:
            portfolio = account.portfolio
            exchange = account.account
            for coin in portfolio:
                self.exchangeData[coin].append(exchange)

    def loadData(self):
        if self.dataLoaded: return

        self.generateExchangeData()
        super().loadData()

    # Overrided from 
    def showAssets(self):
        if not self.dataLoaded: self.loadData()

        print("\nShowing your \033[4mtotal\033[0m assets:\n")

        # Symbol | Name | Amount | Balance | Real-Time Price |  Exchanges with Asset
        header = f"{'Symbol':<5} | {'Name':<25} | {'Amount':<12} | {'Balance':<11} | {'Real-Time Price':<15} | {'Exchanges with Asset':<20}"
        print(header)
        print('-'*110)
        for key, value in self.portfolio.items():
            symbol = key
            name = value[0]
            amount = round(float(value[1]), 5)
            balance = round(float(value[2]), 4)
            price = round(float(value[3]), 4)
            print(f"{symbol:<6} | {name:<25} | {amount:<12} | ${balance:<10} | ${price:<14} | {str(self.exchangeData[key])}")
        print()
        print(f"Total Balance: {self.totalBalance()}")
        for account in self.accounts:
            account.loadData()
            print(f"{account.account}: {account.totalBalance()}")
        print()

    def pandasToExcel(self):
        pass