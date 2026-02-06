from .ai_analyzer import AiAnalyzer

class ComplexityAnalyzer:
    def __init__(self):
        self.analyzer = AiAnalyzer()

    def analyze(self, language, code):
        # We ignore 'language' param effectively since it's Python only now, 
        # but keep signature for compatibility or future use.
        return self.analyzer.analyze(code)
