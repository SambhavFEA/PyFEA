function [ Stiffness ] = GlobalStiffnessAssembler( NodeArray, ElementArray )
%GlobalStiffnessAssembler Summary of this function goes here
%   Detailed explanation goes here
if isa(ElementArray,'Beam3DElement')
    eletype=6;
else
    eletype=3;
end
Stiffness(eletype*size(NodeArray,2),eletype*size(NodeArray,2))=zeros;
z=[NodeArray.No];
for i=1:size(ElementArray,2)
    
    m=find(z==(ElementArray(i).LN(1).No));
    n=find(z==(ElementArray(i).LN(2).No));
%     for j=1:3
%         for k=1:3
%             Stiffness((3*m)-(j-1),(3*m)-(k-1))=Stiffness((3*m)-(j-1),(3*m)-(k-1))+ElementArray(i).Ke(4-j,4-k);
%             Stiffness((3*n)-(j-1),(3*n)-(k-1))=Stiffness((3*n)-(j-1),(3*n)-(k-1))+ElementArray(i).Ke(7-j,7-k);
%             Stiffness((3*m)-(j-1),(3*n)-(k-1))=Stiffness((3*m)-(j-1),(3*n)-(k-1))+ElementArray(i).Ke(4-j,7-k);
%             Stiffness((3*n)-(j-1),(3*m)-(k-1))=Stiffness((3*n)-(j-1),(3*m)-(k-1))+ElementArray(i).Ke(7-j,4-k);
%         end
%     end
    Stiffness((eletype*m)-(eletype-1):eletype*m,(eletype*m)-(eletype-1):eletype*m)=Stiffness((eletype*m)-(eletype-1):eletype*m,(eletype*m)-(eletype-1):eletype*m)+ElementArray(i).Ke(1:eletype,1:eletype);
    Stiffness((eletype*n)-(eletype-1):eletype*n,(eletype*n)-(eletype-1):eletype*n)=Stiffness((eletype*n)-(eletype-1):eletype*n,(eletype*n)-(eletype-1):eletype*n)+ElementArray(i).Ke(eletype+1:end,eletype+1:end);
    Stiffness((eletype*m)-(eletype-1):eletype*m,(eletype*n)-(eletype-1):eletype*n)=Stiffness((eletype*m)-(eletype-1):eletype*m,(eletype*n)-(eletype-1):eletype*n)+ElementArray(i).Ke(1:eletype,eletype+1:end);
    Stiffness((eletype*n)-(eletype-1):eletype*n,(eletype*m)-(eletype-1):eletype*m)=Stiffness((eletype*n)-(eletype-1):eletype*n,(eletype*m)-(eletype-1):eletype*m)+ElementArray(i).Ke(eletype+1:end,1:eletype);
end


end

