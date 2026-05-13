"""
Solutions to module 4 - A calculator
Student: Hugo Lovmar
Mail: hlovmar@gmail.com
"""

"""
Note:
The program is only working for a very tiny set of operations.
You have to add and/or modify code in ALL functions as well as add some new functions.
Use the syntax charts when you write the functions!
However, the class SyntaxError is complete as well as handling in main
of SyntaxError and TokenError.
"""

import math
from tokenize import TokenError  
from MA4tokenizer import TokenizeWrapper



class SyntaxError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)

class EvaluationError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)


def fac(n):
    if n != int(n) or n < 0:
        raise EvaluationError(f"Argument to fac is {n}. Must be integer >= 0")
    return math.factorial(int(n))

def fib(n):
    if n != int(n) or n < 0:
        raise EvaluationError(f"Argument to fib is {n}. Must be integer >= 0")
    
    if n == 0:
        return 0

    a, b = 0, 1
    for _ in range(int(n-1)):
        a, b = b, a + b
    return b

def log(n):
    if n <= 0:
        raise EvaluationError(f"Argument to log is {n}. Must be a positive number")
    return math.log(n)

FUNCTIONS_1 = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'exp': math.exp,
    'log': log,
    'fac': fac,
    'fib': fib,
}

FUNCTIONS_N = {
    'max': max,
    'min': min,
    'sum': sum,
    'mean': lambda args: sum(args) / len(args)
}


def statement(wtok, variables):
    """ See syntax chart for statement"""
    result = assignment(wtok, variables)
    if not wtok.is_at_end():
        raise SyntaxError("Unexpected token")
    return result


def assignment(wtok, variables):
    """ See syntax chart for assignment"""
    result = expression(wtok, variables)
    while wtok.get_current() == '=':
        wtok.next()
        if not wtok.is_name():
            raise SyntaxError("Expected variable after '='")
        variables[wtok.get_current()] = result
        wtok.next()
    return result


def expression(wtok, variables):
    """ See syntax chart for expression"""
    result = term(wtok, variables)
    while wtok.get_current() == '+' or wtok.get_current() == '-':
        op = wtok.get_current()
        wtok.next()
        t = term(wtok, variables)
        result = result + t if op == '+' else result - t
    return result


def term(wtok, variables):
    """ See syntax chart for term"""
    result = factor(wtok, variables)
    while wtok.get_current() == '*' or wtok.get_current() == '/':
        op = wtok.get_current()
        wtok.next()
        f = factor(wtok, variables)
        if op == '*':
            result *= f
        else:
            if f == 0:
                raise EvaluationError("Division by zero")
            result /= f
    return result


def arglist(wtok, variables):
    if wtok.get_current() != '(':
        raise SyntaxError("Expected '(' after function name")
    
    wtok.next()
    args = [assignment(wtok, variables)]
    while wtok.get_current() == ',':
        wtok.next()
        args.append(assignment(wtok, variables))

    if wtok.get_current() != ')':
        raise SyntaxError("Expected ')' or ','")
    wtok.next()

    return args


def factor(wtok, variables):
    """ See syntax chart for factor"""
    if wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok, variables)
        if wtok.get_current() != ')':
            raise SyntaxError("Expected ')'")
        else:
            wtok.next()
            
    elif wtok.is_name():
        name = wtok.get_current()
        wtok.next()


        if name in FUNCTIONS_1:
            if wtok.get_current() != '(':
                raise SyntaxError("Expected '(' after function name")
            wtok.next()
            arg = assignment(wtok, variables)
            if wtok.get_current() != ')':
                raise SyntaxError("Expected ')' after function argument")
            wtok.next()
            result = FUNCTIONS_1[name](arg) 

        elif name in FUNCTIONS_N:
            result = FUNCTIONS_N[name](arglist(wtok, variables))
    

        elif name in variables:
            result = variables[name]
        else:
            raise EvaluationError(f"Undefined variable: {name}")
    

    elif wtok.is_number():
        result = float(wtok.get_current())
        wtok.next()

    elif wtok.get_current() == '-':
        wtok.next()
        result = -factor(wtok, variables)

    else:
        raise SyntaxError("Expected number or '(' but got " + wtok.get_current())  
    
    return result


         
def main():
    """
    Handles:
       the iteration over input lines,
       commands like 'quit' and 'vars' and
       raised exceptions.
    Starts with reading the init file
    """
    
    print("Numerical calculator")
    variables = {"ans": 0.0, "PI": math.pi, "E": math.e}

    # Note: The unit test file initiate variables in this way. If your implementation 
    # requires another initiation you have to update the test file accordingly.

    init_file = 'MA4init.txt'
    lines_from_file = ''
    try:
        with open(init_file, 'r') as file:
            lines_from_file = file.readlines()
            
    except FileNotFoundError:
        pass

    while True:
        if lines_from_file:
            line = lines_from_file.pop(0).strip()
            print('init  :', line)
        else:
            line = input('\nInput : ')

        if line == '' or line[0]=='#':
            continue

        wtok = TokenizeWrapper(line)

        if wtok.get_current() == 'quit':
            print('Bye')
            exit()
        
        elif wtok.get_current() == 'vars':
            for var, val in variables.items():
                print(f"{var} = {val}")

        elif wtok.is_at_end():
            continue

        else:
            try:
                result = statement(wtok, variables)
                variables['ans'] = result
                print('Result:', result)

            except SyntaxError as se:
                print("*** Syntax error: ", se)
                print(
                f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

            except EvaluationError as ee:
                print("*** Evaluation error: ", ee.arg)

            except TokenError as te:
                print('*** Syntax error: Unbalanced parentheses')
 


if __name__ == "__main__":
    main()
