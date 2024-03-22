from pair import *

from operator import add, sub, mul, truediv


def tokenize(expression):
    """ Takes a string and returns a list where each item
    in the list is a parenthesis, one of the four operators (/, *, -, +),
    or a number literal.
    >>> tokenize("(+ 3 2)")
    ['(', '+', '3', '2', ')']
    >>> tokenize("(- 9 3 3)")
    ['(', '-', '9', '3', '3', ')']
    >>> tokenize("(+ 10 100)")
    ['(', '+', '10', '100', ')']
    >>> tokenize("(+ 5.5 10.5)")
    ['(', '+', '5.5', '10.5', ')']
    >>> expr = "(* (- 8 4) 4)"
    >>> tokenize(expr)
    ['(', '*', '(', '-', '8', '4', ')', '4', ')']
    >>> expr = "(* (- 6 8) (/ 18 3) (+ 10 1 2))"
    >>> tokenize(expr)
    ['(', '*', '(', '-', '6', '8', ')', '(', '/', '18', '3', ')', '(', '+', '10', '1', '2', ')', ')']
    """
    # Write your code here

    split_string = expression.split()  # * List obj
    final_list = []

    for group in split_string:
        add_to_end = []
        add_to_beginning = []

        for char in group:
            if char == "(":
                add_to_beginning.append("(")
            if char == ")":
                add_to_end.append(")")

        group_without_paranthesis = (group.replace("(", "")).replace(")", "")

        for char in add_to_beginning:
            final_list.append(char)
        
        final_list.append(group_without_paranthesis)

        for char in add_to_end:
            final_list.append(char)

    for group in final_list:
        if group == "":
            final_list.remove(group)

    return final_list


def parse_tokens(tokens, index):
    """ Takes a list of tokens and an index and converts the tokens to a Pair list

    >>> parse_tokens(['(', '+', '1', '1', ')'], 0)
    (Pair('+', Pair(1, Pair(1, nil))), 5)
    >>> parse_tokens(['(', '*', '(', '-', '8', '4', ')', '4', ')'], 0)
    (Pair('*', Pair(Pair('-', Pair(8, Pair(4, nil))), Pair(4, nil))), 9)
    """
    # Write your code here
    operator = ""
    
    if tokens[index] == ')':
        return nil, index+1
    
    if tokens[index] == '(':
        operator = tokens[index+1]
        
        if index != 0:
            parse_return_value = parse_tokens(tokens, index+2)
            
            new_pair_list = parse_return_value[0]
            index = parse_return_value[1]
            
            operator = Pair(operator, new_pair_list)
            
        if index == 0:
            index += 2
            
        parse_return_value = parse_tokens(tokens, index)
        
        new_pair_list = parse_return_value[0]
        index = parse_return_value[1]
        
        return Pair(operator, new_pair_list), index
    
    try:
        numberfied_token = 0
        
        if '.' in tokens[index]:
            numberfied_token = float(tokens[index])
            
        if not '.' in tokens[index]:
            numberfied_token = int(tokens[index])
            
        parse_return_value = parse_tokens(tokens, index+1)
        
        new_pair_list = parse_return_value[0]
        index = parse_return_value[1]
        
        return Pair(numberfied_token, new_pair_list), index

    except TypeError:
        
        raise TypeError("Conversion to integer/float failed.")
    
    except ValueError:
        
        print("Value is not an integer or decimal point number.")
        

def parse(tokens):
    
    return parse_tokens(tokens, 0)[0]


def reduce(func, operands, initial):
    
    totaled_value = 0
    
    while operands is not nil:
        totaled_value += func(initial, operands.first)
        operands = operands.rest
        
    return totaled_value


def apply(operator, operands):
    
    if operator not in ["+", "-", "*", "/"]:
        raise TypeError("Operator invalid.")
    
    if operator == "+":
        return reduce(add, operands, 0)
        
    elif operator == "*":
        return reduce(mul, operands, 1)
        
    elif operator == "/":
        initial = operands.first
        operands = operands.rest
        return reduce(truediv, operands, initial)
        
    elif operator == "-":
        initial = operands.first
        operands = operands.rest
        return reduce(sub, operands, initial)
    

def eval(expression):
    
    if isinstance(expression, int) or isinstance(expression, float):
        
        return expression
    
    if isinstance(expression, Pair):
        
        if isinstance(expression.first, Pair):
            
            evaluated_first = eval(expression.first)
            
            evaluated_rest = expression.rest.map(eval)
            
            return Pair(evaluated_first, evaluated_rest)
    
        if expression.first in ["+", "-", "*", "/"]:
            
            evaluated_rest = expression.rest.map(eval)
            
            applied_result = apply(expression.first, evaluated_rest)
            
            return applied_result
            
    if not isinstance(expression, int) or not isinstance(expression, float) or not isinstance(expression, Pair):
        
        raise TypeError("Expression is not an int, float, or Pair object.")
    
    
run = True
if __name__ == "__main__":
    
    print("Welcome to the CS 111 Calculator Interpreter.")
    
    while run:
        user_input = input("calc >> ")
    
        tokenized_input = tokenize(user_input)
        
        if user_input == "exit":
            
            run = False
            
            continue
    
        try:
            pair_list = parse(tokenized_input)
            
            results = eval(pair_list)
        
            print(results)
        
        except:
            
            print("Exception caught.")

    print("Goodbye!")