def igor_contains_trig(f, symbols):
    """
    Returns True if f contains sin, cos, tan or cot
    """
    result = []
    if f.args:
        for a in f.args:
            if contains_trig(a, symbols):
                return True
        if f.func in [sin, cos, tan, cot]:
            free = f.free_symbols
            if any(s in free for s in symbols):
                return True
    return False

def igor_is_sin_cos(gens):
    for g in gens:
        if not g.func in [sin, cos]:
           return False
    return True

def igor_trigonometry_formulas(f):
         n=f.find("cos(x+pi/4)")
         #n is set
         if len(n)>0 :
             f = f.replace("cos(x+pi/4)","(sqrt(2)*cos(x)/2 - sqrt(2)*sin(x)/2)")

         n=f.find("sin(2*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("sin(2*x)","2*sin(x)*cos(x)")

         n=f.find("sin(3*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("sin(3*x)","3*sin(x)-4*sin(x)**3")

         n=f.find("cos(3*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("cos(3*x)","4*cos(x)**3-3*cos(x)")

         n=f.find("sin(4*x)")
         #n is set
         if len(n)>0 :
             f = f.replace("sin(4*x)","(2*cos(2*x)*sin(2*x))")
             print(f)

         n=f.find("sin(x)**2")
         if len(n)>0 :
             f = f.replace("sin(x)**2","(1-cos(2*x))/2")

         n=f.find("-cos(x)")
         n1 = f.find("1")
         if len(n)>0 and len(n1)>0:
             f = f.replace("-cos(x)","-2*sin(x/2)**2")
             f = f.replace("1","0")
         return f

