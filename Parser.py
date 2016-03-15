# Parse the word token from the substring
def parseWordToken(substring):
    token = ""
    for c in substring:
        if c.isalpha():
            token += c
        else:
            break
    return token

# Parse the number token from the substring
def parseNumberToken(substring):
    foundDecimal = False
    validAfterDecimal = True
    token = ""
    # Check the substring for digits and decimals
    for c in substring:
        if c.isdigit():
            token += c
            if foundDecimal:
                validAfterDecimal = True
        elif c == '.':
            # Check that there aren't multiple decimal points, and invalidate the token if so
            if foundDecimal:
                token = ""
                break
            foundDecimal = True
            validAfterDecimal = False
            token += "."
        # Break after the entirety of this number has been read
        else:
            break
            
    # If no digits follow the decimal, invalidate the number
    if not validAfterDecimal:
        token = ""
        
    # Return the number token or None if invalid
    if token != "":
        try:
            temp = float(token)
            return token
        except ValueError:
            return None
    else:
        return None

# Parse the substring for an operator and return its precedence and associativity
def parseOperator(substring):
    c = substring[0]
    output = None
    if c == '+':
        output = ['+', 0, "ltr"]
    elif c == '-':
        output = ['-', 0, "ltr"]
    elif c == '*':
        output = ['*', 1, "ltr"]
    elif c == '/':
        output = ['/', 1, "ltr"]
    elif c == '%':
        output = ['%', 1, "ltr"]
    elif c == '^':
        output = ['^', 2, "rtl"]
    return output

# Parse a mathematical expression using the Shunting-yard algorithm
def parseMathExpression(expr):
    prevTokenType = None
    outQueue = []
    midStack = []
    valid = True
    if len(expr) > 0:
        i = 0
        currToken = None
        while i < len(expr):
            print("___________________________________")
            print("Prev token: " + str(prevTokenType))
            print("midStack:")
            for se in midStack:
                print(str(se))

            print("outQueue:")
            for oe in outQueue:
                print(str(oe))
            print("Expr[i]: " + expr[i])
            
            # Skip whitespace
            if expr[i].isspace():
                i += 1
                continue
            # If token is a number, parse it
            elif expr[i].isdigit() or expr[i] == '.':
                currToken = parseNumberToken(expr[i:])
                # If invalid, break the loop
                if currToken is None:
                    valid = False
                    print("Parser.py: Error: Number token is invalid.")
                    break
                # Else increment i, and add the number to the queue
                outQueue.append(currToken)
                i += len(currToken)
                prevTokenType = "number"
            # If token is a word, parse it
            elif expr[i].isalpha():
                currToken = parseWordToken(expr[i:])
                # If invalid, break the loop
                if currToken == "":
                    valid = False
                    print("Parser.py: Error: Word token is invalid.")
                    break
                # Else increment i, and add the variable/ token to the queue/ stack
                if currToken == 'x' or currToken == 'y' or currToken == 'pi' or currToken == 'PI' or currToken == 'Pi' or currToken == 'e':
                    # If the previous token was an end parentheses, consider this multiplication
                    if prevTokenType == ')':
                        expr = expr[:i-1] + '*' + expr[i:]
                        prevTokenType = None
                    outQueue.append(currToken)
                    prevTokenType = "variable"
                else:
                    midStack.append(currToken)
                    prevTokenType = "procedure"
                i += len(currToken)
            # If token is a left parenthesis, add it to the operator stack
            elif expr[i] == '(' or expr[i] == '[':
                # If the previous token was an end parentheses, consider this multiplication
                if prevTokenType == ')' or prevTokenType == "variable":
                    print("Adding * to expression")
                    expr = expr[:i-1] + '*' + expr[i:]
                    prevTokenType = None
                else:
                    print("Adding ( to stack")
                    i += 1
                    midStack.append('(')
                    prevTokenType = "leftparen"
            # If token is a comma, pop operators off the stack until finding a left parenthesis
            elif expr[i] == ',':
                tempToken = ','
                i += 1
                # Loop over the operator stack until encountering the nearest left parenthesis
                while len(midStack) != 0 and tempToken != '(':
                    tempToken = midStack[-1]
                    if tempToken != '(':
                        midStack.pop()
                        print("Appending " + str(tempToken) + " to queue")
                        outQueue.append(tempToken)
                # Ensure proper use of parentheses
                if len(midStack) == 0:
                    valid = False
                    print("Parser.py: Error: Invalid use of ',' separator.")
                    break
            # If token is an end parenthesis, pop operators off the stack until consuming a left parenthesis
            elif expr[i] == ')' or expr[i] == ']':
                tempToken = ')'
                i += 1
                # Loop over the operator stack until encountering the nearest left parenthesis
                while len(midStack) != 0 and tempToken != '(':
                    tempToken = midStack[-1]
                    if tempToken != '(':
                        midStack.pop()
                        print("Appending " + str(tempToken) + " to queue")
                        outQueue.append(tempToken[0])
                # Ensure proper use of parentheses
                if len(midStack) == 0:
                    valid = False
                    print("Parser.py: Error: Mismatched parentheses. (extra close paren)")
                    break
                # tempToken must be an open parentheses, so pop it off the stack
                midStack.pop()
                prevTokenType = "rightparen"

                ###### TODO ######
                # Check if next operator on the stack is a function call
                
            
            # Else parse the expression for an operator
            else:
                currToken = parseOperator(expr[i:])
                # If no operator found, expression is invalid
                if currToken is None:
                    valid = False
                    print("Parser.py: Error: Invalid character or token '" + expr[i] + "' in expression.")
                    break
                # Else current operator is returned as a list-struct
                done = False
                unaryMinusRepeat = False
                while not done:
                    # Ensure that there are operators on the stack before trying to pop them
                    if len(midStack) < 1:
                        done = True
                        break
                    
                    opStackPrecedence = -1
                    # Ensure that the top of the operator stack is an operator, else assume lowest precedence
                    if len(midStack[-1]) > 1:
                        opStackPrecedence = midStack[-1][1]
                    else:
                        opStackPrecedence = -1
                    if currToken[2] == "ltr":
                        # If encountering a unary minus operator, insert replacement tokens into the expression
                        if currToken[0] == '-' and (prevTokenType == '(' or prevTokenType == '*' or prevTokenType is None):
                            expr = expr[:i-1] + "(0-1)*" + expr[i+1:]
                            unaryMinusRepeat = True
                            prevTokenType = "unaryOperatorRepeat"
                            done = True
                            break
                        if currToken[1] <= opStackPrecedence:
                            outQueue.append(midStack[-1][0])
                            midStack.pop()
                            print("operator is ltr; popping top of op stack")
                        else:
                            print("operator is ltr; precedence > top of stack operator")
                            done = True
                    else:
                        if currToken[1] < opStackPrecedence:
                            outQueue.append(midStack[-1][0])
                            midStack.pop()
                            print("operator is rtl; popping top of op stack")
                        else:
                            print("operator is rtl; precedence >= top of stack operator")
                            done = True

                # If a unary minus was encountered, read the replaced token
                if unaryMinusRepeat:
                    continue
                
                # After moving all sequential operators with > / >= precedence off the stack, push the new one
                midStack.append(currToken)
                prevTokenType = currToken[0]
                i += 1

        # After iterating through the entire expression, pop all operators off the stack
        while len(midStack) > 0:
            tempOp = midStack.pop()
            # Check for mismatched parentheses
            if tempOp == '(' or tempOp == ')':
                valid = False
                print("Parser.py: Error: Mismatched parentheses")
                break
            outQueue.append(tempOp)
        
    else:
        valid = False

    # If the queue is valid, reformat it, and replace operator list-structs with just the operator
    if valid:
        # Remove all traces of operator precedence or associativity from the RPN output queue
        """
        for i in range(0, len(outQueue)):
#            print("outQueue[i] = " + str(outQueue[i]) + ",   len(outQueue[i]) = " + str(len(outQueue[i])))
            if len(outQueue[i]) > 1:
                #try:
                #    test = int(outQueue[1])
                outQueue[i] = outQueue[i][0]
                #except ValueError:
                #    pass
        """
        return outQueue
    else:
        print("Parser.py: Error: Invalid expression.")
        return None


