
# Non Terminate symbol
pgm, line, stmt, asgmnt, exp, tmp1, term, iff, cond, tmp2, printt, goto, stop = 'pgm', 'line', 'stmt', 'asgmnt', 'exp', 'tmp1', 'term', 'iff', 'cond', 'tmp2', 'printt', 'goto', 'stop' 

# Terminate symbol
ID, NUM, CONST, LINE_NUM, PLUS, MINUS, LESS, EQ, IF, PRINT, GOTO, STOP, EOF =  'ID', 'NUM', 'CONST', 'LINE_NUM', 'PLUS', 'MINUS', 'LESS', 'EQ', 'IF', 'PRINT', 'GOTO', 'STOP', 'EOF'
ter = [ID, NUM, CONST, LINE_NUM, PLUS, MINUS, LESS, EQ, IF, PRINT, GOTO, STOP, EOF]
alph = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26}

tokens = []
tp = 0

rules = {
        pgm:    [0,0,1,0,0,0,0,0,0,0,0,2],
        line:   [0,0,3,0,0,0,0,0,0,0,0,0],
        stmt:   [4,0,0,0,0,0,0,5,6,7,8,0],
        asgmnt: [9,0,0,0,0,0,0,0,0,0,0,0],
        exp:    [10,10,0,0,0,0,0,0,0,0,0,0],
        tmp1:   [0,0,0,11,12,0,0,0,0,0,0,13],
        term:   [14,15,0,0,0,0,0,0,0,0,0,0],
        iff:    [0,0,0,0,0,0,0,16,0,0,0,0],
        cond:   [17,17,0,0,0,0,0,0,0,0,0,0],
        tmp2:   [0,0,0,0,0,18,19,0,0,0,0,0],
        printt: [0,0,0,0,0,0,0,0,20,0,0,0],
        goto:   [0,0,0,0,0,0,0,0,0,21,0,0],
        stop:   [0,0,0,0,0,0,0,0,0,0,22,0],

    }

class Token(object):
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        # position on parse table
        self.pos = pos

  

def get_next_token() :
    global tp
    tp = tp + 1

def parser() :
    stack = []
    stack.append(EOF)
    stack.append(pgm)

    # loop unitil tos = EOF
    while stack[-1] != EOF :

        # if tos is terminate symbol
        if stack[-1] in ter :

            if stack[-1] == tokens[tp].type :
                # in case token is CONST and out of range {0,100}
                if stack[-1] == CONST :
                    if int(tokens[tp].value) > 100 :
                        return 0
                # in case token is LINE_NUM and out of range {0,1000}
                if stack[-1] == LINE_NUM :
                    if int(tokens[tp].value) > 1000 :
                        return 0
            elif (stack[-1] == LINE_NUM) & (tokens[tp].type == GOTO) :
                pass
            else :
                return 0 
            stack.pop()
            get_next_token()

        else :
            # look up for next rule

            # in case tp is point at EOF
            if(tp == len(tokens)) :
                if(stack[-1] == pgm) | (stack[-1] == tmp1) :
                    lkup = rules[stack[-1]][11]
                else :
                    return 0
            else : 
                lkup = rules[stack[-1]][tokens[tp].pos]

            if lkup == 0 : 
                return 0
            if lkup == 1 :
                stack.pop()
                stack.append(pgm)
                stack.append(line)
            if lkup == 2 :
                stack.pop()
            if lkup == 3 :
                stack.pop()
                stack.append(stmt)
                stack.append(LINE_NUM)
            if lkup == 4 : 
                stack.pop()
                stack.append(asgmnt)
            if lkup == 5 :
                stack.pop()
                stack.append(iff)
            if lkup == 6 :
                stack.pop()
                stack.append(printt)
            if lkup == 7 :
                stack.pop()
                stack.append(goto)
            if lkup == 8 :
                stack.pop()
                stack.append(stop)
            if lkup == 9 :
                stack.pop()
                stack.append(exp)
                stack.append(EQ)
                stack.append(ID)
            if lkup == 10 :
                stack.pop()
                stack.append(tmp1)
                stack.append(term)
            if lkup == 11 :
                stack.pop()
                stack.append(term)
                stack.append(PLUS)
            if lkup == 12 :
                stack.pop()
                stack.append(term)
                stack.append(MINUS)
            if lkup == 13 :
                stack.pop()
            if lkup == 14 :
                stack.pop()
                stack.append(ID)
            if lkup == 15 :
                stack.pop()
                stack.append(CONST)
            if lkup == 16 :
                stack.pop()
                stack.append(LINE_NUM)
                stack.append(cond)
                stack.append(IF)
            if lkup == 17 :
                stack.pop()
                stack.append(tmp2)
                stack.append(term)
            if lkup == 18 :
                stack.pop()
                stack.append(term)
                stack.append(LESS)
            if lkup == 19 :
                stack.pop()
                stack.append(term)
                stack.append(EQ)
            if lkup == 20 :
                stack.pop()
                stack.append(ID)
                stack.append(PRINT)
            if lkup == 21 :
                stack.pop()
                stack.append(LINE_NUM)
                stack.append(GOTO)
            if lkup == 22 :
                stack.pop()
                stack.append(STOP)

    return 1

def tokenizer(text) :
    l = text.split(' ')
    for idx,t in enumerate(l) :

        if (len(t) == 1) & t.isalpha() & t.isupper() :
            tokens.append(Token(ID, t, 0))
        elif t.isdigit() :
            if (idx == len(l)-1) & ((l[1] == IF) | (l[1] == GOTO)) :
                tokens.append(Token(GOTO, t, 2))
            elif idx == 0 :
                tokens.append(Token(LINE_NUM, t, 2))
            else :
                tokens.append(Token(CONST, t, 1))

        elif t == '+' :
            tokens.append(Token(PLUS, t, 3))
        elif t == '-' :
            tokens.append(Token(MINUS, t, 4))
        elif t == '<' :
            tokens.append(Token(LESS, t, 5))
        elif t == '=' :
            tokens.append(Token(EQ, t, 6))
        elif t == 'IF' :
            tokens.append(Token(IF, t, 7))
        elif t == 'PRINT' :
            tokens.append(Token(PRINT, t, 8))
        elif t == 'GOTO' :
            tokens.append(Token(GOTO, t, 9))
        elif t == 'STOP' :
            tokens.append(Token(STOP, t, 10))
        else : 
            return 0
        

def get_bcode() :
    l = []
    while(len(tokens) != 0) :
        t = tokens.pop()
        if t.type == LINE_NUM :
            l.insert(0, int(t.value))
            l.insert(0, 10)
        if t.type == ID :
            l.insert(0, alph[t.value])
            l.insert(0, 11)
        if t.type == CONST :
            l.insert(0, int(t.value))
            l.insert(0, 12)
        if t.type == IF :
            l.insert(0, 0)
            l.insert(0, 13)
        if t.type == GOTO :
            if (t.value != GOTO) :
                l.insert(0, int(t.value))
                l.insert(0, 14)
        if t.type == PRINT :
            l.insert(0, 0)
            l.insert(0, 15)
        if t.type == STOP :
            l.insert(0, 0)
            l.insert(0, 16)
        if t.type == PLUS :
            l.insert(0, 1)
            l.insert(0, 17)
        if t.type == MINUS :
            l.insert(0, 2)
            l.insert(0, 17)
        if t.type == LESS :
            l.insert(0, 3)
            l.insert(0, 17)
        if t.type == EQ :
            l.insert(0, 4)
            l.insert(0, 17)
    return l
        
        

def main() :
    global tp
    while True :
        tp = 0
        try :
            text = input('mild > ')
        except EOFError :
            break
        if not text :
            continue
        else :
            if (tokenizer(text) != 0) & (parser() != 0) :
                print(get_bcode())
            else :
                print("SyntaxError")
            
if __name__ == '__main__':
    main()