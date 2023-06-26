from datetime import date
import csv

CURRENCIES = ("EUR", "USD")

class Movement:
    def __init__(self, input_date, abstract, amount, currency):
        self.date = input_date
        if self._date > date.today():
            raise ValueError("date must be today or lower")
        self.abstract = abstract
        self.amount =  amount
        self.currency = currency

    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, value):
        self._date = date.fromisoformat(value)
        if self._date > date.today():
            raise ValueError("date must be today or lower")
        
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value == 0:
            raise ValueError("amount cannot be zero")
        self._amount = value 

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        if value not in CURRENCIES:
            raise ValueError("Invalid currency.")
        self._currency = value
        
    
# Encapsular lectura y escritura en el csv
class MovementDAO:
    #path (abre y cierra dicho fichero), all devuelve lista de movimientos, insert del movimiento
    def __init__(self, file_path):
        self.path = file_path
        f=open(file_path, "w")
        f.write("date,abstract,amount,currency\n")

    def insert(self, movement):
        f = open(self.path, "a", newline="")
        writer = csv.writer(f, delimiter=",", quotechar='"')
        writer.writerow([movement.date, movement.abstract, movement.amount, movement.currency])