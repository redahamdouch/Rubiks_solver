import kociemba

cube = 'DRFFURLFBDFDDRUUUUUDRBFLULBBULLDFDRFBLFDLDFBRRULBBRRBL'

def give_key(cube):
    try:
        solution = kociemba.solve(cube)

        simple = ["R", "L", "D", "U", "B", "F"]
        inverse = ["R'", "L'", "D'", "U'", "B'", "F'"]
        double = ["R2", "L2", "D2", "U2", "B2", "F2"]

        kociemba_output = ["R'", "R", "L'", "L", "D'", "D", "U'", "U", "B'", "B", "F'", "F"]

        keypad_code = ["K_F3", "K_3", "K_F1", "K_1", "K_F4", "K_4", "K_F6", "K_6", "K_F7", "K_7", "K_9", "K_F9"]

        keypad_code_double = ["K_3", "K_1", "K_4", "K_6", "K_7", "K_F9"]

        touches_to_press_solve = []

        solution = solution.split(' ')
        solution = list(solution)

        solution_init = []

        for s in solution:
            if s in simple:
                index = simple.index(s)
                solution_init.append(inverse[index])
            elif s in inverse:
                index = inverse.index(s)
                solution_init.append(simple[index])
            elif s in double:
                solution_init.append(s)

        solution_init.reverse()

        for s in solution:
            if s in kociemba_output:
                index = kociemba_output.index(s)
                touches_to_press_solve.append(keypad_code[index])
            elif s in double:
                index = double.index(s)
                touches_to_press_solve.append(keypad_code_double[index])
                touches_to_press_solve.append(keypad_code_double[index])

        touches_to_press_mix = []

        for s in solution_init:
            if s in kociemba_output:
                index = kociemba_output.index(s)
                touches_to_press_mix.append(keypad_code[index])
            elif s in double:
                index = double.index(s)
                touches_to_press_mix.append(keypad_code_double[index])
                touches_to_press_mix.append(keypad_code_double[index])

        return touches_to_press_solve, touches_to_press_mix
    except:
        print("Erreur d'acquisition")



