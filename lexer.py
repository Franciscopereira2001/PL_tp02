import ply.lex as plex
import unittest
#   Classe Lexer
#
class Lexer(object):
    tokens = ("INT", "ESCREVER", "VAR", "ENTRADA", "ALEATORIO", "PARA", "EM", "FAZER", "FIM", "SE", "SENAO", "NEG", "STRING", "NAME")
    literals = [";", "=", "+", "-", "*", "/", ",", '"', "(", ")", "[", "]", "<", ">", "&", "|", ".", "{", "}"]
    t_ignore =" \t\r\n"
    
    def __init__(self, exit_failure=False):
        self.lexer = None
        self.exit_failure = exit_failure
    
    t_INT = r"-?[0-9]+"
    t_ESCREVER = r"ESCREVER"
    t_VAR = r"VAR"
    t_ENTRADA = r"ENTRADA"
    t_ALEATORIO = r"ALEATORIO"
    t_PARA = r"PARA"
    t_EM = r"EM"
    t_FAZER = r"FAZER"
    t_FIM = r"FIM"
    t_SE = r"SE"
    t_SENAO = r"SENAO"
    t_NEG = r"NEG"
    t_STRING = r'"[^"]*"'
    t_NAME = "[a-z]([a-z]|[A-Z]|[0-9]|_)*"
    
    def build(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)
    
    def input(self, str):
        self.lexer.input(str)
    
    def token(self): 
        token = self.lexer.token()
        return token if token is None else token.type

    def t_error(self, t):
        print(f"{t.lexer.lineno}: Illegal character '{t.value[0]}'")
        if self.exit_failure == False:
            t.lexer.skip(1)
        else:
            exit(1)
        
#   Testes unitarios
#
class TestLexerMethods(unittest.TestCase):
    
    def setUp(self):
        self.lexer = Lexer()
    
    def helper(self, tc, expect):
        self.lexer.build()
        self.lexer.input(tc)
        
        if type(expect) is list:
            for e in expect:
                token = self.lexer.token()
                self.assertEqual(token, e)
        else:
            token = self.lexer.token()
            self.assertEqual(token, expect)
    
    def test_PROGRAM(self):
        self.helper("{}", ["{", "}"])
        self.helper("{-123}", ["{", "INT", "}"])
        
    def test_INT(self):
        self.helper("123", "INT")
        self.helper("-123", "INT")
    
    def test_ESCREVER(self):
        self.helper("ESCREVER", "ESCREVER")
    
    def test_ENTRADA(self):
        self.helper("ENTRADA", "ENTRADA")
        
    def test_ALEATORIO(self):
        self.helper("ALEATORIO", "ALEATORIO")
    
    def test_PARA(self):
        self.helper("PARA", "PARA")
    
    def test_EM(self):
        self.helper("EM", "EM")
    
    def test_FAZER(self):
        self.helper("FAZER", "FAZER")
    
    def test_FIM(self):
        self.helper("FIM", "FIM")
    
    def test_SE(self):
        self.helper("SE", "SE")
    
    def test_SENAO(self):
        self.helper("SENAO", "SENAO")
        
    def test_NEG(self):
        self.helper("NEG", "NEG")
    
    def test_STRING(self):
        self.helper('"abc"', "STRING")
    
    def test_NAME(self):
        self.helper('qwert', "NAME")
        
    def test_literals(self):
        for literal in self.lexer.literals:
            self.helper(literal, literal)
        
    def test_complex1(self):
        tc = 'ESCREVER "ola mundo!";'
        self.helper(tc,["ESCREVER", "STRING", ";"])
    
    def test_complex2(self):
        tc = 'ESCREVER "PL ", 2 ,"o ano de", "ESI";'
        self.helper(tc,["ESCREVER", "STRING", ",", "INT", "," ,"STRING", "," , "STRING" , ";"])
        
    def test_complex3(self):
        tc = 'ESCREVER "soma de ", 9, "com ", 3*4 , "=", 9+2*3 ;'
        self.helper(tc,["ESCREVER", "STRING", ",", "INT", "," ,"STRING", "," , "INT", "*", "INT", "," , "STRING", "," , "INT" , "+", "INT", "*", "INT", ";"])
    
    def test_complex4(self):
        tc = 'VAR ano = 2023, mes="maio", dia ;'
        self.helper(tc, ["VAR", "NAME", "=", "INT", "," , "NAME" , "=", "STRING", ",", "NAME", ";"])
    
    def test_complex5(self):
        tc = "tmp = 7+3 ;"
        self.helper(tc, ["NAME", "=", "INT", "+", "INT", ";"])
    
    def test_complex6(self):
        tc = "a = 10 (30 + tmp ) ;"
        self.helper(tc, ["NAME", "=", "INT", "(", "INT", "+", "NAME", ")"])
    
    def test_complex7(self):
        tc = "a ++; a += 10; b = tmp * (a + 10);"
        self.helper(tc, ["NAME", "+", "+", ";", "NAME", "+", "=", "INT", ";", "NAME", "=", "NAME", "*", "(", "NAME", "+", "INT" ,")"])
        
    def test_complex8(self):
        tc = "valor = ENTRADA();"
        self.helper(tc, ["NAME", "=", "ENTRADA", "(", ")", ";"])
    
    def test_complex9(self):
        tc = "valor = ALEATORIO(10);"
        self.helper(tc, ["NAME", "=", "ALEATORIO", "(", "INT", ")", ";"])
    
    def test_complex10(self):
        tc = "PARA i EM [10..20] FAZER < valor = ALEATORIO(10); > FIM PARA ;"
        self.helper(tc, ["PARA", "NAME", "EM", "[", "INT", ".", ".", "INT", "]", "FAZER" , "<", "NAME", "=", "ALEATORIO", "(", "INT", ")", ";", ">", "FIM", "PARA", ";"])
    
    
    def test_error(self):
        self.helper("", None)
        

def main():
    unittest.main(verbosity=2)

if __name__ == "__main__":
    main()