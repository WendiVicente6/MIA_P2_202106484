import os
import sys
import struct
import time
from Objects.MBR import *
from Objects.EBR import *
from Objects.Superblock import *
from objects.Fileblock import *
from Objects.Inode import *
from Objects.Folderblock import *
from Global.Global import mounted_partitions

def count_logica(self, path, NParticionE):
    contar = 0
    archivo = open(path, "rb+")
    master = MBR()
    Extendida=EBR()
    archivo.seek(0)
    master_data = archivo.read(struct.calcsize("=i"))
    master.unpack(master_data)
    archivo.seek(master.partitions[NParticionE].start)
    extendida_data = archivo.read(struct.calcsize("=i"))
    if master.part_next != -1:
        while archivo.tell() < master.partitions[NParticionE].size + master.partitions[NParticionE].start:
            contar += 1
            contar += 1
            if Extendida.part_next == -1:
                break
            archivo.seek(Extendida.part_next)
            extendida_data = archivo.read(struct.calcsize("=i"))
            Extendida.unpack(extendida_data)
    return contar

def two_decimal(num):
    aux = str(num)
    back = aux[-1]
    while back == '0':
        aux = aux[:-1]
        back = aux[-1]
    return aux

def get_date(creacion):
    hora = ""
    tm = time.localtime(creacion)
    fecha = time.strftime("%d/%m/%y %H:%M", tm)
    hora = fecha
    return hora

def get_extension(path):
    Carpeta = path
    ext = ""
    while True:
        aux = Carpeta[-1]
        if aux == '.':
            break
        ext = Carpeta[-1] + ext
        Carpeta = Carpeta[:-1]
    return ext

def make_mbr(pathRep, path):
    archivo = open(path, "rb+")
    master = MBR()
    archivo.seek(0, 0)
    master = archivo.read(len(MBR))
    file = open("./reportes/reporte.dot", "w")
    if file.fail():
        print("Error no se pudo abrir el archivo")
        return
    file.write("digraph G{\n" + "node[shape=plaintext]\n" + "concentrate=true\n" + "ReporteMBR[label=<\n")
    file.write("<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\" >\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"4\" BORDER = \"1\">REPORTE DE MBR</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">size</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(master.size) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">mbr_fecha_creacion</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + get_date(master.mbr_fecha_creacion) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">mbr_disk_signature</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(master.mbr_disk_signature) + "</TD>\n" + "</TR>\n")
    NPartE = -1
    for i in range(4):
        if master.partitions[i].start != -1:
            status = ""
            type = ""
            fit = ""
            status = master.partitions[i].status
            type = master.partitions[i].type
            fit = master.partitions[i].type
            name = master.partitions[i].name
            if type == "P" or type == "E":
                file.write("<TR bgcolor=\"blue3\">\n" + "<TD COLSPAN=\"4\" BORDER = \"1\">Particion</TD>\n" + "</TR>\n")
            else:
                file.write("<TR>\n" + "<TD COLSPAN=\"4\" BORDER = \"1\">Particion Logica</TD>\n" + "</TR>\n")
            file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">status</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + status + "</TD>\n" + "</TR>\n")
            file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">type</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + type + "</TD>\n" + "</TR>\n")
            file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">part_fit</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + fit + "</TD>\n" + "</TR>\n")
            file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">start</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(master.partitions[i].start) + "</TD>\n" + "</TR>\n")
            file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">size</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(master.partitions[i].size) + "</TD>\n" + "</TR>\n")
            file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">name</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + name + "</TD>\n" + "</TR>\n")
        if master.partitions[i].type == 'E':
            NPartE = i
    file.write("</TABLE>>]\n")


    if (NPartE!= -1):
        EBR_Extendida = EBR()
        archivo.seek(master.partitions[NPartE].start, 0)
        archivo.readinto(EBR_Extendida)
        i = 1
        if (EBR_Extendida.part_next != -1):
            file.write("EBR[label=<\n")
            file.write("<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\" >\n")
            while (archivo.tell() < (master.partitions[NPartE].size + master.partitions[NPartE].start)):
                comprobar = EBR_Extendida.part_next - (EBR_Extendida.start + EBR_Extendida.size)
                if (comprobar > 0):
                    status = ""
                    status = EBR_Extendida.status
                    fit = ""
                    fit = EBR_Extendida.part_fit
                    name = EBR_Extendida.name.decode().strip('\x00')
                    file.write("<TR>\n" + "<TD COLSPAN=\"4\" BORDER = \"1\">Particion</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">status</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + status + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">part_fit</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + fit + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">start</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(EBR_Extendida.start) + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">size</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(EBR_Extendida.size) + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">part_next</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(EBR_Extendida.part_next - comprobar) + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">name</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + name + "</TD>\n" + "</TR>\n")
                    i += 1
                    fits = ""
                    fits = EBR_Extendida.part_fit
                    file.write("<TR>\n" + "<TD COLSPAN=\"4\" BORDER = \"1\">Particion</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">status</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">1</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">part_fit</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + fits + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">start</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(EBR_Extendida.part_next - EBR_Extendida.size) + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">size</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(comprobar) + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">part_next</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(EBR_Extendida.part_next) + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">name</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\"></TD>\n" + "</TR>\n")
                else:
                    status = ""
                    status = EBR_Extendida.status
                    fit = ""
                    fit = EBR_Extendida.part_fit
                    name = EBR_Extendida.name.decode().strip('\x00')
                    file.write("<TR>\n" + "<TD COLSPAN=\"4\" BORDER = \"1\">Particion</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">status</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + status + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">part_fit</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + fit + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">start</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(EBR_Extendida.start) + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">size</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(EBR_Extendida.size) + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">part_next</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(EBR_Extendida.part_next) + "</TD>\n" + "</TR>\n")
                    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">name</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + name + "</TD>\n" + "</TR>\n")
                if (EBR_Extendida.part_next == -1):
                    break
                i += 1
                archivo.seek(EBR_Extendida.part_next, 0)
                archivo.readinto(EBR_Extendida)
        file.write("</TABLE>>]\n")
    file.write("}")
    file.close()
    extension = "sudo dot -T " + get_extension(pathRep) + " ./reportes/reporte.dot -o " + pathRep
    os.system(extension)
    archivo.close()
    if archivo == open(pathRep, "rb+"):
        print("[Success] > Se creo correctamente el reporte mbr")
        archivo.close()
    else:
        print("[Error] > No fue posible crear el reporte mbr")

def make_disk(pathRep, path):
    master = MBR()
    archivo = open(path, "rb+")
    archivo.seek(0, 0)
    archivo.readinto(master)
    file = open("./reportes/reporte.dot", "w")
    if (file.fail()):
        print("Error no se pudo abrir el archivo")
        return
    file.write("digraph G{\n" + "node[shape=plaintext]\n" + "concentrate=true\n" + "ReporteDISK[label=<\n")
    file.write("<TABLE BORDER=\"2\" CELLBORDER=\"1\" CELLSPACING=\"2\" >\n")
    file.write("<TR>\n<TD COLSPAN=\"1\" ROWSPAN = \"2\" BORDER = \"1\">MBR</TD>\n")
    NParticionE = -1
    tamTotal = 0
    for i in range(4):
        if (master.partitions[i].type == 'P'):
            tamTotal += master.partitions[i].size
            sizePrimaria = ((master.partitions[i].size)*100)/master.size
            file.write("<TD COLSPAN=\"1\" ROWSPAN = \"2\" BORDER = \"1\">Primaria <BR/> " + two_decimal(sizePrimaria) + "\% del disco</TD>\n")
            if (i != 3):
                comprobar = master.partitions[i+1].start - (master.partitions[i].size+master.partitions[i].start)
                if (comprobar > 0):
                    sizeLibre = (comprobar*100)/master.size
                    file.write("<TD COLSPAN=\"1\" ROWSPAN = \"2\" BORDER = \"1\">Libre <BR/> " + two_decimal(sizeLibre) + "\% del disco</TD>\n")
            else:
                comprobar = (master.size+len(MBR)) - (master.partitions[i].size+master.partitions[i].start)
                if (comprobar > 0):
                    libre = comprobar
                    sizeLibre = (libre*100)/master.size
                    file.write("<TD COLSPAN=\"1\" ROWSPAN = \"2\" BORDER = \"1\">Libre <BR/> " + two_decimal(sizeLibre) + "\% del disco</TD>\n")
        elif (master.partitions[i].type == 'E'):
            tamTotal += master.partitions[i].size
            cont = count_logica(path, i)
            if (cont == 0):
                sizeExtendida = ((master.partitions[i].size)*100)/master.size
                file.write("<TD COLSPAN=\"1\" ROWSPAN = \"2\" BORDER = \"1\">Extendida <BR/> " + two_decimal(sizeExtendida) + "\% del disco</TD>\n")
            else:
                file.write("<TD COLSPAN=\"" + str(cont+1) + "\" ROWSPAN = \"1\" BORDER = \"1\">Extendida</TD>\n")
                NParticionE = i
            if (i != 3):
                comprobar = master.partitions[i+1].start - (master.partitions[i].size+master.partitions[i].start)
                if (comprobar > 0):
                    sizeLibre = (comprobar*100)/master.size
                    file.write("<TD COLSPAN=\"1\" ROWSPAN = \"2\" BORDER = \"1\">Libre <BR/> " + two_decimal(sizeLibre) + "\% del disco</TD>\n")
            else:
                comprobar = (master.size+len(MBR)) - (master.partitions[i].size+master.partitions[i].start)
                if (comprobar > 0):
                    libre = comprobar
                    sizeLibre = (libre*100)/master.size
                    file.write("<TD COLSPAN=\"1\" ROWSPAN = \"2\" BORDER = \"1\">Libre <BR/> " + two_decimal(sizeLibre) + "\% del disco</TD>\n")
    file.write("</TR>\n")
    if (NParticionE != -1):
        file.write("<TR>\n")
        Extendida = EBR()
        total = master.size
        totalEx = master.partitions[NParticionE].size
        archivo.seek(master.partitions[NParticionE].start, 0)
        archivo.readinto(Extendida)
        totalLogic = 0
        if (Extendida.part_next != -1):
            while (archivo.tell() < master.partitions[NParticionE].size + master.partitions[NParticionE].start):
                totalLogic += float(Extendida.size)
                if (Extendida.status == '1'):
                    sizeLibre = float(Extendida.size*100)/total
                    file.write("<TD>Libre <BR/> " + two_decimal(sizeLibre) + "\% del disco</TD>\n")
                else:
                    file.write("<TD>EBR</TD>\n")
                    sizeLogica = float(Extendida.size*100)/total
                    file.write("<TD>Logica <BR/> " + two_decimal(sizeLogica) + "\% del disco</TD>\n")
                if (Extendida.part_next == -1):
                    break
                aux = Extendida.part_next - (Extendida.start + Extendida.size)
                if (aux > 0):
                    sizeLibre = (aux*100)/total
                    file.write("<TD>Libre <BR/> " + two_decimal(sizeLibre) + "\% del disco</TD>\n")
                archivo.seek(Extendida.part_next, 0)
                archivo.readinto(Extendida)
        comprobar = float(totalEx) - totalLogic
        if (comprobar > 0):
            sizeLibre = (comprobar*100)/(total)
            file.write("<TD>Libre <BR/>" + two_decimal(sizeLibre) + "\% del disco</TD>\n")
        file.write("</TR>\n")
    file.write("</TABLE>>]\n}")
    file.close()
    extension = "dot -T " + get_extension(pathRep)+ " ./reportes/reporte.dot -o "+pathRep
    os.system(extension)
    archivo.close()
    if archivo == open(pathRep, "rb+"):
        print("[Success] > Se creo correctamente el reporte disk")
        archivo.close()
    else:
        print("[Error] > No fue posible crear el reporte mbr")

def make_bm_block(pathRep, path, name):
    master = MBR()
    archivo = open(path, "rb+")
    archivo.seek(0, 0)
    archivo.readinto(master)
    
    bloquesito = Superblock()
    start = get_partition_start(path, name, master)
    archivo.seek(start, 0)
    archivo.readinto(bloquesito)
    
    file = open("./reportes/reporte.dot", "w")
    if (file.fail()):
        print("Error no se pudo abrir el archivo")
        return
    
    file.write("digraph G{\n" + "node[shape=plaintext]\n" + "concentrate=true\n" + "ReporteMBR[label=<\n")
    
    file.write("<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\" >\n")
    
    indice = 0
    status = ""
    archivo.seek(bloquesito.s_bm_block_start, 0)
    for i in range(bloquesito.s_block_count):
        status = archivo.read(1)
        if (indice == 0): file.write("<TR>\n")
        file.write("<TD COLSPAN=\"2\" BORDER = \"1\">" + status.decode() + " | B | " + str(i+1) + "</TD>\n")
        indice += 1
        if (indice == 10): 
            file.write("</TR>\n")
            indice = 0
    if (indice > 0):
        file.write("</TR>\n")
    
    file.write("</TABLE>>]\n")
    file.write("}")
    file.close()
    
    extension = "sudo dot -T " + get_extension(pathRep) + " ./reportes/reporte.dot -o " + pathRep
    os.system(extension)
    archivo.close()
    if archivo == open(pathRep, "rb+"):
        print("[Success] > Se creo correctamente el reporte bm_block")
        archivo.close()
    else:
        print("[Error] > No fue posible crear el reporte bm_block")

def make_bm_inode(pathRep, path, name):
    master = MBR()
    archivo = open(path, "rb+")
    archivo.seek(0, 0)
    archivo.readinto(master)
    
    bloquesito = Superblock()
    start = get_partition_start(path, name, master)
    archivo.seek(start, 0)
    archivo.readinto(bloquesito)
    
    file = open("./reportes/reporte.dot", "w")
    if (file.fail()):
        print("Error no se pudo abrir el archivo")
        return
    
    file.write("digraph G{\n" + "node[shape=plaintext]\n" + "concentrate=true\n" + "ReporteMBR[label=<\n")
    
    file.write("<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\" >\n")
    
    indice = 0
    status = ""
    archivo.seek(bloquesito.s_bm_inode_start, 0)
    for i in range(bloquesito.s_inodes_count):
        status = archivo.read(1)
        if (indice == 0): file.write("<TR>\n")
        file.write("<TD COLSPAN=\"2\" BORDER = \"1\">" + status.decode() + " | I | " + str(i+1) + "</TD>\n")
        indice += 1
        if (indice == 10): 
            file.write("</TR>\n")
            indice = 0
    if (indice > 0):
        file.write("</TR>\n")
    
    file.write("</TABLE>>]\n")
    file.write("}")
    file.close()
    
    extension = "sudo dot -T " + get_extension(pathRep) + " ./reportes/reporte.dot -o " + pathRep
    os.system(extension)
    archivo.close()
    if archivo == open(pathRep, "rb+"):
        print("[Success] > Se creo correctamente el reporte bm_inode")
        archivo.close()
    else:
        print("[Error] > No fue posible crear el reporte bm_inode")



def make_sb(pathRep, path, name):
    
    master = MBR()
    archivo = open(path, "rb+")
    archivo.seek(0, 0)
    master = archivo.read(len(MBR))
    
    bloquesito = Superblock()
    start = get_partition_start(path, name, master)
    archivo.seek(start, 0)
    bloquesito = archivo.read(len(Superblock))
    
    file = open("./reportes/reporte.dot", "w")
    if file.fail():
        print("Error no se pudo abrir el archivo")
        return
    
    file.write("digraph G{\n" + "node[shape=plaintext]\n" + "concentrate=true\n" + "ReporteMBR[label=<\n")
    
    file.write("<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\" >\n")
    
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_inodes_count</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_inodes_count) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_blocks_count</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_block_count) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_free_blocks_count</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_free_blocks_count) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_free_inodes_count</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_free_inodes_count) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_mtime</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + get_date(bloquesito.s_mtime) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_umtime</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + get_date(bloquesito.s_umtime) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_mnt_count</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_mnt_count) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_magic</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_magic) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_inode_size</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_inode_size) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_block_size</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_block_size) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_first_ino</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_first_ino) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_first_blo</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_first_blo) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_bm_inode_start</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_bm_inode_start) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_bm_block_start</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_bm_block_start) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_inode_start</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_inode_start) + "</TD>\n" + "</TR>\n")
    file.write("<TR>\n" + "<TD COLSPAN=\"2\" BORDER = \"1\">s_block_start</TD>\n" + "<TD COLSPAN=\"2\" BORDER =\"1\">" + str(bloquesito.s_block_start) + "</TD>\n" + "</TR>\n")
    
    file.write("</TABLE>>]" + "\n")
    file.write("}")
    file.close()
    
    extension = "sudo dot -T " + get_extension(pathRep) + " ./reportes/reporte.dot -o " + pathRep
    os.system(extension)
    archivo.close()
    if archivo == open(pathRep, "rb+"):
        print("[Success] > Se creo correctamente el reporte sb\n")
        archivo.close()
    else:
        print("[Error] > No fue posible crear el reporte sb\n")

def graph_inode(start_inodo, path, pathRep):
    
    inodo = Inode()
    archivo = open(path, "rb+")
    archivo.seek(start_inodo, 0)
    inodo = archivo.read(len(Inode))
    archivo.close()
    
    archivo.write("\"node" + str(start_inodo) + "\" [label = \"")
    archivo.write("<f0> INODO " + str(start_inodo) + " |")
    for i in range(15):
        archivo.write("<f" + str(i+1) + "> " + str(inodo.i_block[i]))
        if i < 14:
            archivo.write("|")
    archivo.write("\"shape = \"record\"];" + "\n")
    
    for i in range(15):
        if i < 12:
            if inodo.i_block[i] != -1:
                
                if inodo.i_type == '0':
                    
                    start_block = inodo.i_block[i]
                    
                    carpetita = Folderblock()
                    archivo = open(path, "rb+")
                    archivo.seek(start_block, 0)
                    carpetita = archivo.read(len(Folderblock))
                    archivo.close()
                    
                    archivo.write("\"node" + str(start_block) + "\" [label = \"")
                    archivo.write("<f0> BLOQUE DE CARPETA " + str(start_block) + " |")
                    for i in range(4):
                        archivo.write("<f" + str(i+1) + "> [" + carpetita.b_content[i].b_name + "] ---- [" + carpetita.b_content[i].b_inodo + "]")
                        if i < 3:
                            archivo.write("|")
                    archivo.write("\"shape = \"record\"];" + "\n")
                    
                    archivo.write("\"node" + str(start_inodo) + "\":f" + str(i+1) + " -> \"node" + str(start_block) + "\":f0;" + "\n")
                    
                    for i in range(1, 4):
                        if carpetita.b_content[i].b_inodo != -1:
                            
                            graph_inode(carpetita.b_content[i].b_inodo, path, pathRep)
                            
                            archivo.write("\"node" + str(start_block) + "\":f" + str(i+1) + " -> \"node" + str(carpetita.b_content[i].b_inodo) + "\":f0;" + "\n")
                else:
                    
                    start_block = inodo.i_block[i]
                    
                    archivito = Fileblock()
                    archivo = open(path, "rb+")
                    archivo.seek(start_block, 0)
                    archivito = archivo.read(len(Fileblock))
                    archivo.close()
                    
                    archivo.write("\"node" + str(start_block) + "\" [label = \"")
                    archivo.write("<f0> BLOQUE DE ARCHIVO " + str(start_block) + " |")
                    archivo.write("<f1> [" + archivito.b_name + "] |")
                    archivo.write("<f2> [" + archivito.b_content + "]")
                    archivo.write("\"shape = \"record\"];" + "\n")
                    
                    archivo.write("\"node" + str(start_inodo) + "\":f" + str(i+1) + " -> \"node" + str(start_block) + "\":f0;" + "\n")
        elif i == 12:
            if inodo.i_block[i] != -1:
                
                start_pointer = inodo.i_block[i]
                
                apuntadores = BloqueApuntador()
                archivo = open(path, "rb+")
                archivo.seek(start_pointer, 0)
                apuntadores = archivo.read(len(BloqueApuntador))
                archivo.close()
                
                archivo.write("\"node" + str(start_pointer) + "\" [label = \"")
                archivo.write("<f0> BLOQUE DE APUNTADORES " + str(start_pointer) + " |")
                for i in range(16):
                    archivo.write("<f" + str(i+1) + "> " + str(apuntadores.b_pointers[i]))
                    if i < 15:
                        archivo.write("|")
                archivo.write("\"shape = \"record\"];" + "\n")
                
                archivo.write("\"node" + str(start_inodo) + "\":f" + str(i+1) + " -> \"node" + str(start_pointer) + "\":f0;" + "\n")
                
                for i in range(16):
                    if apuntadores.b_pointers[i] != -1:
                        
                        if inodo.i_type == '0':
                            
                            start_block = apuntadores.b_pointers[i]
                            
                            carpetita = Folderblock()
                            archivo = open(path, "rb+")
                            archivo.seek(start_block, 0)
                            carpetita = archivo.read(len(Folderblock))
                            archivo.close()
                            
                            archivo.write("\"node" + str(start_block) + "\" [label = \"")
                            archivo.write("<f0> BLOQUE DE CARPETA " + str(start_block) + " |")
                            for i in range(4):
                                archivo.write("<f" + str(i+1) + "> [" + carpetita.b_content[i].b_name + "] ---- [" + carpetita.b_content[i].b_inodo + "]")
                                if i < 3:
                                    archivo.write("|")
                            archivo.write("\"shape = \"record\"];" + "\n")
                            
                            archivo.write("\"node" + str(start_inodo) + "\":f" + str(i+1) + " -> \"node" + str(start_block) + "\":f0;" + "\n")
                            
                            for i in range(1, 4):
                                if carpetita.b_content[i].b_inodo != -1:
                                    
                                    graph_inode(carpetita.b_content[i].b_inodo, path, pathRep)
                                    
                                    archivo.write("\"node" + str(start_block) + "\":f" + str(i+1) + " -> \"node" + str(carpetita.b_content[i].b_inodo) + "\":f0;" + "\n")
                        else:
                            print("entraste aca?")
                            
                            start_block = apuntadores.b_pointers[i]
                            
                            archivito = Fileblock()
                            archivo = open(path, "rb+")
                            archivo.seek(start_block, 0)
                            archivito = archivo.read(len(Fileblock))
                            archivo.close()
                            
                            archivo.write("\"node" + str(start_block) + "\" [label = \"")
                            archivo.write("<f0> BLOQUE DE ARCHIVO " + str(start_block) + " |")
                            archivo.write("<f1> [" + archivito.b_name + "] |")
                            archivo.write("<f2> [" + archivito.b_content + "]")
                            archivo.write("\"shape = \"record\"];" + "\n")
                            
                            archivo.write("\"node" + str(start_inodo) + "\":f" + str(i+1) + " -> \"node" + str(start_block) + "\":f0;" + "\n")
        elif i == 13:
            pass
        elif i == 14:
            pass

def make_tree(pathRep, path, name):
    
    archivo = open(path, "rb+")
    archivo.seek(0, os.SEEK_SET)
    master = MBR()
    master_data = archivo.read(struct.calcsize("=i"))
    master_values = struct.unpack("=i", master_data)
    master.value = master_values[0]
    
    bloquesito = Superblock()
    start = get_partition_start(path, name, master)
    archivo.seek(start, os.SEEK_SET)
    bloquesito_data = archivo.read(struct.calcsize("=i"))
    bloquesito_values = struct.unpack("=i", bloquesito_data)
    bloquesito.value = bloquesito_values[0]
    
    archivo = open("./reportes/reporte.dot", "w")
    if archivo.fail():
        print("Error no se pudo abrir el archivo")
        return
    
    archivo.write("digraph g {\n")
    archivo.write("fontname=\"Helvetica,Arial,sans-serif\"\n")
    archivo.write("node [fontname=\"Helvetica,Arial,sans-serif\"]\n")
    archivo.write("edge [fontname=\"Helvetica,Arial,sans-serif\"]\n")
    archivo.write("graph [rankdir = \"LR\"];\n")
    archivo.write("node [fontsize = \"16\" shape = \"ellipse\"];\n")
    archivo.write("edge [];\n")
    
    graph_inode(bloquesito.s_inode_start, path, pathRep)
    
    archivo.write("}")
    archivo.close()
    
    extension = "sudo dot -T " + get_extension(pathRep) + " ./reportes/reporte.dot -o " + pathRep
    os.system(extension)
    archivo.close()
    if archivo == open(pathRep, "rb+"):
        print("[Success] > Se creo correctamente el reporte tree\n")
        archivo.close()
    else:
        print("[Error] > No fue posible crear el reporte tree\n")









def make_file(pathRep, path, name, rutaString):

    def get_partition_start(path, name, master):
        # implementation of get_partition_start function
        pass
    
    def search_path(token, inode_start, path, count_tokens):
        # implementation of search_path function
        pass
    
    def get_count_tokens(token, count):
        # implementation of get_count_tokens function
        pass
    
    def make_file_report(pathRep, path, name, rutaCopia1, rutaCopia2, master, bloquesito, inodo):
        archivo = open("./reportes/reporte.dot", "w")
        if archivo:
            archivo.write("digraph g {\n")
            archivo.write("node [shape=record fontname=Arial];\n")
            
            archivo.write("a  [label=\"")
            for i in range(15):
                if i < 12:
                    if inodo.i_block[i] != -1:
                        archivito = Fileblock()
                        archivo = open(path, "rb+")
                        if archivo:
                            archivo.seek(inodo.i_block[i], os.SEEK_SET)
                            archivito_data = archivo.read(struct.calcsize("Fileblock"))
                            archivito_data = struct.unpack("Fileblock", archivito_data)
                            archivito.__dict__.update(archivito_data._asdict())
                            archivo.write(archivito.b_content + "\\l\n")
                        archivo.close()
            archivo.write("\"]")
            
            archivo.write("}")
            archivo.close()
            
            extension = "sudo dot -T " + get_extension(pathRep) + " ./reportes/reporte.dot -o " + pathRep
            os.system(extension)
            
            archivo = open(path, "rb+")
            if archivo:
                print("[Success] > Se creo correctamente el reporte file")
                archivo.close()
            else:
                print("[Error] > No fue posible crear el reporte file")
    
    master = MBR()
    archivo = open(path, "rb+")
    if archivo:
        archivo.seek(0, os.SEEK_SET)
        master_data = archivo.read(struct.calcsize("MBR"))
        master_data = struct.unpack("MBR", master_data)
        master.__dict__.update(master_data._asdict())
        
        bloquesito =Superblock()
        start = get_partition_start(path, name, master)
        archivo.seek(start, os.SEEK_SET)
        bloquesito_data = archivo.read(struct.calcsize("Superblock"))
        bloquesito_data = struct.unpack("Superblock", bloquesito_data)
        bloquesito.__dict__.update(bloquesito_data._asdict())
        
        rutaCopia1 = rutaString
        rutaCopia2 = rutaString
        
        ruta = rutaCopia1.encode()
        token = ruta.split(b"/")
        count_tokens = get_count_tokens(token, 0)
        
        ruta = rutaCopia2.encode()
        token = ruta.split(b"/")
        posicion_inodo_carpeta = search_path(token, bloquesito.s_inode_start, path, 0, count_tokens)
        if posicion_inodo_carpeta == -1:
            print("[Error] > No fue posible encontrar la ruta del archivo")
            return
        
        inodo = Inode()
        archivo.seek(posicion_inodo_carpeta, os.SEEK_SET)
        inodo_data = archivo.read(struct.calcsize("Inode"))
        inodo_data = struct.unpack("Inode", inodo_data)
        inodo.__dict__.update(inodo_data._asdict())
        
        make_file_report(pathRep, path, name, rutaCopia1, rutaCopia2, master, bloquesito, inodo)
        
        archivo.close()
    else:
        print("Error no se pudo abrir el archivo")

def make_rep(reportito):
    
    if reportito.path == "":
        print("[Error] > No se ingreso el parametro $path")
        return
    if reportito.name == "":
        print("[Error] > No se ingreso el parametro $name")
        return
    if reportito.id == "":
        print("[Error] > No se ingreso el parametro $id")
        return

             
    if find_partition_in_mount(reportito.id):
        
        nodo = get_partition_in_mount(reportito.id)
        
        file = None
        usaraRaid = False
        copyPath = get_path_raid(nodo.path)
        realPath = nodo.path
        if not file == open(realPath, "r"):
            realPath = copyPath
            usaraRaid = True
        else:
            file.close()
        if usaraRaid:
            if not file == open(realPath, "r"):
                print("[Error] > No se ha encontrado el disco")
                return
            else:
                file.close()
        
        reportito.name = reportito.name.upper()
        
        path_without_name = get_path_without_name(reportito.path)
        if not os.path.exists(path_without_name):
            cmd = "mkdir -p \"" + path_without_name + "\""
            os.system(cmd)
        if reportito.name == "MBR":
            make_mbr(reportito.path, realPath)
        elif reportito.name == "DISK":
            make_disk(reportito.path, realPath)
        elif reportito.name == "BM_BLOCK":
            make_bm_block(reportito.path, realPath, nodo.nombre)
        elif reportito.name == "BM_INODE":
            make_bm_inode(reportito.path, realPath, nodo.nombre)
        elif reportito.name == "SB":
            make_sb(reportito.path, realPath, nodo.nombre)
        elif reportito.name == "TREE":
            make_tree(reportito.path, realPath, nodo.nombre)
        elif reportito.name == "FILE":
            make_file(reportito.path, realPath, nodo.nombre, reportito.ruta)
        else:
            print("No se encuentra este reporte")




