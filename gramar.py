import ply.yacc as pyacc
import unittest
from lexer import Lexer 

#   Classe Gramar
#
class Gramar:
    
    def __init__(self):
        self.yacc = None
        self.lexer = None
        self.tokens = None
    
    def build(self, **kwargs):
        self.lexer = Lexer()
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self, **kwargs)
    
    def parse(self, string):
        self.lexer.input(string)
        return self.yacc.parse(lexer=self.lexer.lexer)
    
    def p_exparitm(self, p):
        """ exparitm : estrutura """
        p[0] = p[1]
        
    def p_estrutura1(self,p):
        """ estrutura : '{' estrutura '}' """
        p[0] = p[2]
    
    def p_estrutura2(self,p):
        """ estrutura : '{' '}' """
        p[0] = None
    
    def p_estrutura3(self, p):
        """ estrutura : '{' linha '}' """
        p[0] = p[2]
        
    def p_linha1(self, p):
        """ linha : linha linha
        """
        p[0] = []
        p[0].append(p[1])
        p[0].append(p[2])
    
    def p_linha2(self, p):
        """ linha : linha estrutura
                  | estrutura linha
        """
        p[0] = []
        p[0].append(p[1])
        p[0].append(p[2])
        
    def p_linha3(self, p):
        """ linha : VAR declvar ';'
        """
        p[0] = p[2]
    
    def p_declvar1(self, p):
        """ declvar :  declattr
        """
        p[0] = p[1]
        
    def p_declvar2(self, p):
        """ declvar :  declattr ',' declattr
        """
        p[0] = []
        
        p[0].append(p[1])
        p[0].append(p[3])
        
    def p_declattr1(self, p):
        """ declattr :  NAME
        """
        p[0] = {"op": "var", "val": {"tipo" : None, "nome": p[1], "valor": None}}
    
    def p_declattr2(self, p):
        """ declattr :   NAME '=' INT
        """
        p[0] = {"op": "var", "val": {"tipo" : "int", "nome": p[1], "valor": int(p[3])}}
        
    def p_declattr3(self, p):
        """ declattr :   NAME '=' STRING
        """
        p[0] = {"op": "var", "val": {"tipo" : "string", "nome": p[1], "valor": p[3].replace('"','')}}
    
    def p_error(self, p):
        if p:
            print(f"Syntax error: unexpected '{p.type}'")
        else:
            print("Syntax error: unexpected end of file")
        exit(1)
        
class TestGramarMethods(unittest.TestCase):

    def setUp(self):
        self.gramar = Gramar()
        self.gramar.build()
        
    def test_estutura(self):
        tc = "{{}}"
        t = self.gramar.parse(tc)
        self.assertEqual(t, None)
    
    def test_variaveis_1(self):
        tc = "{VAR dia;}"
        t = self.gramar.parse(tc)
        self.assertEqual(t, {'op': 'var', 'val': {'tipo': None, 'nome': 'dia', 'valor': None}})
    
    def test_variaveis_2(self):
        tc = "{VAR dia = 123;}"
        t = self.gramar.parse(tc)
        self.assertEqual(t, {'op': 'var', 'val': {'tipo': 'int', 'nome': 'dia', 'valor': 123}})
    
    def test_variaveis_3(self):
        tc = '{VAR dia = "123";}'
        t = self.gramar.parse(tc)
        self.assertEqual(t, {'op': 'var', 'val': {'tipo': 'string', 'nome': 'dia', 'valor': "123"}})
    
    def test_variaveis_4(self):
        tc = '{VAR dia = 1, mes="feb";}'
        t = self.gramar.parse(tc)
        self.assertEqual(t[0], {'op': 'var', 'val': {'tipo': 'int', 'nome': 'dia', 'valor': 1}})
        self.assertEqual(t[1], {'op': 'var', 'val': {'tipo': 'string', 'nome': 'mes', 'valor': 'feb'}})
    
    def test_variaveis_5(self):
        tc = '''{
            VAR dia = 1, mes="feb";
            VAR dia = 2, mes="mar";
            }
            '''
        t = self.gramar.parse(tc)
        self.assertEqual(t[0][0], {'op': 'var', 'val': {'tipo': 'int', 'nome': 'dia', 'valor': 1}})
        self.assertEqual(t[0][1], {'op': 'var', 'val': {'tipo': 'string', 'nome': 'mes', 'valor': 'feb'}})
        self.assertEqual(t[1][0], {'op': 'var', 'val': {'tipo': 'int', 'nome': 'dia', 'valor': 2}})
        self.assertEqual(t[1][1], {'op': 'var', 'val': {'tipo': 'string', 'nome': 'mes', 'valor': 'mar'}})
            
def main():
    unittest.main(verbosity=2)
    pass

if __name__ == "__main__":
    main()