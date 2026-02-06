import ast

class PythonAnalyzer:
    def analyze(self, code):
        try:
            tree = ast.parse(code)
            visitor = ComplexityVisitor()
            visitor.visit(tree)
            
            # Formulate result
            time_comp = self._format_complexity(visitor.max_loop_depth, visitor.has_recursion)
            explanation = self._generate_explanation(visitor.max_loop_depth, visitor.has_recursion)
            
            return {
                'time_complexity': time_comp,
                'space_complexity': 'O(n)' if visitor.has_recursion else 'O(1)', # Simplified heuristic
                'confidence': '90%',
                'explanation': explanation
            }
        except SyntaxError:
             return {
                'time_complexity': 'N/A',
                'space_complexity': 'N/A',
                'confidence': '0%',
                'explanation': 'Syntax Error: Cannot analyze complexity.'
            }
        except Exception as e:
            return {
                'time_complexity': 'Unknown',
                'space_complexity': 'Unknown',
                'confidence': '0%',
                'explanation': f'Analysis Error: {str(e)}'
            }

    def _format_complexity(self, depth, recurses):
        if recurses:
            return 'O(2^n) or O(log n) (Recursive)' # Broad estimation for recursion
        if depth == 0:
            return 'O(1)'
        if depth == 1:
            return 'O(n)'
        return f'O(n^{depth})'

    def _generate_explanation(self, depth, recurses):
        reasons = []
        if depth > 0:
            reasons.append(f"Detected {depth} nested loops.")
        else:
            reasons.append("No loops detected (constant time).")
            
        if recurses:
            reasons.append("Detected pattern indicative of recursion.")
            
        return " ".join(reasons)

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.max_loop_depth = 0
        self.current_depth = 0
        self.has_recursion = False
        self.function_names = set()

    def visit_FunctionDef(self, node):
        self.function_names.add(node.name)
        # Check for recursion in body
        self.generic_visit(node)

    def visit_Call(self, node):
        # A simple recursion check: if a call name matches a known function name
        # Note: This is a basic check and won't catch indirect recursion perfectly or if func isn't defined yet
        if isinstance(node.func, ast.Name):
            if node.func.id in self.function_names:
                self.has_recursion = True
        self.generic_visit(node)

    def visit_For(self, node):
        self.current_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1

    def visit_While(self, node):
        self.current_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1
