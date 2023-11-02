import re
import argparse

import shlex
from Utilities.Utilities import printConsole,printError
from DiskManagement.DiskManagement import *
from FileSystem.FileSystem import *
from User.User import *
from Rep.rep import *

def Commands(data):
   print(data)
   printConsole(" ---- Bienvenido al Sistema de Archivos de  - 202000119 ---- ")
   arr = data

   response = ""
   for command in arr:
      command = re.sub(r"[#][^\n]*", "", command)
      if command == "": continue
      elif re.search("[e|E][x|X][i|I][t|T]", command): break
      response += AnalyzeType(command) + "\n"

   printConsole("... Saliendo del programa ...")
   return response
   

def AnalyzeType(entry):
   try:
      entry= entry.lower()
      printConsole("Analizando comando: " + entry)
      split_args = shlex.split(entry)
      command = split_args.pop(0)
      if(command == "mkdisk"):
         print(" ------ Se dectecto mkdisk ------ ")
         return fn_mkdisk(split_args)
      elif(command == "rmdisk"):
         print(" ------ Se dectecto rmdisk ------ ")
         return fn_rmdisk(split_args)
         print(" ------ Termino rmdisk ------ ")
      elif(command == "fdisk"):
         print(" ------ Se dectecto fdisk ------ ")
         return fn_fdisk(split_args)
         print(" ------ Termino fdisk ------ ")
      elif(command == "mount"):
         print(" ------ Se dectecto mount ------ ")
         return fn_mount(split_args)
         print(" ------ Termino mount ------ ")
      elif(command == "mkfs"):
         print(" ------ Se dectecto mkfs ------ ")
         return fn_mkfs(split_args)
         print(" ------ Termino mkfs ------ ")
      elif(command == "login"):
         print(" ------ Se dectecto login ------ ")
         return fn_login(split_args)
         print(" ------ Termino login ------ ")
      elif(command=="rep"):
         print( " ------ Se dectecto rep ------ ")
         return rep(split_args)
   except Exception as e: pass
def fn_rmdisk(split_args):
        try:
            parser = argparse.ArgumentParser(description="Parámetros")
            parser.add_argument("-path", required=True)
            args = parser.parse_args(split_args)
            def confirmar(mensaje):
                respuesta = input(f"{mensaje} (y/n)\n\t").lower()
                return respuesta == "y"
            if os.path.isfile(args.path):
                if not args.path.endswith(".dsk"):
                    return("\tERROR: Extensión de archivo no válida para la eliminación del Disco.") 
                else:
                    os.remove(args.path)
                    return("Disco "+args.path+" eliminado exitosamente ") 
                 
            else:
                return("ERROR: El disco "+args.path+"  no existe en la ruta indicada.") 
            
        except SystemExit: print("Análisis de argumentos")
        except Exception as e: print(str(e))
        
def fn_login(split_args):
   try:
      parser = argparse.ArgumentParser(description="Parámetros")
      parser.add_argument("-user", required=True)
      parser.add_argument("-pass", required=True)
      parser.add_argument("-id", required=True)
      args = parser.parse_args(split_args)

      return login(args)

   except SystemExit: printError("Análisis de argumentos")
   except Exception as e: printError(str(e))

def fn_mkfs(split_args):
   try:
      parser = argparse.ArgumentParser(description="Parámetros")
      parser.add_argument("-id", required=True)
      parser.add_argument("-type")
      parser.add_argument("-fs", default='2')
      args = parser.parse_args(split_args)
      args.fs = args.fs[:1]

      return mkfs(args)

   except SystemExit: printError("Análisis de argumentos")
   except Exception as e: printError(str(e))


def fn_mount(split_args):
   try:
      parser = argparse.ArgumentParser(description="Parámetros")
      parser.add_argument("-path", required=True)
      parser.add_argument("-name", required=True)
      args = parser.parse_args(split_args)

      return mount(args)

   except SystemExit: printError("Análisis de argumentos")
   except Exception as e: printError(str(e))


def fn_fdisk(split_args):
   try:
      parser = argparse.ArgumentParser(description="Parámetros")
      parser.add_argument("-size", type=int)
      parser.add_argument("-path", required=True)
      parser.add_argument("-name", required=True)
      parser.add_argument("-unit", default='k')
      parser.add_argument("-type", default='p')
      parser.add_argument("-fit", default='w')
      parser.add_argument("-delete")
      parser.add_argument("-add")
      args = parser.parse_args(split_args)

      args.fit = args.fit[:1]

      if args.unit is not None:
         if args.unit not in ["k","m","b"]: raise Exception("El parametro unit solo puede ser k o m o b")


      return fdisk(args)

   except SystemExit: printError("Análisis de argumentos")
   except Exception as e: printError(str(e))


def fn_mkdisk(split_args):
   try:
      parser = argparse.ArgumentParser(description="Parámetros")
      parser.add_argument("-size", type=int, required=True)
      parser.add_argument("-path", required=True)
      parser.add_argument("-fit", default='f')
      parser.add_argument("-unit", default='m')
      args = parser.parse_args(split_args)

      args.fit = args.fit[:1]

      if args.fit not in ["b","f","w"]: raise Exception("El parametro fit solo puede ser b, f o w")
      if args.unit not in ["k","m"]: raise Exception("El parametro unit solo puede ser k o m")
      
      if re.search("[.][d|D][s|S][k|K]",args.path) is None: raise Exception("La extensión del archivo debe ser .dsk")

      return mkdisk(args)

   except SystemExit: printError("Análisis de argumentos")
   except Exception as e: printError(str(e))

  

      
      

