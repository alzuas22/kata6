from datetime import date
from mi_cartera.models import Movement, MovementDAO
import pytest
import os
import csv

def test_create_movement(): 
    m=Movement("0001-01-01", "Sueldo", 1000, "EUR")
    assert m.date == date(1, 1, 1)
    assert m.abstract == "Sueldo"
    assert m.amount == 1000
    assert m.currency == "EUR"

def test_fails_if_date_greater_than_today():
    with pytest.raises(ValueError):
        m = Movement("9999-12-31", "concepto", 1000, "USD")

def test_change_date():
     m=Movement("0001-01-01", "Sueldo", 1000, "EUR")
     with pytest.raises(ValueError):
        m.date = "999-12-31"
        

def test_fails_if_amount_eq_zero():
    with pytest.raises(ValueError):
        m = Movement("2023-06-24", "Compra", 0, "USD")
 

def test_fails_if_currency_not_in_currencies():
    with pytest.raises(ValueError):
        m = Movement("2023-06-24", "Compra", 100, "INR")

def test_fails_if_amount_change_to_zero():
    m = Movement("2023-06-24", "Compra", 100, "USD")
    with pytest.raises(ValueError):
        m.amount = 0

def test_fails_if_amount_is_not_float():
    with pytest.raises(ValueError):
        m=Movement("0005-01-01", "Sueldo", "1000,25", "EUR")

    m = Movement("0005-01-01", "Sueldo", "1000.23", "EUR")
    assert m.amount == 1000.23

def test_fails_if_change_currency_not_in_currencies():
    m = Movement("2023-06-24", "Compra", 100, "USD")
    with pytest.raises(ValueError):
        m.currency = "INR"

def test_create_dao():
    path = "data_mentira.dat"
    if os.path.exists(path):
        os.remove(path)

    dao = MovementDAO(path)
    
    f= open(path, "r")
    cabecera = f.readline()

    assert cabecera == "date,abstract,amount,currency\n"

def test_insert_one_movement():
    path = "data_mentira.dat"
    if os.path.exists(path):
       os.remove(path)

    dao = MovementDAO(path)
    mvm = Movement("2023-01-01", "Un concepto", 1, "EUR")
    dao.insert(mvm)

    f= open(path, "r")
    reader=csv.reader(f, delimiter=",", quotechar='"')
    registros = list(reader)

    assert registros[0] == ["date", "abstract", "amount", "currency"]
    assert registros[1] == ["2023-01-01", "Un concepto", "1.0", "EUR"]
    

def test_all_movements():
    path = "data_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
    
    dao = MovementDAO(path)
    mvm1 = Movement("2023-01-01", "Un concepto1", 1, "EUR")
    dao.insert(mvm1)
    mvm2 = Movement("2023-01-02", "Un concepto2", 2, "EUR")
    dao.insert(mvm2)
    mvm3 = Movement("2023-01-03", "Un concepto3", 3, "EUR")
    dao.insert(mvm3)

    registers = dao.all() 
    assert registers[0] == mvm1
    assert registers[1] == mvm2
    assert registers[2] == mvm3

    