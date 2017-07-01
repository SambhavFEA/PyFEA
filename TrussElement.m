classdef TrussElement < handle
    %TrussElement Summary of this class goes here
    %   Detailed explanation goes here
    
    properties (SetAccess='private')
        No  %Ellement no, to be used as primary key
        LN  %Local nodes array
        length %element length
        dc %direction cosine array
        E   %Young's Modulus of the material
        area%Area of cross section
        Ke  %Element stiffness matrix
        
        Force=0  %Force in element
        Stress=0 %Stress in element
        Strain=0 %Strain in element
    end
    
    properties (GetAccess='private', SetAccess='private')
        Ti  %Transformation matrix
    end
   
    
    methods
        function obj=TrussElement(ArrayNodes, inputmatrix,materialmat)
            if nargin~=0
                m=size(inputmatrix,1);
                obj(m)=TrussElement;
                for i=1:m
                   
                obj(i).No=inputmatrix(i,1);
                obj(i).LN=[findobj(ArrayNodes,'No',inputmatrix(i,2)) findobj(ArrayNodes,'No',inputmatrix(i,3))];
                obj(i).length=elementLength(obj(i).LN(1),obj(i).LN(2));
                obj(i).dc=[(obj(i).LN(2).X-obj(i).LN(1).X)/obj(i).length (obj(i).LN(2).Y-obj(i).LN(1).Y)/obj(i).length (obj(i).LN(2).Z-obj(i).LN(1).Z)/obj(i).length];
                
                matno=inputmatrix(i,4);
                matno=find(materialmat(:,1)==matno);
                obj(i).E=materialmat(matno,2);
                obj(i).area=materialmat(matno,4);
                obj(i).Ti=[obj(i).dc(1) obj(i).dc(2) obj(i).dc(3) 0 0 0; 0 0 0 obj(i).dc(1) obj(i).dc(2) obj(i).dc(3)];
                obj(i).Ke=(obj(i).Ti.'*[1 -1; -1 1]*obj(i).Ti).*(obj(i).E*obj(i).area/obj(i).length);
                  
                end
            end
        end
        function calcResults(obj)
            for i=1:3
                obj.Strain=obj.Strain+(obj.dc(i)*((obj.LN(2).U(i))-(obj.LN(1).U(i))));
            end
            obj.Force=obj.Strain*obj.area*obj.E/obj.length;
            obj.Stress=obj.Force/obj.area;
        end  
    end
end





