#Author- Mohamed Mashaly     MDE,Faculty of Engineering,Cairo University
#Description- creat a 2D spline from an equuation

from math import acos, acosh, asin, asinh, atan, atan2, atanh, ceil, copysign, cos, cosh, degrees, e, erf, erfc, exp, expm1, fabs, factorial, floor, fmod, frexp, fsum, gamma, gcd, hypot, inf, isclose, isfinite, isinf, isnan, ldexp, lgamma, log, log10, log1p, log2, modf, nan, pi, pow, radians, sin, sinh, sqrt, tan, tanh, trunc
import adsk.core, adsk.fusion, adsk.cam, traceback
_handlers=[]
app = adsk.core.Application.get()
ui  = app.userInterface
x=1
T=0
#safe_list=['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign', 'cos', 'cosh', 'degrees', 'e', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite', 'isinf', 'isnan', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'nan', 'pi', 'pow', 'radians', 'remainder', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau', 'trunc']
#safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])
#safe_dict['abs'] = abs
#safe_dict['x'] = x
#safe_dict['T'] = T
class MyInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            inputs = eventArgs.inputs
            list1=inputs.itemById('pc').selectedItem.name

            if str(list1) == 'Cylindrical':
               inputs.itemById('xmin').isVisible=False
               inputs.itemById('xmax').isVisible=False
               inputs.itemById('tmin').isVisible=True
               inputs.itemById('tmax').isVisible=True
               inputs.itemById('equa_cyl').isVisible=True
               inputs.itemById('equa_car').isVisible=False
               inputs.itemById('equa_px').isVisible=False
               inputs.itemById('equa_py').isVisible=False
            elif str(list1) == 'Cartesian':
               inputs.itemById('equa_car').isVisible=True
               inputs.itemById('equa_cyl').isVisible=False
               inputs.itemById('equa_px').isVisible=False
               inputs.itemById('equa_py').isVisible=False
               inputs.itemById('xmin').isVisible=True
               inputs.itemById('xmax').isVisible=True
               inputs.itemById('tmin').isVisible=False
               inputs.itemById('tmax').isVisible=False
            elif  str(list1) == 'Parametric':
               inputs.itemById('equa_car').isVisible=False
               inputs.itemById('equa_cyl').isVisible=False
               inputs.itemById('equa_px').isVisible=True
               inputs.itemById('equa_py').isVisible=True
               inputs.itemById('tmin').isVisible=True
               inputs.itemById('tmax').isVisible=True
               inputs.itemById('xmin').isVisible=False
               inputs.itemById('xmax').isVisible=False
              
        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
class MyCommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            cmdDef = ui.commandDefinitions.itemById('Spline_Derived_Euations')
            if cmdDef:
             cmdDef.deleteMe() 
             
            adsk.terminate() 
        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
class MyExecuteHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
         cmd=adsk.core.Command.cast(args.command)
         inputs=cmd.commandInputs
         p_or_c=inputs.addDropDownCommandInput('pc','Parametric Or Cartesian Or Cylindrical',adsk.core.DropDownStyles.TextListDropDownStyle)
         list1=p_or_c.listItems
         list1.add('Parametric',True)
         list1.add('Cylindrical',False)
         list1.add('Cartesian',False)
         inputs.addStringValueInput('equa_car', 'Enter Equation Y =', '')
         inputs.addStringValueInput('equa_cyl', 'Enter Equation R =', '')
         inputs.addStringValueInput('equa_px', 'Enter Equation X =', '')
         inputs.addStringValueInput('equa_py', 'Enter Equation Y =', '')
         inputs.addValueInput('xmin','Enter X Min','',adsk.core.ValueInput.createByReal(0.0))
         inputs.addValueInput('xmax','Enter X Max','',adsk.core.ValueInput.createByReal(0.0))
         inputs.addValueInput('tmin','Enter T Min','',adsk.core.ValueInput.createByReal(0.0))
         inputs.addValueInput('tmax','Enter T Max','',adsk.core.ValueInput.createByReal(0.0))
         inputs.addValueInput('noi','Enter No. of Points','',adsk.core.ValueInput.createByReal(0.0))
         X_Basis=inputs.addSelectionInput('xBasis','Enter X Basis','Select X Coordinate')
         X_Basis.setSelectionLimits(1,1)
         X_Basis.addSelectionFilter('SketchLines')
         Y_Basis=inputs.addSelectionInput('yBasis','Enter Y Basis','Select Y Coordinate')
         Y_Basis.setSelectionLimits(1,1)
         Y_Basis.addSelectionFilter('SketchLines')
         Origin=inputs.addSelectionInput('or','Enter origin Point','Select origin point')
         Origin.setSelectionLimits(1,1)
         Origin.addSelectionFilter('SketchPoints')
         inputs.itemById('xmin').isVisible=False
         inputs.itemById('xmax').isVisible=False
         inputs.itemById('tmin').isVisible=False
         inputs.itemById('tmax').isVisible=False
         inputs.itemById('equa_car').isVisible=False
         inputs.itemById('equa_cyl').isVisible=False
         inputs.itemById('equa_px').isVisible=False
         inputs.itemById('equa_py').isVisible=False
         # when input change
         onInputChanged = MyInputChangedHandler()
         cmd.inputChanged.add(onInputChanged)
         _handlers.append(onInputChanged)
         # Connect to the command destroyed event.
         onDestroy = MyCommandDestroyHandler()
         cmd.destroy.add(onDestroy)
         _handlers.append(onDestroy)
         # When OK button is pressed
         onExecute = MyExecuteHandler2()
         cmd.execute.add(onExecute)
         _handlers.append(onExecute)
        except:
         if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
class MyExecuteHandler2(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
       try: 
        eventArgs = adsk.core.CommandEventArgs.cast(args)
        inputs = eventArgs.command.commandInputs
        origin=inputs.itemById('or').selection(0).entity.geometry
        #zbasis=adsk.core.Point3D.create(0, 0,1).asVector()
        xbasis=inputs.itemById('xBasis').selection(0).entity.startSketchPoint.geometry.vectorTo(inputs.itemById('xBasis').selection(0).entity.endSketchPoint.geometry)
        ybasis=inputs.itemById('yBasis').selection(0).entity.startSketchPoint.geometry.vectorTo(inputs.itemById('yBasis').selection(0).entity.endSketchPoint.geometry)
        n=int(inputs.itemById('noi').value)
        pnts = adsk.core.ObjectCollection.create()
        actSketch=app.activeEditObject
        p=origin.getData()
        list1=inputs.itemById('pc').selectedItem.name
        if str(list1) == 'Cylindrical':
         Equ = inputs.itemById('equa_cyl').value
         Equ=Equ.replace('^','**')
         xmi=inputs.itemById('tmin').value
         xma=inputs.itemById('tmax').value
         for i in range(0, n+1):
          T=xmi*(1-i/n)+(i/n)*xma
          r=eval(Equ,{"__builtins__":None},{'t': T,'T': T,'acos': acos,'acosh': acosh,'asin': asin,'asinh': asinh,'atan': atan,'atan2': atan2,'atanh': atanh,'ceil': ceil,'copysign': copysign,'cos': cos,'cosh': cosh,'degrees': degrees,'e': e,'erf': erf,'erfc': erfc,'exp': exp,'expm1': expm1,'fabs': fabs,'factorial': factorial,'floor': floor,'fmod': fmod,'frexp': frexp,'fsum': fsum,'gamma': gamma,'gcd': gcd,'hypot': hypot,'inf': inf,'isclose': isclose,'isfinite': isfinite,'isinf': isinf,'isnan': isnan,'ldexp': ldexp,'lgamma': lgamma,'log': log,'log10': log10,'log1p': log1p,'log2': log2,'modf': modf,'nan': nan,'pi': pi,'pow': pow,'radians': radians,'sin': sin,'sinh': sinh,'sqrt': sqrt,'tan': tan,'tanh': tanh,'trunc': trunc})
          x=r*cos(T)
          y=r*sin(T)
          v1=adsk.core.Vector3D.create()
          v1.add(xbasis)
          v2=adsk.core.Vector3D.create()
          v2.add(ybasis)
          v1.scaleBy(x)
          v2.scaleBy(y)
          point=origin
          point.translateBy(v1)
          point.translateBy(v2)
          point=adsk.core.Point3D.create(p[1],p[2],p[3])
          point.translateBy(v1)
          point.translateBy(v2)
          pnts.add(point)
          actSketch.sketchPoints.add(point)
         
        elif str(list1) == 'Cartesian':
         Equ = inputs.itemById('equa_car').value
         Equ=Equ.replace('^','**')
         xmi=inputs.itemById('xmin').value
         xma=inputs.itemById('xmax').value
         for i in range(0, n+1):
          x=xmi*(1-i/n)+(i/n)*xma
          y=eval(Equ,{"__builtins__":None},{'x': x,'acos': acos,'acosh': acosh,'asin': asin,'asinh': asinh,'atan': atan,'atan2': atan2,'atanh': atanh,'ceil': ceil,'copysign': copysign,'cos': cos,'cosh': cosh,'degrees': degrees,'e': e,'erf': erf,'erfc': erfc,'exp': exp,'expm1': expm1,'fabs': fabs,'factorial': factorial,'floor': floor,'fmod': fmod,'frexp': frexp,'fsum': fsum,'gamma': gamma,'gcd': gcd,'hypot': hypot,'inf': inf,'isclose': isclose,'isfinite': isfinite,'isinf': isinf,'isnan': isnan,'ldexp': ldexp,'lgamma': lgamma,'log': log,'log10': log10,'log1p': log1p,'log2': log2,'modf': modf,'nan': nan,'pi': pi,'pow': pow,'radians': radians,'sin': sin,'sinh': sinh,'sqrt': sqrt,'tan': tan,'tanh': tanh,'trunc': trunc})
          v1=adsk.core.Vector3D.create()
          v1.add(xbasis)
          v2=adsk.core.Vector3D.create()
          v2.add(ybasis)
          v1.scaleBy(x)
          v2.scaleBy(y)
          point=origin
          point.translateBy(v1)
          point.translateBy(v2)
          point=adsk.core.Point3D.create(p[1],p[2],p[3])
          point.translateBy(v1)
          point.translateBy(v2)
          pnts.add(point)
          actSketch.sketchPoints.add(point)
        elif str(list1) == 'Parametric':
           Equ = inputs.itemById('equa_px').value
           Equ=Equ.replace('^','**')
           Equ_y= inputs.itemById('equa_py').value
           Equ_y=Equ_y.replace('^','**')
           xmi=inputs.itemById('tmin').value
           xma=inputs.itemById('tmax').value
           for i in range(0, n+1):
            T=xmi*(1-i/n)+(i/n)*xma
            x=eval(Equ,{"__builtins__":None},{'t': T,'T': T,'acos': acos,'acosh': acosh,'asin': asin,'asinh': asinh,'atan': atan,'atan2': atan2,'atanh': atanh,'ceil': ceil,'copysign': copysign,'cos': cos,'cosh': cosh,'degrees': degrees,'e': e,'erf': erf,'erfc': erfc,'exp': exp,'expm1': expm1,'fabs': fabs,'factorial': factorial,'floor': floor,'fmod': fmod,'frexp': frexp,'fsum': fsum,'gamma': gamma,'gcd': gcd,'hypot': hypot,'inf': inf,'isclose': isclose,'isfinite': isfinite,'isinf': isinf,'isnan': isnan,'ldexp': ldexp,'lgamma': lgamma,'log': log,'log10': log10,'log1p': log1p,'log2': log2,'modf': modf,'nan': nan,'pi': pi,'pow': pow,'radians': radians,'sin': sin,'sinh': sinh,'sqrt': sqrt,'tan': tan,'tanh': tanh,'trunc': trunc})
            y=eval(Equ_y,{"__builtins__":None},{'t': T,'T': T,'acos': acos,'acosh': acosh,'asin': asin,'asinh': asinh,'atan': atan,'atan2': atan2,'atanh': atanh,'ceil': ceil,'copysign': copysign,'cos': cos,'cosh': cosh,'degrees': degrees,'e': e,'erf': erf,'erfc': erfc,'exp': exp,'expm1': expm1,'fabs': fabs,'factorial': factorial,'floor': floor,'fmod': fmod,'frexp': frexp,'fsum': fsum,'gamma': gamma,'gcd': gcd,'hypot': hypot,'inf': inf,'isclose': isclose,'isfinite': isfinite,'isinf': isinf,'isnan': isnan,'ldexp': ldexp,'lgamma': lgamma,'log': log,'log10': log10,'log1p': log1p,'log2': log2,'modf': modf,'nan': nan,'pi': pi,'pow': pow,'radians': radians,'sin': sin,'sinh': sinh,'sqrt': sqrt,'tan': tan,'tanh': tanh,'trunc': trunc})
            v1=adsk.core.Vector3D.create()
            v1.add(xbasis)
            v2=adsk.core.Vector3D.create()
            v2.add(ybasis)
            v1.scaleBy(x)
            v2.scaleBy(y)
            point=origin
            point.translateBy(v1)
            point.translateBy(v2)
            point=adsk.core.Point3D.create(p[1],p[2],p[3])
            point.translateBy(v1)
            point.translateBy(v2)
            pnts.add(point)
            actSketch.sketchPoints.add(point)
           

        actSketch.sketchCurves.sketchFittedSplines.add(pnts)
        cmdDef = ui.commandDefinitions.itemById('Spline_Derived_Euations')
        if cmdDef:
            cmdDef.deleteMe()
            
        adsk.terminate() 
       except:
         if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        cmddefs=ui.commandDefinitions
        Spline_buttton=cmddefs.itemById('spline_derived_euations')
        if not Spline_buttton:
          Spline_buttton=cmddefs.addButtonDefinition('Spline_Derived_Euations','Equation Derived Spline','make a spline from an equation')
        onExecute = MyExecuteHandler()
        Spline_buttton.commandCreated.add(onExecute)
        _handlers.append(onExecute)
        Spline_buttton.execute()
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
def stop(context):
    try:    
        
        # Delete the command definition.
        cmdDef = ui.commandDefinitions.itemById('Spline_Derived_Euations')
        if cmdDef:
            cmdDef.deleteMe()            
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
