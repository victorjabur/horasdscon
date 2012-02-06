import requests

class Pmo:

    def login(self, usuario, senha):
        post_login = {'login':'login', 'username':usuario, 'password':senha, 'login.x':'13', 'login.y':'12'}
        r = requests.post('http://www.dscon.com.br/pmo/index.php', post_login)
        pagina = requests.get('http://dscon.com.br/pmo/index.php?', cookies=r.cookies)
        return r