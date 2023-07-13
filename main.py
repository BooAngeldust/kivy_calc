from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivy.config import Config

Config.set('graphics', 'resizable', 1)

class Calculator:
    __operands = {
            "/" : 100,
            "*" : 100,
            "+" : 99,
            "-" : 99,
    }

    __math_op_func = {
        '/' : lambda x,y: x/y,
        '*' : lambda x,y: x*y,
        '+' : lambda x,y: x+y,
        '-' : lambda x,y: x-y,
    }

    def __parseString(string : str) -> list:
        parsed_arr = []
        _temp = ""

        for n, i in enumerate(string):
            if i in Calculator.__operands.keys() and _temp != "":
                parsed_arr.append(float(_temp))
                parsed_arr.append(i)
                _temp = ""
            else:
                _temp += i

            if (n == len(string) - 1):
                parsed_arr.append(float(_temp))

        return parsed_arr
    
    def __calculateRecursed(arr : list) -> list:
        temp_arr = arr
        last_char = ""

        arr_not_clean = True
        while (arr_not_clean):
            arr_not_clean = False
            # Check if opearands are repeated
            for n, i in enumerate(temp_arr):
                if (i in Calculator.__operands and last_char in Calculator.__operands):
                    arr_not_clean = True
                    if (i in ['+','-']):
                        if last_char == i:
                            temp_arr[n] == '+'
                        else:
                            temp_arr[n] == '-'
                        temp_arr.pop(n-1)

            last_char = i
        
        while (len(temp_arr) > 1):
            highest_priority = 0

            index = 0
            operand = "+"

            # Find highest priority operand
            for i in temp_arr:
                if i in Calculator.__operands.keys():
                    if Calculator.__operands[i] >= highest_priority:
                        highest_priority = Calculator.__operands[i]

            # Find index of that operand
            for n, i in enumerate(temp_arr):
                if i in Calculator.__operands.keys() and Calculator.__operands[i] == highest_priority:
                    index = n
                    operand = i
                    break

            print(f"[DEBUG] BEFORE: {temp_arr}")

            x = temp_arr[index-1]
            y = temp_arr[index+1]

            temp_arr[index] = Calculator.__math_op_func[operand](x,y)

            temp_arr.pop(index-1)
            temp_arr.pop(index)

            print(f"[DEBUG] AFTER: {temp_arr}")

            
        
        return temp_arr


    def calculate(string : str) -> float:
        parsed_arr = Calculator.__parseString(string)
        
        return Calculator.__calculateRecursed(parsed_arr)[0]


class CalcBase(GridLayout):
    def calculate(self, string : str) -> None:
        try:
            ans = Calculator.calculate(string)
            self.display.text = str(ans)
        except:
            self.display.text = f"Invalid Input: [{string}]"
        


class CalcApp(App):
    def build(self):
        return CalcBase()


if __name__ == '__main__':
    CalcApp().run()