import ply.lex as plex
import unittest
#   Classe Lexer
#
class Lexer(object):
    tokens = ("INT", "ESCREVER", "VAR", "ENTRADA", "ALEATORIO", "PARA", "EM", "FAZER", "FIM", "SE", "SENAO", "NEG", "STRING", "VARNAME")
    literals = [";", "=", "+", "-", "*", "/", ",", '"', "(", ")", "[", "]", "<", ">", "&", "|"]
    t_ignore =" \t"
    
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
    t_VARNAME = "[a-z]([a-z]|[A-Z]|[0-9]|_)*"
    
    def build(self, string, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)
        self.lexer.input(string)
        
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
        self.lexer.build(tc)
        
        if type(expect) is list:
            for e in expect:
                token = self.lexer.token()
                self.assertEqual(token, e)
        else:
            token = self.lexer.token()
            self.assertEqual(token, expect)
    
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
    
    def test_VARNAME(self):
        self.helper('qwert', "VARNAME")
        
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
        self.helper(tc, ["VAR", "VARNAME", "=", "INT", "," , "VARNAME" , "=", "STRING", ",", "VARNAME", ";"])
    
    def test_error(self):
        self.helper("", None)
        

def main():
    unittest.main(verbosity=2)

if __name__ == "__main__":
    main()