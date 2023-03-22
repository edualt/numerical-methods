from flask import Flask, request, jsonify
import sympy as sp
from math import *

app = Flask(__name__)

@app.route('/biseccion', methods=['POST'])
def biseccion():
    data = request.json
    a = data['a']
    b = data['b']
    tol = data['tol']
    maxiter = data['maxiter']
    f = lambda x: eval(data['funcion'])
    
    i = 0
    fa = f(a)
    t=0
    iteraciones_a = []
    iteraciones_b = []
    iteraciones_c = []
    iteraciones_fc = []
    iteraciones_t = [0,]
    while i < maxiter:
        i += 1
        c = (a + b) / 2
        fc = f(c)
        if i > 1:
          t = abs(c - iteraciones_c[i-2])
          iteraciones_t.append(t)

        iteraciones_a.append(a)
        iteraciones_b.append(b)
        iteraciones_c.append(c)
        iteraciones_fc.append(fc)
        if fc == 0 or (b - a) / 2 < tol:
            return jsonify({'raiz': c, 'iteraciones': i, 'a': iteraciones_a, 'b': iteraciones_b, 'c': iteraciones_c, 'fc': iteraciones_fc, 't': iteraciones_t})
        if fa * fc > 0:
            a = c
            fa = fc
        else:
            b = c
    return jsonify({'raiz': c, 'iteraciones': i, 'a': iteraciones_a, 'b': iteraciones_b, 'c': iteraciones_c, 'fc': iteraciones_fc, 't': iteraciones_t})


@app.route('/newton-raphson', methods=['POST'])
def newton_raphson():
    data = request.json
    x1 = data['x1']
    tol = data['tol']
    maxiter = data['maxiter']
    f = lambda x: eval(data['funcion'])

    x = sp.Symbol('x')
    df = sp.diff(data['funcion'], x)

    roots = []
    i=0
    while i < maxiter:
        i += 1
        x2 = x1 - f(x1) / df.subs(x, x1)
        c=str(x2)
        roots.append(c)
        if abs(x2 - x1) < tol:
            return jsonify({'raiz': c, 'iteraciones': i, "x": roots})
        x1 = x2
    return jsonify({'raiz': c, 'iteraciones': i, 'x': roots})

    
@app.route('/secante', methods=['POST'])
def secante():
    data = request.json
    x0 = data['x0']
    x1 = data['x1']
    tol = data['tol']
    maxiter = data['maxiter']
    f = lambda x: eval(data['funcion'])

    # return values as lists
    iteraciones_x0 = []
    iteraciones_x1 = []
    iteraciones_x2 = []
    iteraciones_fx0 = []
    iteraciones_fx1 = []
    iteraciones_fx2 = []
    iteraciones_t = []

    i = 0
    while i < maxiter:
        i += 1
        fx0 = f(x0)
        fx1 = f(x1)
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        fx2 = f(x2)
        t = abs(x2 - x1)
        iteraciones_x0.append(x0)
        iteraciones_x1.append(x1)
        iteraciones_x2.append(x2)
        iteraciones_fx0.append(fx0)
        iteraciones_fx1.append(fx1)
        iteraciones_fx2.append(fx2)
        iteraciones_t.append(t)
        if abs(x2 - x1) < tol:
            return jsonify({'raiz': x2, 'iteraciones': i, 'x0': iteraciones_x0, 'x1': iteraciones_x1, 'x2': iteraciones_x2, 'fx0': iteraciones_fx0, 'fx1': iteraciones_fx1, 'fx2': iteraciones_fx2, 't': iteraciones_t})
        x0 = x1
        x1 = x2
    return jsonify({'raiz': x2, 'iteraciones': i, 'x0': iteraciones_x0, 'x1': iteraciones_x1, 'x2': iteraciones_x2, 'fx0': iteraciones_fx0, 'fx1': iteraciones_fx1, 'fx2': iteraciones_fx2, 't': iteraciones_t})

@app.route('/falsa-posicion', methods=['POST'])
def falsa_posicion():
    data = request.json
    a = data['a']
    b = data['b']
    tol = data['tol']
    maxiter = data['maxiter']
    f = lambda x: eval(data['funcion'])
    
    i = 0
    iteraciones_a = []
    iteraciones_b = []
    iteraciones_c = []
    iteraciones_fc = []
    iteraciones_t = [0,]
    while i < maxiter:
        i += 1
        fa = f(a)
        fb = f(b)
        c = a - fa * (b - a) / (fb - fa)
        fc = f(c)
        if i > 1:
          t = abs(c - iteraciones_c[i-2])
          iteraciones_t.append(t)

        iteraciones_a.append(a)
        iteraciones_b.append(b)
        iteraciones_c.append(c)
        iteraciones_fc.append(fc)
        if fc == 0 or (b - a) / 2 < tol:
            return jsonify({'raiz': c, 'iteraciones': i, 'a': iteraciones_a, 'b': iteraciones_b, 'c': iteraciones_c, 'fc': iteraciones_fc, 't': iteraciones_t})
        if fa * fc > 0:
            a = c
        else:
            b = c
    return jsonify({'raiz': c, 'iteraciones': i, 'a': iteraciones_a, 'b': iteraciones_b, 'c': iteraciones_c, 'fc': iteraciones_fc, 't': iteraciones_t})

if __name__ == '__main__':
    app.run()