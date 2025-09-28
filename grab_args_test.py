import CLIGPT as cg 
tester = cg.CLIGPT()
test_text = 'instructions "Hello World" tokens 200'
print(tester.grab_args(test_text))
