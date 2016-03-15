import math

# Return whether or not the queue of RPN instructions produced a valid result
def checkValid(Q):
    valid = True
    stack = []

    
    print("Printing instruction queue:")
    for e in Q:
        print(str(e))
    

    # Iterate over the queue, treating each element as either an operator or a value to push
    for elem in Q:
        # One push values
        if elem == "x" or elem == "y" or elem == "pi" or elem == "PI" or elem == "Pi" or elem == "e":
            stack.append(0)
        # One push value (constant)
        if elem[0].isdigit() or elem[0] == '.':
            try:
                stack.append(float(elem))
            except ValueError:
                valid = False
                print("Calculator.py: Error: Expected a valid number token.")
                break
        # One pop, one push operators
        elif elem == "sin" or elem == "cos" or elem == "tan":
            if len(stack) < 1:
                valid = False
                break
        # Two pop, one push operators
        elif elem == "+" or elem == "-" or elem == "*" or elem == "/" or elem == "^" or elem == "%"  or elem == "max" or elem == "min":
            if len(stack) < 2:
                valid = False
                break
            stack.pop()
    
    # If the stack doesn't have exactly one element after evaluating, invalidate it
    if stack is None:
        print("Calculator.py: Error: Stack is empty")
        valid = False
    elif len(stack) != 1:
        print("Calculator.py: Error: Stack length is not 1")
        valid = False

    return valid

# Evaluate a queue of instructions by pushing instructions onto an RPN stack, passing x and y as variables
def evaluate(Q, x, y):
    stack = []
    
    for elem in Q:
        if elem == "x":
            stack.append(x)
        elif elem == "y":
            stack.append(y)
        elif elem[0].isdigit() or elem[0] == '.':
            stack.append(float(elem))
        elif elem == "pi" or elem == "PI" or elem == "Pi":
            stack.append(math.pi)
        elif elem == "e":
            stack.append(math.e)
        elif elem == "sin":
            temp = stack.pop()
            stack.append(math.sin(temp))
        elif elem == "cos":
            temp = stack.pop()
            stack.append(math.cos(temp))
        elif elem == "tan":
            temp = stack.pop()
            stack.append(math.tan(temp))
        elif elem == "max":
            temp2 = stack.pop()
            temp1 = stack.pop()
            stack.append(max(temp1, temp2))
        elif elem == "min":
            temp2 = stack.pop()
            temp1 = stack.pop()
            stack.append(min(temp1, temp2))
        elif elem == "+":
            temp2 = stack.pop()
            temp1 = stack.pop()
            stack.append(temp1 + temp2)
        elif elem == "-":
            temp2 = stack.pop()
            temp1 = stack.pop()
            stack.append(temp1 - temp2)
        elif elem == "*":
            temp2 = stack.pop()
            temp1 = stack.pop()
            stack.append(temp1 * temp2)
        elif elem == "/":
            temp2 = stack.pop()
            temp1 = stack.pop()
            stack.append(temp1 / temp2)
        elif elem == "^":
            temp2 = stack.pop()
            temp1 = stack.pop()
            stack.append(math.pow(temp1, temp2))
        elif elem == "%":
            temp2 = stack.pop()
            temp1 = stack.pop()
            stack.append(math.fmod(temp1, temp2))

    # Ensure that there is exactly one value left on the stack
    if(len(stack) != 1):
        print("Calculator.py: Error: Equation is invalid")
        return None

    # Return the last value on the stack
    return stack[0]
