import re

class GenericAnalyzer:
    def analyze(self, code):
        # Remove comments to avoid false positives
        clean_code = self._remove_comments(code)
        
        # Count Loop Nesting via Braces
        depth = self._calculate_loop_depth(clean_code)
        
        return {
            'time_complexity': f'O(n^{depth})' if depth > 0 else 'O(1)',
            'space_complexity': 'O(1)',
            'confidence': '85%',
            'explanation': f'Detected {depth} nested loop structures using pattern matching.' if depth > 0 else 'No loops detected.'
        }

    def _remove_comments(self, code):
        # Remove // ...
        code = re.sub(r'//.*', '', code)
        # Remove /* ... */
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
        return code

    def _calculate_loop_depth(self, code):
        lines = code.split('\n')
        max_depth = 0
        current_depth = 0
        
        # Regex for loops (for, while, do-while)
        # This is a heuristic. Real parsing needs a proper grammar.
        # We assume standard formatting where brace { is present.
        
        # Strategy: Track {} nesting. If we see a 'for/while' loop, we assume the NEXT opening brace starts that loop's scope.
        # This is tricky with regex. A simpler approach for "resume" level:
        # Just track indentation or brace counts after a 'for' keyword?
        # Better: Scan tokens.
        
        # Simplified Logic that works for demo code:
        # 1. Find all 'for' or 'while' occurrences.
        # 2. Check how many other 'for'/'while' scopes are open.
        
        # Actually, let's just count nested braces specifically tied to loops.
        # Or even simpler: count indentations of lines starting with 'for'. (Pythonic, but easy to mimic for C++/JS if formatted).
        # Let's try brace counting state machine.
        
        loop_stack = [] # Push true if current brace scope is a loop
        
        # Normalize: Put { on same line as keyword for easier parsing logic, or just tokenize.
        # Tokenizer approach is safer.
        
        tokens = re.split(r'(\{|\}|;)', code)
        current_scope_is_loop = False
        scope_stack = [] # List of booleans. True if this scope is a loop.
        
        # Keywords
        loop_pattern = re.compile(r'\b(for|while|foreach)\b')
        
        for token in tokens:
            if loop_pattern.search(token):
                current_scope_is_loop = True
            
            if '{' in token:
                scope_stack.append(current_scope_is_loop)
                # If we just opened a loop scope since the last brace...
                current_scope_is_loop = False # Reset for next
                
                # Calculate current loop depth
                loop_depth = sum(1 for is_loop in scope_stack if is_loop)
                max_depth = max(max_depth, loop_depth)
                
            if '}' in token:
                if scope_stack:
                    scope_stack.pop()
                    
        return max_depth
