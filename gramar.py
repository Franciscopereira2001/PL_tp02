import ply.yacc as pyacc
import unittest
from lexer import Lexer 

#   Classe Gramar
#
class Gramar:
    '''
    precedence = (
        ("left", "+", "-"),
        ("left", "*", "/"),
    )
    '''
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
    
    def flatten(self,A):
        rt = []
        
        for i in A:
            if isinstance(i,list) and not isinstance(i,dict): rt.extend(self.flatten(i))
            else: rt.append(i)
        return rt

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
        """ linha : linha linha """
        p[0] = []
        p[0].append(p[1])
        p[0].append(p[2])
    
    def p_linha2(self, p):
        """ linha : linha estrutura
                  | estrutura linha """
        p[0] = []
        p[0].append(p[1])
        p[0].append(p[2])
        
    def p_linha3(self, p):
        """ linha : VAR declvar ';' """
        p[0] = p[2]
    
    def p_linha4(self, p):
        """ linha : ESCREVER fparams_args ';' """
        p[0] = {"op": "ESCREVER", "params": p[2]}
    
    def p_declvar1(self, p):
        """ declvar :  declattr """
        p[0] = p[1]
        
    def p_declvar2(self, p):
        """ declvar :  declattr ',' declattr """
        p[0] = []
        
        p[0].append(p[1])
        p[0].append(p[3])
        
    def p_declattr1(self, p):
        """ declattr :  NAME """
        p[0] = {"op": "var", "params": {"tipo" : None, "nome": p[1], "valor": None}}
    
    def p_declattr2(self, p):
        """ declattr :   NAME '=' INT """
        p[0] = {"op": "var", "params": {"tipo" : "int", "nome": p[1], "valor": int(p[3])}}
        
    def p_declattr3(self, p):
        """ declattr :   NAME '=' STRING """
        p[0] = {"op": "var", "params": {"tipo" : "string", "nome": p[1], "valor": p[3].replace('"','')}}
    
    def p_declattr4(self, p):
        """ declattr :   NAME '=' num """
        p[0] = {"op": "var", "params": p[3]}
    
    def p_fparams_args1(self, p):
        """ fparams_args :  fparams_args_decl """
        p[0] = self.flatten([p[1]])
        
    def p_fparams_args2(self, p):
        """ fparams_args :  fparams_args_decl ',' fparams_args """
        p[0] = self.flatten([p[1], p[3]])
    
    def p_fparams_args_decl1(self, p):
        """ fparams_args_decl :  INT"""
        p[0] = {"tipo" : "int", "valor": int(p[1])}
    
    def p_fparams_args_decl2(self, p):
        """ fparams_args_decl :  STRING """
        p[0] = {"tipo" : "string", "valor": p[1].replace('"','')}

    def p_num1(self, p):
        """ num : valor '+' num
                | valor '-' num
                | valor '*' num
                | valor '/' num """
        p[0] = {"op": p[2], "params": [p[1], p[3]]}
    
    def p_num2(self, p):
        """ num : valor"""
        p[0] = p[1]
        
    def p_num3(self, p):
        """ num : '(' num ')' """
        p[0] = p[2]
        
    def p_valor1(self, p):
        """ valor : NAME """
        p[0] = {"tipo" : "int", "nome": p[1], "valor": None }

    def p_valor2(self, p):
        """ valor : '(' valor ')' """
        p[0] = p[2]

    def p_valor3(self, p):
        """ valor : INT """
        p[0] = p[0] = {"tipo" : "int", "nome": None, "valor": p[1] }

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
        self.assertEqual(t, {'op': 'var', 'params': {'tipo': None, 'nome': 'dia', 'valor': None}})
    
    def test_variaveis_2(self):
        tc = "{VAR dia = 123;}"
        t = self.gramar.parse(tc)
        self.assertEqual(t, {'op': 'var', 'params': {'tipo': 'int', 'nome': 'dia', 'valor': 123}})
    
    def test_variaveis_3(self):
        tc = '{VAR dia = "123";}'
        t = self.gramar.parse(tc)
        self.assertEqual(t, {'op': 'var', 'params': {'tipo': 'string', 'nome': 'dia', 'valor': "123"}})
    
    def test_variaveis_4(self):
        tc = '{VAR dia = 1, mes="feb";}'
        t = self.gramar.parse(tc)
        self.assertEqual(t[0], {'op': 'var', 'params': {'tipo': 'int', 'nome': 'dia', 'valor': 1}})
        self.assertEqual(t[1], {'op': 'var', 'params': {'tipo': 'string', 'nome': 'mes', 'valor': 'feb'}})
    
    def test_variaveis_5(self):
        tc = '''{
            VAR dia = 1, mes="feb";
            VAR dia = 2, mes="mar";
            }
            '''
        t = self.gramar.parse(tc)
        self.assertEqual(t[0][0], {'op': 'var', 'params': {'tipo': 'int', 'nome': 'dia', 'valor': 1}})
        self.assertEqual(t[0][1], {'op': 'var', 'params': {'tipo': 'string', 'nome': 'mes', 'valor': 'feb'}})
        self.assertEqual(t[1][0], {'op': 'var', 'params': {'tipo': 'int', 'nome': 'dia', 'valor': 2}})
        self.assertEqual(t[1][1], {'op': 'var', 'params': {'tipo': 'string', 'nome': 'mes', 'valor': 'mar'}})
    
    def test_variaveis_6(self):
        tc = '{VAR dia = ab+2;}'
        t = self.gramar.parse(tc)
        res = str(t) 
        self.assertEqual(t,{'op': 'var', 'params': {'op': '+', 'params': [{'tipo': 'int', 'nome': 'ab', 'valor': None}, {'tipo': 'int', 'nome': None, 'valor': '2'}]}})
    
    def test_variaveis_7(self):
        tc = '{VAR dia = (((ab)+2));}'
        t = self.gramar.parse(tc)
        res = str(t) 
        self.assertEqual(t,{'op': 'var', 'params': {'op': '+', 'params': [{'tipo': 'int', 'nome': 'ab', 'valor': None}, {'tipo': 'int', 'nome': None, 'valor': '2'}]}})
    
    def test_variaveis_8(self):
        tc = '{VAR dia = ((3+4*2));}' #todo: Falta a precedencia do *
        t = self.gramar.parse(tc)
        res = str(t) 
        self.assertEqual(t,{'op': 'var', 'params': {'op': '+', 'params': [{'tipo': 'int', 'nome': 'ab', 'valor': None}, {'tipo': 'int', 'nome': None, 'valor': '2'}]}})
    
    def test_escrever_1(self):
        tc = '{ESCREVER "ola Mundo!";}'
        t = self.gramar.parse(tc)
        self.assertEqual(t,{'op': 'ESCREVER', 'params': [{'tipo': 'string', 'valor': 'ola Mundo!'}]})
        
    def test_escrever_2(self):
        tc = '{ESCREVER "ola Mundo!", 123;}'
        t = self.gramar.parse(tc)
        self.assertEqual(t,{'op': 'ESCREVER', 'params': [{'tipo': 'string', 'valor': 'ola Mundo!'}, {'tipo': 'int', 'valor': 123}]})
    
    def test_escrever_3(self):
        tc = '{ESCREVER "ola Mundo!", 123, "ok" ;}'
        t = self.gramar.parse(tc)
        self.assertEqual(t,{'op': 'ESCREVER', 'params': [{'tipo': 'string', 'valor': 'ola Mundo!'}, {'tipo': 'int', 'valor': 123}, {'tipo': 'string', 'valor': "ok"}]})
    '''
    def test_escrever_4(self):
        tc = '{ESCREVER "soma de ", 9, "com ", 3*4 , "=", 9+2*3 ;}'
        t = self.gramar.parse(tc)
        self.assertEqual(t,{'op': 'ESCREVER', 'params': [{'tipo': 'string', 'valor': 'ola Mundo!'}, {'tipo': 'int', 'valor': 123}, {'tipo': 'string', 'valor': "ok"}]})
    '''
    
    
def main():
    unittest.main(verbosity=2)
    pass

if __name__ == "__main__":
    main()