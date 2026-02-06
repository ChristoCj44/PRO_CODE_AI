from .handlers import PythonHandler

class CodeRunner:
    def __init__(self):
        self.handler = PythonHandler()

    def run(self, language, code):
        if language.lower() != 'python':
            return {'error': 'Only Python is supported.'}
        
        return self.handler.execute(code)
