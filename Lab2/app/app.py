from crypt import methods
from pickle import FALSE
from flask import Flask, render_template, request, make_response
import operator as op

app = Flask(__name__)
application = app

OPERATIONS = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv}


@app.route('/')
def index():
    url = request.url
    return render_template('index.html')


@app.route('/args')
def args():
    return render_template('args.html')


@app.route('/headers')
def headers():
    return render_template('headers.html')


@app.route('/cookies')
def cookies():
    response = make_response(render_template('cookies.html'))
    if request.cookies.get('name') is None:
        response.set_cookie('name', 'qq')
    else:
        response.set_cookie('name', 'qq', expires=0)
    return response


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    result = None
    error_msg = None
    if request.method == 'POST':
        try:
            operand1 = float(request.form.get('operand1'))
            operand2 = float(request.form.get('operand2'))
            operation = request.form.get('operation')
            result = OPERATIONS[operation](operand1, operand2)
        except ValueError:
            error_msg = 'Нужно вводить только цифры'
        except ZeroDivisionError:
            error_msg = 'На ноль делить нельзя'

    return render_template('calc.html', operations=OPERATIONS, result=result, error_msg=error_msg)


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    isValid = False
    output = ''
    if request.method == 'POST':
        isValid, output = isPhoneValid(request.form.get('phone'))

    return render_template('phone.html', output=output, isValid = isValid)


def isPhoneValid(phone: str):
    isValid = True
    errorCode = ''
    allowedSymbols = '()-+.0123456789 '
    numbers = '0123456789'
    numCount = 0
    phoneNumbers = []
    startsWith7or8 = False

    for i in range(len(phone)):
        if allowedSymbols.find(phone[i]) == -1:
            isValid = False
            errorCode = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
            return isValid, errorCode

        if phone.startswith('+7'):
            startsWith7or8 = True
            if i == 0:
                numCount += 1
                continue
            if i == 1:
                continue

        if phone.startswith('8'): 
            startsWith7or8 = True
            if i == 0: 
                numCount += 1
                continue

        if numbers.find(phone[i]) != -1:
            numCount += 1
            phoneNumbers.append(phone[i])

    if (numCount == 10 and not startsWith7or8) or numCount == 11:
        isValid = True
        outputPhone = f'8-{phoneNumbers[0:3]}-{phoneNumbers[3]}{phoneNumbers[4]}{phoneNumbers[5]}-{phoneNumbers[6]}{phoneNumbers[7]}-{phoneNumbers[8]}{phoneNumbers[9]}'
        return isValid, outputPhone

    isValid = False
    errorCode = 'Недопустимый ввод. Неверное количество цифр.'
    return isValid, errorCode

#isPhoneValid("8(123)4567590")