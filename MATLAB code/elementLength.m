function [ elemLength ] = elementLength( node1,node2 )
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
elemLength=sqrt((node1.X-node2.X)^2+(node1.Y-node2.Y)^2+(node1.Z-node2.Z)^2);

end

