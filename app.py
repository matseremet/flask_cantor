from flask import Flask, url_for, request, session, redirect, render_template, flash

app = Flask(__name__)

app.config['SECRET_KEY'] = '12345'

class Currency:
    def __init__(self, code, name, flag):
        self.code = code
        self.name = name
        self.flag = flag
        
    def __repr__(self):
        return '<Currency {}>'.format(self.code)
    
class CantorOffer:
    def __init__(self):
        self.currencies = []
        self.denied_codes = []
        
    def load_offer(self):
        self.currencies.append(Currency('USD', 'Dollar', 'USA_flag.png'))
        self.currencies.append(Currency('EUR', 'Euro', 'EUROPE_flag.png'))
        self.currencies.append(Currency('JPY', 'Yen', 'JAPAN_flag.png'))
        self.currencies.append(Currency('GBP', 'Pound', 'UK_flag.png'))
        self.denied_codes.append('USD')
        
    def get_by_code(self, code):
        for currency in self.currencies:
            if currency.code == code:
                return currency
        return Currency('unknown', 'unknown', 'PIRATE_flag.png')
        

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exchange', methods=['GET', 'POST'])
def exchange():
    
    offer = CantorOffer()
    offer.load_offer()
    
    if request.method == 'GET':
        return render_template('exchange.html', offer=offer)
    else:
        currency = 'EUR'
        if 'currency' in request.form:
            currency = request.form['currency']
            
        if currency in offer.denied_codes:
            flash('The currency {} cannot be accepted'.format(currency))
        elif offer.get_by_code(currency) == 'unknown':
            flash('The selected currency is unknown and cannot be accepted')
        else:
            flash('Request to exchange {} was accepted'.format(currency))
            
        amount = '100'
        if 'amount' in request.form:
            amount = request.form['amount']
            
        return render_template('exchange_result.html', currency=currency, amount=amount, currency_info=offer.get_by_code(currency))
    
if __name__ == '__main__':
    app.run(debug=True)