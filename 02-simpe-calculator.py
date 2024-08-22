# sexpr은 괄호로 묶은 중첩된 리스트로 구성된 데이터 구조이거나 원자라고 하는 분할할 수 없는 값이다.
# 예룰 들면 다음과 같다.
# 원자
# a 123 
# 리스트
# (a) (a b c) (a d)
# 중첩된 리스트
# ((a) (b) (c)) ((a b) (c d) (e f))



def parse_expr(s: str, idx:int):
    idx = skip_spaces(s, idx)
    if s[idx] == '(':
        # 리스트일 때
        idx += 1
        l = []
        while True:
            idx = skip_spaces(s, idx)
            if idx >= len(s):
                raise Exception('unbalanced parenthesis')
            if s[idx] == ')':
                idx += 1
                break
            
            idx, v = parse_expr(s, idx)
            l.append(v)
        return idx, l
    elif s[idx] == ')':
        raise Exception('bas parenthesis')
    else:
        # 원자일 때 
        start = idx
        # 원자를 읽어서 idx를 증가시키고 원자를 반환
        # 인덱스가 문자열의 길이보다 작고, 공백이 아니고, 괄호가 아닐 때까지 인덱스를 증가시킨다.
        while idx < len(s) and not s[idx].isspace() and s[idx] not in '()':
            idx += 1
        if idx == start:
            raise Exception('empty program')
        return idx, parse_atom(s[start:idx])
    
    
def skip_spaces(s: str, idx: int):
    while idx < len(s) and s[idx].isspace():
        idx += 1
    return idx

# bool, number, string or a symbol
def parse_atom(s: str):
   # TODO: acutal implement this
   import json
   try:
       return ['val', json.loads(s)]
   except json.JSONDecodeError:
    return s


def pl_parse(s: str):
    idx, node = parse_expr(s, 0)
    idx = skip_spaces(s, idx)
    if idx < len(s):
        raise ValueError('trailing characters')
    return node 



def pl_eval(node):
    if len(node) == 0:
        raise ValueError('empty list')
    
    #bool, number, string and etc
    if len(node) == 2 and node[0] == 'val':
        return node[1]
    
    # 이항 연산자
    import operator
    binops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        'eq': operator.eq,
        'ne': operator.ne,
        'lt': operator.lt,
        'le': operator.le,
        'gt': operator.gt,
        'ge': operator.ge,
        'and': operator.and_,
        'or': operator.or_,
    }
    if len(node) == 3 and node[0] in binops:
        op = binops[node[0]]
        return op(pl_eval(node[1]), pl_eval(node[2]))
    
    # 단항 연산자
    unops = {
        'not': operator.not_,
        '-': operator.neg,
    }
    
    if len(node) == 2 and node[0] in unops:
        op = unops[node[0]]
        return op(pl_eval(node[1]))
    
    # 조건부
    if len(node) == 4 and node[0] == '?':
        # 구조 분해 할당 
        _, cond, yes, no = node
        if pl_eval(cond):
            return pl_eval(yes)
        else:
            return pl_eval(no)
        
    
    # 출력
    if node[0] == 'print':
        # *은 unpacking 연산자 
        # print(*[1, 2, 3]) -> print(1, 2, 3)
        return print(*[pl_eval(e) for e in node[1:]])
    
    raise ValueError('unknown expression')


def test_eval():
    def f(s):
        return pl_eval(pl_parse(s))
    assert f('1') == 1
    assert f('(+ 1 2)') == 3
    assert f('(+ 1 (* 2 3))') == 7
    assert f('(- 1 (* 2 3))') == -5
    assert f('(?(lt 1 3) "yes" "no")') == "yes"
    assert f('(print 1 2 3)') is None
    
    

test_eval()
    
    