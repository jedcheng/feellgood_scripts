#!/usr/bin/env python3

import math
import gmsh

import numpy as np

class Mediator(object):
    def __init__ (self,radius,thickness, rect_length, mesh_size,surfName,volName):
        """ 
            geometrical cylinder is zero centered, with radius r and length t along (Oz), build by extrusion
            gmsh file format 2.2 is used to write the mesh text file  
        """
        
        self.r = radius
        self.t = thickness
        self.msh_s = mesh_size
        self.length = rect_length
        self.surfName = surfName
        self.volName = volName
        self.withExtraSurf = False

    def addEdgeSurf(self,name1,name2):
        """ optional surfaces : 
        name1 will refer to the base surface, 
        name2 will refer to the translated name1 surface from extrusion """
        self.n1 = name1
        self.n2 = name2
        self.withExtraSurf = True
    
    def make(self,meshFileName):
        """ write cylinder mesh file in gmsh 2.2 text format """
        
        gmsh.initialize()
        gmsh.option.setNumber("General.Terminal",False) # to silent gmsh
        gmsh.model.add("cyl")
        
        p_origin1 = gmsh.model.geo.addPoint(self.r,self.r,-0.5*self.t,self.msh_s)

        start_pt1 = gmsh.model.geo.addPoint(2*self.r, self.r, -0.5*self.t,self.msh_s)
        interim_pt1 = gmsh.model.geo.addPoint(self.r, 2*self.r, -0.5*self.t,self.msh_s)
        interim1_pt1 = gmsh.model.geo.addPoint(0, self.r, -0.5*self.t,self.msh_s)
        interim2_pt1 = gmsh.model.geo.addPoint(self.r,0,-0.5*self.t,self.msh_s)
        end_pt1 = gmsh.model.geo.addPoint(2*self.r, self.r, -0.5*self.t,self.msh_s)

        big_circle_1 = gmsh.model.geo.addCircleArc(start_pt1,p_origin1,interim_pt1)
        big_circle1_1 = gmsh.model.geo.addCircleArc(interim_pt1,p_origin1,interim1_pt1)
        big_circle2_1 = gmsh.model.geo.addCircleArc(interim1_pt1,p_origin1,interim2_pt1)
        big_circle3_1 = gmsh.model.geo.addCircleArc(interim2_pt1,p_origin1,end_pt1)

        curvedLoop1 = gmsh.model.geo.addCurveLoop([big_circle_1,big_circle1_1,
                                    big_circle2_1, big_circle3_1]) # curvedLoop is an index (integer)

        surf1 = gmsh.model.geo.addPlaneSurface([curvedLoop1]) # surf is an index (integer)

        out1 = gmsh.model.geo.extrude([(2,surf1)],0,0,self.t) 
        # 2 is the dimension of the object refered by index surf

        gmsh.model.geo.synchronize() # we have to sync before calling addPhysicalGroup

        volume_tag = 300
        gmsh.model.addPhysicalGroup(3,[out1[1][1]],volume_tag)
        gmsh.model.setPhysicalName(3,volume_tag,self.volName)



        p_origin2 = gmsh.model.geo.addPoint(self.r + self.length ,self.r,-0.5*self.t,self.msh_s)

        start_pt2 = gmsh.model.geo.addPoint(2*self.r + self.length, self.r, -0.5*self.t,self.msh_s)
        interim_pt2 = gmsh.model.geo.addPoint(self.r + self.length, 2*self.r, -0.5*self.t,self.msh_s)
        interim1_pt2 = gmsh.model.geo.addPoint(self.length, self.r, -0.5*self.t,self.msh_s)
        interim2_pt2 = gmsh.model.geo.addPoint(self.r + self.length,0,-0.5*self.t,self.msh_s)
        end_pt2 = gmsh.model.geo.addPoint(2*self.r + self.length, self.r, -0.5*self.t,self.msh_s)

        big_circle_2 = gmsh.model.geo.addCircleArc(start_pt2,p_origin2,interim_pt2)
        big_circle1_2 = gmsh.model.geo.addCircleArc(interim_pt2,p_origin2,interim1_pt2)
        big_circle2_2 = gmsh.model.geo.addCircleArc(interim1_pt2,p_origin2,interim2_pt2)
        big_circle3_2 = gmsh.model.geo.addCircleArc(interim2_pt2,p_origin2,end_pt2)

        curvedLoop2 = gmsh.model.geo.addCurveLoop([big_circle_2,big_circle1_2,
                                    big_circle2_2, big_circle3_2]) # curvedLoop is an index (integer)

        surf2 = gmsh.model.geo.addPlaneSurface([curvedLoop2]) # surf is an index (integer)

        out2 = gmsh.model.geo.extrude([(2,surf2)],0,0,self.t) 
        # 2 is the dimension of the object refered by index surf

        gmsh.model.geo.synchronize() # we have to sync before calling addPhysicalGroup



        volume_tag = 400
        gmsh.model.addPhysicalGroup(3,[out2[1][1]],volume_tag)
        gmsh.model.setPhysicalName(3,volume_tag,self.volName)



        gmsh.model.geo.synchronize() # we have to synchronize before the call to 'generate' to build the mesh





        # generate  a rectangle 

        rect_start = gmsh.model.geo.addPoint(self.r, self.r*2, -0.5*self.t, self.msh_s)
        rect_interim = gmsh.model.geo.addPoint(self.r + self.length, self.r*2, -0.5*self.t, self.msh_s)
        rect_interim1 = gmsh.model.geo.addPoint(self.r + self.length, 0, -0.5*self.t, self.msh_s)
        rect_interim2 = gmsh.model.geo.addPoint(self.r, 0, -0.5*self.t, self.msh_s)
        rect_end = gmsh.model.geo.addPoint(self.r, self.r*2, -0.5*self.t, self.msh_s)

        rect_line1 = gmsh.model.geo.addLine(rect_start, rect_interim)
        rect_line2 = gmsh.model.geo.addLine(rect_interim, rect_interim1)
        rect_line3 = gmsh.model.geo.addLine(rect_interim1, rect_interim2)
        rect_line4 = gmsh.model.geo.addLine(rect_interim2, rect_end)

        rect_loop = gmsh.model.geo.addCurveLoop([rect_line1, rect_line2, rect_line3, rect_line4])
        
        rect_surf = gmsh.model.geo.addPlaneSurface([rect_loop])

        rect_out = gmsh.model.geo.extrude([(2,rect_surf)],0,0,self.t)

        gmsh.model.geo.synchronize() # we have to sync before calling addPhysicalGroup
















        gmsh.model.mesh.generate(3) # 3 is the dimension of the mesh

        gmsh.option.set_number("Mesh.MshFileVersion", 2.2) # to force mesh file format to 2.2

        gmsh.write(meshFileName)

        nbNodes = gmsh.option.get_number("Mesh.NbNodes")
        nbTriangles = gmsh.option.get_number("Mesh.NbTriangles")
        nbTetra = gmsh.option.get_number("Mesh.NbTetrahedra")

# uncomment next line to see a graphic rendering of the mesh
        gmsh.fltk.run()
                
        gmsh.finalize()
        
        print("mesh file " + meshFileName + " generated, nb nodes =" + str(nbNodes) + " , nb tetra =" +str(nbTetra) )



height = 10          # we use nanometers
radius = 50 
elt_size = 4         # typical element size

length = 80         # length of the bar
surface_name = "surface"
volume_name = "volume"

# Create the mesh and save it in the file "cylinder.msh".
mesh = Mediator(radius, height, length, elt_size, surface_name, volume_name)
mesh.make("cylinder.msh")