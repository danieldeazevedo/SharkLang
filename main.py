import re
import math
from enum import Enum
from typing import Any, List, Dict, Optional
from statistics import mean, median, mode, stdev, variance

# ============= LEXER =============
class TokenType(Enum):
    # Literals
    INT = "INT"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOL = "BOOL"

    # Keywords
    VAR = "VAR"
    FOR = "FOR"
    IN = "IN"
    WHILE = "WHILE"
    QUESTION = "QUESTION"
    OTHERWISE = "OTHERWISE"
    RETURN = "RETURN"

    # Types
    TYPE_INT = "TYPE_INT"
    TYPE_FLOAT = "TYPE_FLOAT"
    TYPE_STRING = "TYPE_STRING"
    TYPE_BOOL = "TYPE_BOOL"
    TYPE_ARRAY = "TYPE_ARRAY"

    # Identifiers
    IDENT = "IDENT"

    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULT = "MULT"
    DIV = "DIV"
    MOD = "MOD"
    POWER = "POWER"

    # Comparison
    EQ = "EQ"
    NEQ = "NEQ"
    LT = "LT"
    GT = "GT"
    LTE = "LTE"
    GTE = "GTE"

    # Logical
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COMMA = "COMMA"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    ARROW = "ARROW"
    ASSIGN = "ASSIGN"
    RANGE = "RANGE"

    EOF = "EOF"

class Token:
    def __init__(self, type: TokenType, value: Any, line: int, col: int):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []

        self.keywords = {
            'var': TokenType.VAR,
            'for': TokenType.FOR,
            'in': TokenType.IN,
            'while': TokenType.WHILE,
            'otherwise': TokenType.OTHERWISE,
            'return': TokenType.RETURN,
            'true': TokenType.BOOL,
            'false': TokenType.BOOL,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
            # Types
            'int': TokenType.TYPE_INT,
            'float': TokenType.TYPE_FLOAT,
            'string': TokenType.TYPE_STRING,
            'bool': TokenType.TYPE_BOOL,
            'array': TokenType.TYPE_ARRAY,
        }

    def current_char(self):
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def peek(self, offset=1):
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]

    def advance(self):
        if self.pos < len(self.source) and self.source[self.pos] == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        self.pos += 1

    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\n\r':
            self.advance()

    def skip_comment(self):
        if self.current_char() == '/' and self.peek() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()

    def read_number(self):
        num_str = ''
        has_dot = False

        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.current_char()
            self.advance()

        if has_dot:
            return Token(TokenType.FLOAT, float(num_str), self.line, self.col)
        return Token(TokenType.INT, int(num_str), self.line, self.col)

    def read_string(self):
        quote = self.current_char()
        self.advance()
        string = ''

        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    string += '\n'
                elif self.current_char() == 't':
                    string += '\t'
                else:
                    string += self.current_char()
            else:
                string += self.current_char()
            self.advance()

        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, string, self.line, self.col)

    def read_identifier(self):
        ident = ''
        while self.current_char() and (self.current_char().isalnum() or self.current_char() in '_μσΣ'):
            ident += self.current_char()
            self.advance()

        token_type = self.keywords.get(ident, TokenType.IDENT)

        if token_type == TokenType.BOOL:
            value = ident == 'true'
            return Token(TokenType.BOOL, value, self.line, self.col)

        return Token(token_type, ident, self.line, self.col)

    def tokenize(self):
        while self.pos < len(self.source):
            self.skip_whitespace()

            if not self.current_char():
                break

            # Comments
            if self.current_char() == '/' and self.peek() == '/':
                self.skip_comment()
                continue

            # Numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue

            # Strings
            if self.current_char() in '"\'':
                self.tokens.append(self.read_string())
                continue

            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() in '_μσΣ':
                self.tokens.append(self.read_identifier())
                continue

            # Operators and delimiters
            char = self.current_char()
            line, col = self.line, self.col

            if char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', line, col))
            elif char == '-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, '-', line, col))
            elif char == '*':
                self.advance()
                if self.current_char() == '*':
                    self.advance()
                    self.tokens.append(Token(TokenType.POWER, '**', line, col))
                else:
                    self.tokens.append(Token(TokenType.MULT, '*', line, col))
            elif char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIV, '/', line, col))
            elif char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.MOD, '%', line, col))
            elif char == '=':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.EQ, '==', line, col))
                elif self.current_char() == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.ARROW, '=>', line, col))
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', line, col))
            elif char == '!':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.NEQ, '!=', line, col))
            elif char == '<':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.LTE, '<=', line, col))
                else:
                    self.tokens.append(Token(TokenType.LT, '<', line, col))
            elif char == '>':
                self.advance()
                if self.current_char() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.GTE, '>=', line, col))
                else:
                    self.tokens.append(Token(TokenType.GT, '>', line, col))
            elif char == '?':
                self.advance()
                self.tokens.append(Token(TokenType.QUESTION, '?', line, col))
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', line, col))
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', line, col))
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', line, col))
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', line, col))
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', line, col))
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', line, col))
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', line, col))
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', line, col))
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', line, col))
            elif char == '.':
                self.advance()
                if self.current_char() == '.':
                    self.advance()
                    self.tokens.append(Token(TokenType.RANGE, '..', line, col))
            else:
                raise SyntaxError(f"Unexpected character '{char}' at line {line}, col {col}")

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return self.tokens

# ============= AST NODES =============
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarDecl(ASTNode):
    def __init__(self, name, type_annotation, value):
        self.name = name
        self.type_annotation = type_annotation
        self.value = value

class FuncDecl(ASTNode):
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body

class IfStmt(ASTNode):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class ForStmt(ASTNode):
    def __init__(self, var_name, iterable, body):
        self.var_name = var_name
        self.iterable = iterable
        self.body = body

class WhileStmt(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ReturnStmt(ASTNode):
    def __init__(self, value):
        self.value = value

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class FuncCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ArrayLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class RangeExpr(ASTNode):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

# ============= PARSER =============
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]

    def peek(self, offset=1):
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]

    def advance(self):
        self.pos += 1

    def expect(self, token_type):
        if self.current_token().type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token().type}")
        token = self.current_token()
        self.advance()
        return token

    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    def parse_statement(self):
        token = self.current_token()

        if token.type == TokenType.VAR:
            return self.parse_var_decl()
        elif token.type == TokenType.QUESTION:
            return self.parse_if_stmt()
        elif token.type == TokenType.FOR:
            return self.parse_for_stmt()
        elif token.type == TokenType.WHILE:
            return self.parse_while_stmt()
        elif token.type == TokenType.RETURN:
            return self.parse_return_stmt()
        elif token.type == TokenType.IDENT:
            # Check if it's a function declaration or assignment
            if self.peek().type == TokenType.LPAREN:
                # Check if it's a function declaration (has => after params)
                saved_pos = self.pos
                self.advance()  # Skip name
                self.skip_params()
                if self.current_token().type == TokenType.ARROW:
                    self.pos = saved_pos
                    return self.parse_func_decl()
                else:
                    self.pos = saved_pos
                    return self.parse_expression_stmt()
            elif self.peek().type == TokenType.ASSIGN:
                return self.parse_assignment()
            else:
                return self.parse_expression_stmt()
        else:
            return self.parse_expression_stmt()

    def skip_params(self):
        self.expect(TokenType.LPAREN)
        while self.current_token().type != TokenType.RPAREN:
            self.advance()
        self.expect(TokenType.RPAREN)

    def parse_var_decl(self):
        self.expect(TokenType.VAR)
        name = self.expect(TokenType.IDENT).value

        type_annotation = None
        if self.current_token().type == TokenType.COLON:
            self.advance()
            type_annotation = self.current_token().value
            self.advance()

        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        return VarDecl(name, type_annotation, value)

    def parse_func_decl(self):
        name = self.expect(TokenType.IDENT).value

        self.expect(TokenType.LPAREN)
        params = []
        while self.current_token().type != TokenType.RPAREN:
            param_name = self.expect(TokenType.IDENT).value
            param_type = None
            if self.current_token().type == TokenType.COLON:
                self.advance()
                param_type = self.current_token().value
                self.advance()
            params.append((param_name, param_type))

            if self.current_token().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RPAREN)

        return_type = None
        if self.current_token().type == TokenType.COLON:
            self.advance()
            return_type = self.current_token().value
            self.advance()

        self.expect(TokenType.ARROW)

        # Check if it's a single expression or block
        if self.current_token().type == TokenType.LBRACE:
            body = self.parse_block()
        else:
            # Single expression function
            expr = self.parse_expression()
            self.expect(TokenType.SEMICOLON)
            body = [ReturnStmt(expr)]

        return FuncDecl(name, params, return_type, body)

    def parse_if_stmt(self):
        self.expect(TokenType.QUESTION)
        condition = self.parse_expression()
        then_block = self.parse_block()

        else_block = None
        if self.current_token().type == TokenType.OTHERWISE:
            self.advance()
            else_block = self.parse_block()

        return IfStmt(condition, then_block, else_block)

    def parse_for_stmt(self):
        self.expect(TokenType.FOR)
        var_name = self.expect(TokenType.IDENT).value
        self.expect(TokenType.IN)
        iterable = self.parse_expression()
        body = self.parse_block()

        return ForStmt(var_name, iterable, body)

    def parse_while_stmt(self):
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        body = self.parse_block()

        return WhileStmt(condition, body)

    def parse_return_stmt(self):
        self.expect(TokenType.RETURN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStmt(value)

    def parse_assignment(self):
        name = self.expect(TokenType.IDENT).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return Assignment(name, value)

    def parse_expression_stmt(self):
        expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return expr

    def parse_block(self):
        self.expect(TokenType.LBRACE)
        statements = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.expect(TokenType.RBRACE)
        return statements

    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        left = self.parse_logical_and()

        while self.current_token().type == TokenType.OR:
            op = self.current_token().value
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)

        return left

    def parse_logical_and(self):
        left = self.parse_equality()

        while self.current_token().type == TokenType.AND:
            op = self.current_token().value
            self.advance()
            right = self.parse_equality()
            left = BinaryOp(left, op, right)

        return left

    def parse_equality(self):
        left = self.parse_comparison()

        while self.current_token().type in (TokenType.EQ, TokenType.NEQ):
            op = self.current_token().value
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)

        return left

    def parse_comparison(self):
        left = self.parse_range()

        while self.current_token().type in (TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            op = self.current_token().value
            self.advance()
            right = self.parse_range()
            left = BinaryOp(left, op, right)

        return left

    def parse_range(self):
        left = self.parse_addition()

        if self.current_token().type == TokenType.RANGE:
            self.advance()
            right = self.parse_addition()
            return RangeExpr(left, right)

        return left

    def parse_addition(self):
        left = self.parse_multiplication()

        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplication()
            left = BinaryOp(left, op, right)

        return left

    def parse_multiplication(self):
        left = self.parse_power()

        while self.current_token().type in (TokenType.MULT, TokenType.DIV, TokenType.MOD):
            op = self.current_token().value
            self.advance()
            right = self.parse_power()
            left = BinaryOp(left, op, right)

        return left

    def parse_power(self):
        left = self.parse_unary()

        if self.current_token().type == TokenType.POWER:
            op = self.current_token().value
            self.advance()
            right = self.parse_power()  # Right associative
            left = BinaryOp(left, op, right)

        return left

    def parse_unary(self):
        if self.current_token().type in (TokenType.MINUS, TokenType.NOT):
            op = self.current_token().value
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand)

        return self.parse_postfix()

    def parse_postfix(self):
        expr = self.parse_primary()

        while True:
            if self.current_token().type == TokenType.LPAREN:
                # Function call
                self.advance()
                args = []
                while self.current_token().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    if self.current_token().type == TokenType.COMMA:
                        self.advance()
                self.expect(TokenType.RPAREN)

                if isinstance(expr, Identifier):
                    expr = FuncCall(expr.name, args)
                else:
                    raise SyntaxError("Invalid function call")
            else:
                break

        return expr

    def parse_primary(self):
        token = self.current_token()

        if token.type == TokenType.INT:
            self.advance()
            return Literal(token.value)
        elif token.type == TokenType.FLOAT:
            self.advance()
            return Literal(token.value)
        elif token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value)
        elif token.type == TokenType.BOOL:
            self.advance()
            return Literal(token.value)
        elif token.type == TokenType.IDENT:
            self.advance()
            return Identifier(token.value)
        elif token.type == TokenType.LBRACKET:
            return self.parse_array()
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_array(self):
        self.expect(TokenType.LBRACKET)
        elements = []

        while self.current_token().type != TokenType.RBRACKET:
            elements.append(self.parse_expression())
            if self.current_token().type == TokenType.COMMA:
                self.advance()

        self.expect(TokenType.RBRACKET)
        return ArrayLiteral(elements)

# ============= INTERPRETER =============
class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.globals = {}
        self.locals = [{}]
        self.setup_builtins()

    def setup_builtins(self):
        # Math functions
        self.globals['sqrt'] = lambda x: math.sqrt(x)
        self.globals['pow'] = lambda x, y: x ** y
        self.globals['abs'] = lambda x: abs(x)
        self.globals['floor'] = lambda x: math.floor(x)
        self.globals['ceil'] = lambda x: math.ceil(x)
        self.globals['round'] = lambda x: round(x)

        # Statistical functions
        self.globals['sum'] = lambda arr: sum(arr)
        self.globals['mean'] = lambda arr: mean(arr)
        self.globals['median'] = lambda arr: median(arr)
        self.globals['mode'] = lambda arr: mode(arr)
        self.globals['stdev'] = lambda arr: stdev(arr) if len(arr) > 1 else 0
        self.globals['variance'] = lambda arr: variance(arr) if len(arr) > 1 else 0
        self.globals['min'] = lambda arr: min(arr)
        self.globals['max'] = lambda arr: max(arr)

        # Utility functions
        self.globals['print'] = lambda *args: print(*args)
        self.globals['len'] = lambda x: len(x)
        self.globals['range'] = lambda start, end=None: list(range(start, end) if end else range(start))

        # Greek letter aliases
        self.globals['μ'] = self.globals['mean']
        self.globals['σ'] = self.globals['stdev']
        self.globals['Σ'] = self.globals['sum']

    def get_var(self, name):
        # Search from innermost to outermost scope
        for scope in reversed(self.locals):
            if name in scope:
                return scope[name]

        if name in self.globals:
            return self.globals[name]

        raise NameError(f"Variable '{name}' not defined")

    def set_var(self, name, value):
        # Set in current scope
        self.locals[-1][name] = value

    def interpret(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {type(node).__name__}")

    def visit_Program(self, node):
        result = None
        for stmt in node.statements:
            result = self.interpret(stmt)
        return result

    def visit_VarDecl(self, node):
        value = self.interpret(node.value)
        self.set_var(node.name, value)
        return value

    def visit_FuncDecl(self, node):
        self.set_var(node.name, ('function', node.params, node.body))
        return None

    def visit_IfStmt(self, node):
        condition = self.interpret(node.condition)

        if condition:
            for stmt in node.then_block:
                self.interpret(stmt)
        elif node.else_block:
            for stmt in node.else_block:
                self.interpret(stmt)

        return None

    def visit_ForStmt(self, node):
        iterable = self.interpret(node.iterable)

        for item in iterable:
            self.locals.append({})
            self.set_var(node.var_name, item)

            try:
                for stmt in node.body:
                    self.interpret(stmt)
            finally:
                self.locals.pop()

        return None

    def visit_WhileStmt(self, node):
        while self.interpret(node.condition):
            for stmt in node.body:
                self.interpret(stmt)
        return None

    def visit_ReturnStmt(self, node):
        value = self.interpret(node.value)
        raise ReturnValue(value)

    def visit_Assignment(self, node):
        value = self.interpret(node.value)
        # Find the variable in scopes and update it
        for scope in reversed(self.locals):
            if node.name in scope:
                scope[node.name] = value
                return value

        if node.name in self.globals:
            self.globals[node.name] = value
        else:
            self.set_var(node.name, value)

        return value

    def visit_BinaryOp(self, node):
        left = self.interpret(node.left)
        right = self.interpret(node.right)

        # Vectorized operations for arrays
        if isinstance(left, list) or isinstance(right, list):
            if node.op in ['+', '-', '*', '/', '**']:
                return self.vectorized_op(left, right, node.op)

        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
        elif node.op == '%':
            return left % right
        elif node.op == '**':
            return left ** right
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        elif node.op == 'and':
            return left and right
        elif node.op == 'or':
            return left or right
        else:
            raise Exception(f"Unknown operator: {node.op}")

    def vectorized_op(self, left, right, op):
        """Handle vectorized operations on arrays"""
        if isinstance(left, list) and isinstance(right, list):
            if len(left) != len(right):
                raise ValueError("Arrays must have same length for vectorized operations")
            return [self.apply_op(l, r, op) for l, r in zip(left, right)]
        elif isinstance(left, list):
            return [self.apply_op(l, right, op) for l in left]
        else:  # right is list
            return [self.apply_op(left, r, op) for r in right]

    def apply_op(self, left, right, op):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '**':
            return left ** right

    def visit_UnaryOp(self, node):
        operand = self.interpret(node.operand)

        if node.op == '-':
            return -operand
        elif node.op == 'not':
            return not operand
        else:
            raise Exception(f"Unknown unary operator: {node.op}")

    def visit_FuncCall(self, node):
        func = self.get_var(node.name)
        args = [self.interpret(arg) for arg in node.args]

        # Built-in function
        if callable(func):
            return func(*args)

        # User-defined function
        if isinstance(func, tuple) and func[0] == 'function':
            _, params, body = func

            if len(args) != len(params):
                raise TypeError(f"Function {node.name} expects {len(params)} arguments, got {len(args)}")

            # Create new scope
            self.locals.append({})

            # Bind parameters
            for (param_name, _), arg_value in zip(params, args):
                self.set_var(param_name, arg_value)

            try:
                for stmt in body:
                    self.interpret(stmt)
                return None
            except ReturnValue as ret:
                return ret.value
            finally:
                self.locals.pop()

        raise TypeError(f"{node.name} is not a function")

    def visit_ArrayLiteral(self, node):
        return [self.interpret(elem) for elem in node.elements]

    def visit_RangeExpr(self, node):
        start = self.interpret(node.start)
        end = self.interpret(node.end)
        return list(range(start, end))

    def visit_Identifier(self, node):
        return self.get_var(node.name)

    def visit_Literal(self, node):
        return node.value

# ============= MAIN =============
def run_shark(source_code: str):
    """Execute Shark code"""
    try:
        # Lexing
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()

        # Interpreting
        interpreter = Interpreter()
        interpreter.interpret(ast)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def run_shark_file(filename: str):
    """Execute Shark code from a file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()

        print(f"🦈 Executing {filename}...\n")
        run_shark(source_code)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error reading file: {e}")

# ============= EXAMPLES =============
if __name__ == "__main__":
    import sys

    # Check if a file was provided as argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        run_shark_file(filename)
    else:
        # If no file provided, try to run index.shark by default
        import os
        if os.path.exists('index.shark'):
            run_shark_file('index.shark')
        else:
            # Run example code
            print("🦈 Shark Language Interpreter v1.0")
            print("Usage: python shark.py <filename.shark>")
            print("Or create an index.shark file in the current directory\n")
            print("Running examples...\n")

            # Example 1: Basic variables and math
            print("=== Example 1: Variables and Math ===")
            code1 = """
var x: int = 10;
var y: float = 3.14;
var result = x + y * 2;
print("Result:", result);
"""
            run_shark(code1)

            # Example 2: Functions
            print("\n=== Example 2: Functions ===")
            code2 = """
media(a, b) => (a + b) / 2;

var m = media(10, 20);
print("Media:", m);

fatorial(n) => {
    ? n <= 1 {
        return 1;
    }
    return n * fatorial(n - 1);
}

var fat = fatorial(5);
print("Fatorial de 5:", fat);
"""
            run_shark(code2)

            # Example 3: Arrays and statistics
            print("\n=== Example 3: Statistics ===")
            code3 = """
var dados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

var μ = mean(dados);
var σ = stdev(dados);
var Σ = sum(dados);

print("Media (μ):", μ);
print("Desvio Padrão (σ):", σ);
print("Soma (Σ):", Σ);
print("Min:", min(dados));
print("Max:", max(dados));
"""
            run_shark(code3)

            # Example 4: Vectorized operations
            print("\n=== Example 4: Vectorized Operations ===")
            code4 = """
var vetor = [1, 2, 3, 4, 5];
var dobro = vetor * 2;
var quadrado = vetor ** 2;

print("Original:", vetor);
print("Dobro:", dobro);
print("Quadrado:", quadrado);
"""
            run_shark(code4)

            # Example 5: Loops and conditionals
            print("\n=== Example 5: Control Flow ===")
            code5 = """
print("Números pares de 1 a 10:");
for i in 1..11 {
    ? i % 2 == 0 {
        print(i);
    }
}

var contador = 0;
while contador < 5 {
    print("Contador:", contador);
    contador = contador + 1;
}
"""
            run_shark(code5)

            # Example 6: Complex statistics
            print("\n=== Example 6: Statistical Analysis ===")
            code6 = """
var notas = [7.5, 8.0, 6.5, 9.0, 7.0, 8.5, 9.5, 6.0];

var media = mean(notas);
var mediana = median(notas);
var desvio = stdev(notas);
var nota_min = min(notas);
var nota_max = max(notas);

print("Análise de Notas:");
print("================");
print("Média:", media);
print("Mediana:", mediana);
print("Desvio Padrão:", desvio);
print("Nota Mínima:", nota_min);
print("Nota Máxima:", nota_max);

? media >= 7.0 {
    print("Turma aprovada! 🎉");
} otherwise {
    print("Turma precisa melhorar.");
}
"""
            run_shark(code6)

            print("\n🦈 Todos os exemplos executados com sucesso!")