class Calculator():

    def __init__(self):
        self.operatorsByPrecedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    def parse(self, inputstr):
        if not inputstr:
            raise ValueError('нет входа')

        index = 0
        operators = []
        output = []
        while index < len(inputstr):
            current_token = inputstr[index]
            if current_token.isdigit():
                current_number = current_token
                while (index < len(inputstr) - 1) and (inputstr[index + 1].isdigit() or inputstr[index + 1] =='.'):
                    index += 1
                    assert not (inputstr[index] == inputstr[index-1] == '.'), 'много точек'
                    current_number += inputstr[index]
                output.append(float(current_number))
            elif current_token in self.operatorsByPrecedence:
                operator_index = len(operators) - 1
                while operator_index >= 0 and \
                        operators[operator_index] != '(' and \
                        self.operatorsByPrecedence[current_token] <= \
                        self.operatorsByPrecedence[operators[operator_index]]:
                    output.append(operators.pop())
                    operator_index -= 1
                operators.append(current_token)
            elif current_token == '(':
                operators.append(current_token)
            elif current_token == ')':
                operator_index = len(operators) - 1
                while operator_index >= 0 and \
                        operators[operator_index] != '(':
                    output.append(operators.pop())
                    operator_index -= 1
                if operator_index < 0:
                    raise SyntaxError(
                        'нет пары для  ")" на индексе {0}'.format(index))
                operators.pop()
            elif current_token == ' ':
                pass
            else:
                raise SyntaxError(
                    'неизвестный токен "{0}" на индексе {1}'.format(current_token, index))
            index += 1
        while operators:
            operator = operators.pop()
            if operator == '(':
                raise SyntaxError('нет пары "("')
            output.append(operator)

        return output

    def process(self, parsed_tokens):
        if len(parsed_tokens) == 0:
            raise ValueError('нечего обрабатывать')
        index = 0
        values = []
        while index < len(parsed_tokens):
            # print(index)
            current_token = parsed_tokens[index]
            if type(current_token).__name__ == 'float':
                values.append(current_token)
            elif current_token in self.operatorsByPrecedence:
                if len(values) < 2:
                    raise SyntaxError('недостаточно аргументов')
                right = values.pop()
                left = values.pop()
                if current_token == '+':
                    values.append(left + right)
                elif current_token == '-':
                    values.append(left - right)
                elif current_token == '*':
                    values.append(left * right)
                elif current_token == '/':
                  if right==0:
                    raise ZeroDivisionError('деление на 0')
                  values.append(left / right)
            index += 1

        if len(values) == 1:
            return values[0]

        raise SyntaxError('недостаточно операторов')

    def evaluate(self, inputstr):
        return self.process(self.parse(inputstr))
