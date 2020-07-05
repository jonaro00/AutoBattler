scripts = [
    {
        'name': 'Auto Blanche 3@270ms',
        'sequence':
            'U1;R2;U3;\n'+
            '\n'    * 2  +
            'T3;\n'      +
            'T3;\n'      +
            '\n'    * 4  +
            'T3;\n'      +
            'T3;\n'      +
            '\n'    * 4  +
            'T1;\n'      +
            'T1;\n'      +
            '\n'    * 3  +
            'T3;\n'      +
            'T3;\n'      +
            '\n'    * 2  +
            'R3;\n'      +
            'T1;\n' * 229+
            'U2;T1;\n'   +
            'T1;\n' * 2  +
            '\n'    * 3  +
            'T2;\n'      +
            'T2;\n'      +
            '\n'    * 5
            ,
        'onend': 'R1;R2;R3;',
    },
    {
        'name': 'Auto Blanche 3',
        'sequence':
            'U1;R2;U3;\n'+
            '\n'    * 2  +
            'T3;\n'      +
            'T3;\n'      +
            '\n'    * 5  +
            'T3;\n'      +
            'T3;\n'      +
            '\n'    * 5  +
            'T1;\n'      +
            'T1;\n'      +
            '\n'    * 4  +
            'T3;\n'      +
            'T3;\n'      +
            '\n'    * 2  +
            'R3;\n'      +
            'T1;\n' * 248+
            'U2;T1;\n'   +
            'T1;\n' * 2  +
            '\n'    * 3  +
            'T2;\n'      +
            'T2;\n'      +
            '\n'    * 5
            ,
        'onend': 'R1;R2;R3;',
    },
    {
        'name': 'Auto Blanche 2',
        'sequence':
            'U1;U2;U3;\n'+
            '\n'    * 2  +
            'T3;\n'      +
            '\n'    * 7  +
            'T3;\n'      +
            '\n'    * 7  +
            'T1;\n'      +
            '\n'    * 7  +
            'T3;\n'      +
            '\n'    * 2  +
            'T1;\n' * 255+
            '\n'    * 1  +
            'T2;\n'      +
            '\n'    * 6
            ,
        'onend': 'R1;R2;R3;',
    },
    {
        'name': 'Auto Blanche 1',
        'sequence':
            'U1;U2;U3;\n'+
            '\n'    * 2  +
            'T3;\n'      +
            '\n'    * 7  +
            'T3;\n'      +
            '\n'    * 7  +
            'T1;\n'      +
            '\n'    * 7  +
            'T3;\n'      +
            '\n'    * 20 +
            'T1;\n' * 275+
            '\n'    * 4  +
            'T2;\n'      +
            '\n'    * 12
            ,
        'onend': 'R1;R2;R3;',
    },
    {
        'name': 'Test taps',
        'sequence':
            'U1;U2;U3;\n'+
            '\n'         +
            'T1;\n'      +
            'T2;\n'      +
            'T3;\n'      +
            '\n'
            ,
        'onend': 'R1;R2;R3;',
    },
    {
        'name': 'T1T2T3',
        'sequence':
            'U1;U2;U3;\n'+
            '\n'         +
            'T1;T2;T3;\n'+
            '\n'
            ,
        'onend': 'R1;R2;R3;',
    },
    {
        'name': 'T2T2',
        'sequence':
            'U2;\n'      +
            '\n'         +
            'T2;\n'      +
            'T2;\n'      +
            '\n'
            ,
        'onend': 'R1;R2;R3;',
    },
    {
        'name': 'Rapid T1',
        'sequence':
            'U1;R2;R3;\n'+
            '\n'     * 4 +
            'T1;\n'  * 40+
            '\n'     * 3
            ,
        'onend': 'R1;',
    },
    {
        'name': 'Rapid T2',
        'sequence':
            'R1;U2;R3;\n'+
            '\n'     * 4 +
            'T2;\n'  * 40+
            '\n'     * 3
            ,
        'onend': 'R2;',
    },
    {
        'name': 'Rapid T3',
        'sequence':
            'R1;R2;U3;\n'+
            '\n'     * 4 +
            'T3;\n'  * 40+
            '\n'     * 3
            ,
        'onend': 'R3;',
    },
]