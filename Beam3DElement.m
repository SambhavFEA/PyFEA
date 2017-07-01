classdef Beam3DElement<handle
    %Beam3DElement Summary of this class goes here
    %   Detailed explanation goes here
    properties (SetAccess='private')
        No  %Ellement no, to be used as primary key
        LN  %Local nodes array
        length %element length
        dc %direction cosine array
        E   %Young's Modulus of the material
        G   %Modulus of rigidity
        mu  %Poisson's ratio
        Iy  %moment of inertia about y axis
        Iz  %moment of inertia about z axis
        J   %polar moment of inertia
        area%Area of cross section
        Ke  %Element stiffness matrix
    end
        
    properties (GetAccess='private', SetAccess='private')
        Ti  %Transformation matrix
    end
    
    properties
        Force  %Force in element
        Stress %Stress in element
        Strain %Strain in element
    end
    
    methods
        function obj=Beam3DElement(ArrayNodes, inputmatrix,materialmat)
            if nargin~=0     
                m=size(inputmatrix,1);
                obj(m)=Beam3DElement;
                for i=1:m
                    obj(i).No=inputmatrix(i,1);
                    obj(i).LN=[findobj(ArrayNodes,'No',inputmatrix(i,2)) findobj(ArrayNodes,'No',inputmatrix(i,3))];
                    obj(i).length=elementLength(obj(i).LN(1),obj(i).LN(2));
                    
                    matno=inputmatrix(i,4);
                    matno=find(materialmat(:,1)==matno);
                    obj(i).E=materialmat(matno,2);
                    obj(i).mu=inputmatrix(i,3);
                    obj(i).G=obj(i).E/(2*(1+obj(i).mu));
                    obj(i).area=materialmat(matno,4);
                    obj(i).Iy=materialmat(matno,5);
                    obj(i).Iz=materialmat(matno,6);
                    obj(i).J=materialmat(matno,7);
                    
                    %Direction Cosines
                    if m==1
                        vect1=[obj(i).LN(2).X-obj(i).LN(1).X obj(i).LN(2).Y-obj(i).LN(1).Y obj(i).LN(2).Z-obj(i).LN(1).Z];
                        obj(i).dc=vect1/(sqrt(3)*rms(vect1));
                    else
                        vect1=[(obj(i).LN(2).X-obj(i).LN(1).X)/obj(i).length (obj(i).LN(2).Y-obj(i).LN(1).Y)/obj(i).length (obj(i).LN(2).Z-obj(i).LN(1).Z)/obj(i).length];
                        vect2=materialmat(matno,8:10);
                        vect3=cross(vect1,vect2);
                        obj(i).dc=[vect1;vect2;vect3];

                    end
                    obj(i).Ti=zeros(12);
                    obj(i).Ti(1:3,1:3)=obj(i).dc;
                    obj(i).Ti(4:6,4:6)=obj(i).dc;
                    obj(i).Ti(7:9,7:9)=obj(i).dc;
                    obj(i).Ti(10:12,10:12)=obj(i).dc;
                    
                    %Element Matrix
                    obj(i).Ke=zeros(12,12);
                    obj(i).Ke([1 7],[1 7])=(obj(i).E*obj(i).area/obj(i).length)*[1 -1;-1 1];
                    obj(i).Ke([2 6 8 12],[2 6 8 12])=(obj(i).E*obj(i).Iz/obj(i).length^3)*[12 6*obj(i).length -12 6*obj(i).length;
                                                                                           6*obj(i).length 4*obj(i).length^2 -6*obj(i).length 2*obj(i).length^2;
                                                                                           -12 -6*obj(i).length 12 -6*obj(i).length;
                                                                                           6*obj(i).length  2*obj(i).length^2 -6*obj(i).length 4*obj(i).length^2];
                    obj(i).Ke([3 5 9 11],[3 5 9 11])=(obj(i).E*obj(i).Iy/obj(i).length^3)*[12 6*obj(i).length -12 6*obj(i).length;
                                                                                           6*obj(i).length 4*obj(i).length^2 -6*obj(i).length 2*obj(i).length^2;
                                                                                           -12 -6*obj(i).length 12 -6*obj(i).length;
                                                                                           6*obj(i).length  2*obj(i).length^2 -6*obj(i).length 4*obj(i).length^2];
                    obj(i).Ke([4 10],[4 10])=(obj(i).G*obj(i).J/obj(i).length)*[1 -1;-1 1];

                    obj(i).Ke=obj(i).Ti*obj(i).Ke*obj(i).Ti';
                end
            end
        end
        function calcForce(obj)
            obj.Force=obj.Ti(1,3)*((obj.LN(2).U)-(obj.LN(1).U))';
        end
    end
end

