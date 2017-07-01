classdef NodalPoint < handle
    %NodalPoint class defines the node
    %  
    
    properties
        F=[nan nan nan]  %Forces on node
        M=[nan nan nan]  %Moments on node 
        U=[nan nan nan]  %Displacements of node
        A=[nan nan nan]  %Angle of node
    end
    properties (SetAccess='private')
        No  %nodal point number/name be used as primary key
        X   %X coordinate
        Y   %Y coordinate
        Z   %Z coordinate

    end

    
    methods
%         function F=confirmnan(F,U)
%             if isnan(F)&&isnan(U)
%                 F=0;
%             end
%         end
        
        function obj=NodalPoint(inputmatrix)
            if nargin~=0
                
                m=size(inputmatrix,1);
                obj(m)=NodalPoint;
                for i=1:m
                    obj(i).No=inputmatrix(i,1);
                    obj(i).X=inputmatrix(i,2);
                    obj(i).Y=inputmatrix(i,3);
                    obj(i).Z=inputmatrix(i,4);
%                     for j=1:3
%                         if isnan(inputmatrix(i,j+4))&&isnan(inputmatrix(i,j+7))
%                             inputmatrix(i,j+4)=0;
%                         end
%                         obj(i).U(j)=inputmatrix(i,j+7);
%                         obj(i).F(j)=inputmatrix(i,j+4);
%                         if  strcmp(eletype,'Beam3d')
%                             if isnan(inputmatrix(i,j+7))&&isnan(inputmatrix(i,j+10))
%                                 inputmatrix(i,j+7)=0;
%                             end
%                             obj(i).A(j)=inputmatrix(i,j+10);
%                             obj(i).M(j)=inputmatrix(i,j+7);
%                         end
%                     end
                end
                
            end
        end
    end
end

